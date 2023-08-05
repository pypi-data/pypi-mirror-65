# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from sql.aggregate import Sum
from sql.conditionals import Coalesce

from trytond.model import ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Bool, Eval, Not
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.exceptions import UserError
from trytond.i18n import gettext


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    pos_payments = fields.One2Many('account.statement.line', 'sale',
        'POS Payments')
    paid_amount = fields.Function(fields.Numeric('Paid Amount', readonly=True),
        'get_paid_amount')
    residual_amount = fields.Function(fields.Numeric('Residual Amount'),
        'get_residual_amount', searcher='search_residual_amount')
    sale_device = fields.Many2One('sale.device', 'Sale Device',
        domain=[('channel', '=', Eval('channel'))],
        depends=['channel'], states={
            'readonly': Eval('state') != 'draft',
            }
        )

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls._buttons.update({
                'wizard_sale_payment': {
                    'invisible': Eval('state') == 'done',
                    'readonly': Not(Bool(Eval('lines'))),
                    },
                })

    @staticmethod
    def default_sale_device():
        User = Pool().get('res.user')
        user = User(Transaction().user)
        return user.sale_device and user.sale_device.id or None

    @classmethod
    def workflow_to_end(cls, sales):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        Date = pool.get('ir.date')
        StatementLine = pool.get('account.statement.line')

        to_write = []
        to_do = []
        for sale in sales:
            if sale.state == 'draft':
                cls.quote([sale])
            if sale.state == 'quotation':
                cls.confirm([sale])
            if sale.state == 'confirmed':
                cls.process([sale])

            if not sale.invoices and sale.invoice_method == 'order':
                raise UserError(gettext(
                    'sale_payment_channel.not_customer_invoice',
                        reference=sale.reference))

            grouping = getattr(sale.party, 'sale_invoice_grouping_method',
                False)
            if sale.invoices and not grouping:
                for invoice in sale.invoices:
                    if invoice.state == 'draft':
                        if not getattr(invoice, 'invoice_date', False):
                            invoice.invoice_date = Date.today()
                        if not getattr(invoice, 'accounting_date', False):
                            invoice.accounting_date = Date.today()
                        invoice.description = (sale.channel.rec_name + '/'
                            + sale.number)
                        invoice.save()
                Invoice.post(sale.invoices)
                for payment in sale.pos_payments:
                    invoice = sale.invoices[0]
                    payment.invoice = invoice.id
                    # Because of account_invoice_party_without_vat module
                    # could be installed, invoice party may be different of
                    # payment party if payment party has not any vat
                    # and both parties must be the same
                    if payment.party != invoice.party:
                        payment.party = invoice.party
                    to_write.extend(([payment], payment._save_values))

            if sale.is_done():
                to_do.append(sale)

        if to_write:
            StatementLine.write(*to_write)

        if to_do:
            cls.do(to_do)

    @classmethod
    def get_paid_amount(cls, sales, names):
        result = {n: {s.id: Decimal(0) for s in sales} for n in names}
        for name in names:
            for sale in sales:
                for payment in sale.pos_payments:
                    result[name][sale.id] += payment.amount
        return result

    @classmethod
    def get_residual_amount(cls, sales, name):
        return {s.id: s.total_amount - s.paid_amount if s.state != 'cancel'
            else Decimal(0) for s in sales}

    @classmethod
    def search_residual_amount(cls, name, clause):
        pool = Pool()
        Sale = pool.get('sale.sale')
        StatementLine = pool.get('account.statement.line')

        sale = Sale.__table__()
        payline = StatementLine.__table__()
        Operator = fields.SQL_OPERATORS[clause[1]]
        value = clause[2]

        query = sale.join(
            payline,
            type_='LEFT',
            condition=(sale.id == payline.sale)
            ).select(
                sale.id,
                where=((sale.total_amount_cache != None) &
                    (sale.state.in_([
                        'draft',
                        'quotation',
                        'confirmed',
                        'processing',
                        'done']))),
                group_by=(sale.id),
                having=(
                    (Sum(Coalesce(payline.amount, 0)) < sale.total_amount_cache)
                & Operator(sale.total_amount_cache -
                    Sum(Coalesce(payline.amount, 0)), value)
                ))

        return [('id', 'in', query)]

    @classmethod
    @ModelView.button_action('sale_payment_channel.wizard_sale_payment')
    def wizard_sale_payment(cls, sales):
        pass

    @classmethod
    def copy(cls, sales, default=None):
        if default is None:
            default = {}
        default['pos_payments'] = None
        return super(Sale, cls).copy(sales, default)


class SalePaymentForm(ModelView):
    'Sale Payment Form'
    __name__ = 'sale.payment.form'
    journal = fields.Many2One('account.statement.journal', 'POS Journal',
        domain=[
            ('id', 'in', Eval('journals', [])),
            ],
        depends=['journals'], required=True)
    journals = fields.One2Many('account.statement.journal', None,
        'Allowed POS Journals')
    payment_amount = fields.Numeric('Payment amount', required=True,
        digits=(16, Eval('currency_digits', 2)),
        depends=['currency_digits'])
    currency_digits = fields.Integer('Currency Digits')
    party = fields.Many2One('party.party', 'Customer', readonly=True)


class WizardSalePayment(Wizard):
    'Wizard Sale Payment'
    __name__ = 'sale.payment'
    start = StateView('sale.payment.form',
        'sale_payment_channel.sale_payment_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Pay', 'pay_', 'tryton-ok', default=True),
        ])
    pay_ = StateTransition()

    def default_start(self, fields):
        pool = Pool()
        Sale = pool.get('sale.sale')
        User = pool.get('res.user')
        sale = Sale(Transaction().context['active_id'])
        user = User(Transaction().user)
        sale_device = sale.sale_device or user.sale_device or False
        if user.id != 0 and not sale_device:
            raise UserError(gettext(
                    'sale_payment_channel.sale_device_configuration_missing'))
        return {
            'journal': sale_device.journal.id if sale_device.journal else None,
            'journals': [j.id for j in sale_device.journals],
            'payment_amount': sale.total_amount - sale.paid_amount
                if sale.paid_amount else sale.total_amount,
            'currency_digits': sale.currency_digits,
            'party': sale.party.id,
            }

    def get_statement_line(self, sale):
        pool = Pool()
        Date = pool.get('ir.date')
        Sale = pool.get('sale.sale')
        Statement = pool.get('account.statement')
        StatementLine = pool.get('account.statement.line')

        form = self.start
        statements = Statement.search([
                ('journal', '=', form.journal),
                ('state', '=', 'draft'),
                ], order=[('date', 'DESC')])
        if not statements:
            raise UserError(gettext(
                    'sale_payment_channel.missing_draft_statement',
                    journal=form.journal.name))

        if not sale.number:
            Sale.set_number([sale])

        with Transaction().set_context(date=Date.today()):
            account = sale.party.account_receivable_used
        if not account:
            raise UserError(gettext(
                    'sale_payment_channel.party_without_account_receivable',
                    party=sale.party.name))

        if form.payment_amount:
            description = '(' + sale.channel.rec_name + ') ' + sale.number
            return StatementLine(
                statement=statements[0],
                date=Date.today(),
                amount=form.payment_amount,
                party=sale.party,
                account=account,
                description=sale.number,
                sale=sale,
                )

    def transition_pay_(self):
        Sale = Pool().get('sale.sale')

        active_id = Transaction().context.get('active_id', False)
        sale = Sale(active_id)

        line = self.get_statement_line(sale)
        if line:
            line.save()

        if sale.total_amount != sale.paid_amount:
            return 'start'
        if sale.state != 'draft':
            return 'end'

        sale.description = self.get_sale_description(sale)
        sale.save()

        Sale.workflow_to_end([sale])
        return 'end'

    def get_sale_description(self, sale):
        pool = Pool()
        User = pool.get('res.user')
        user = User(Transaction().user)
        sale_device = sale.sale_device or user.sale_device or False
        description = sale.number
        if sale_device:
            description = '(' + sale_device.rec_name + ') ' + description
        return description


class WizardSaleReconcile(Wizard):
    'Reconcile Sales'
    __name__ = 'sale.reconcile'
    start = StateTransition()
    reconcile = StateTransition()

    def transition_start(self):
        pool = Pool()
        Sale = pool.get('sale.sale')
        Line = pool.get('account.move.line')
        for sale in Sale.browse(Transaction().context['active_ids']):
            account = sale.party.account_receivable
            lines = []
            amount = Decimal('0.0')
            for invoice in sale.invoices:
                for line in invoice.lines_to_pay:
                    if not line.reconciliation:
                        lines.append(line)
                        amount += line.debit - line.credit
            for payment in sale.pos_payments:
                if not payment.move:
                    continue
                for line in payment.move.lines:
                    if (not line.reconciliation and
                            line.account.id == account.id):
                        lines.append(line)
                        amount += line.debit - line.credit
            if lines and amount == Decimal('0.0'):
                Line.reconcile(lines)
        return 'end'
