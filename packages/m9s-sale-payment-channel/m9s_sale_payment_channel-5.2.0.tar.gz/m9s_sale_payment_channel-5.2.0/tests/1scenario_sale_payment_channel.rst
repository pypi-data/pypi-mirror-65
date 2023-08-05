=============================
Sale Payment Channel Scenario
=============================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Install sale::

    >>> config = activate_modules(['party', 'sale_payment_channel'])

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')
    >>> period = fiscalyear.periods[0]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> receivable = accounts['receivable']
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> cash = accounts['cash']

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.account_receivable = receivable
    >>> customer.save()

Create category::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name='Category')
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.customer_taxes.append(tax)
    >>> account_category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'service'
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.account_category = account_category
    >>> product, = template.products
    >>> product.cost_price = Decimal('5')
    >>> template.save()
    >>> product, = template.products

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create a channel::

    >>> Channel = Model.get('sale.channel')
    >>> Sequence = Model.get('ir.sequence')
    >>> PriceList = Model.get('product.price_list')
    >>> Location = Model.get('stock.location')
    >>> warehouse, = Location.find([
    ...         ('code', '=', 'WH'),
    ...         ])
    >>> price_list = PriceList()
    >>> price_list.name = 'Default price list'
    >>> price_list.save()
    >>> channel = Channel()
    >>> channel.name = 'Local channel'
    >>> channel.warehouse = warehouse
    >>> channel.shipment_method = 'order'
    >>> channel.invoice_method = 'order'
    >>> sequence, = Sequence.find([('code', '=', 'sale.sale')])
    >>> channel.sequence = sequence
    >>> channel.payment_term = payment_term
    >>> channel.price_list = price_list
    >>> channel.save()

Create journals::

    >>> StatementJournal = Model.get('account.statement.journal')
    >>> Journal = Model.get('account.journal')
    >>> sequence = Sequence(name='Satement',
    ...     code='account.journal',
    ...     company=company,
    ... )
    >>> sequence.save()
    >>> account_journal = Journal(name='Statement',
    ...     type='statement',
    ...     sequence=sequence,
    ... )
    >>> account_journal.save()
    >>> statement_journal = StatementJournal(name='Default',
    ...     journal=account_journal,
    ...     account=cash,
    ...     validation='balance',
    ... )
    >>> statement_journal.save()

Create a device::

    >>> Device = Model.get('sale.device')
    >>> device = Device()
    >>> device.channel = channel
    >>> device.name = 'Default'
    >>> device.journals.append(statement_journal)
    >>> device.journal = statement_journal
    >>> device.save()

Reload the context::

    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> user, = User.find([('login', '=', 'admin')])
    >>> user.channels.append(channel)
    >>> user.channel = channel
    >>> user.sale_device = device
    >>> user.save()
    >>> config._context = User.get_preferences(True, config.context)

Create sale user::

    >>> channel = Channel(channel.id)
    >>> sale_user = User()
    >>> sale_user.name = 'Sale'
    >>> sale_user.login = 'sale'
    >>> sale_user.main_company = company
    >>> sale_group, = Group.find([('name', '=', 'Sales')])
    >>> sale_user.groups.append(sale_group)
    >>> sale_user.channels.append(channel)
    >>> sale_user.channel = channel
    >>> sale_user.sale_device = device
    >>> sale_user.save()

Create account user::

    >>> channel = Channel(channel.id)
    >>> account_user = User()
    >>> account_user.name = 'Account'
    >>> account_user.login = 'account'
    >>> account_user.main_company = company
    >>> account_group, = Group.find([('name', '=', 'Account')])
    >>> account_user.groups.append(account_group)
    >>> account_user.channels.append(channel)
    >>> account_user.channel = channel
    >>> account_user.sale_device = device
    >>> account_user.save()

Sale services::

    >>> config.user = sale_user.id
    >>> Sale = Model.get('sale.sale')
    >>> SaleLine = Model.get('sale.line')
    >>> sale = Sale()
    >>> sale.party = customer
    >>> sale_line = sale.lines.new()
    >>> sale_line.product = product
    >>> sale_line.quantity = 2.0
    >>> sale.save()
    >>> len(sale.shipments), len(sale.invoices), len(sale.payments)
    (0, 0, 0)

Open statements for current device::

    >>> Statement = Model.get('account.statement')
    >>> len(Statement.find([('state', '=', 'draft')]))
    0
    >>> open_statment = Wizard('open.statement')
    >>> open_statment.execute('create_')
    >>> open_statment.form.result == 'Statement Default opened.'
    True
    >>> payment_statement, = Statement.find([('state', '=', 'draft')])

Partially pay the sale::

    >>> pay_sale = Wizard('sale.payment', [sale])
    >>> pay_sale.form.journal == statement_journal
    True
    >>> pay_sale.form.payment_amount
    Decimal('22.00')
    >>> pay_sale.form.payment_amount = Decimal('12.00')
    >>> pay_sale.execute('pay_')
    >>> sale.invoice_state = 'waiting'
    >>> sale.save()
    >>> statment_line, = payment_statement.lines
    >>> statment_line.amount
    Decimal('12.00')
    >>> statment_line.party == customer
    True
    >>> statment_line.sale == sale
    True
    >>> sale.reload()
    >>> sale.paid_amount
    Decimal('12.00')
    >>> sale.invoice_state != None
    True
    >>> sale.residual_amount
    Decimal('10.00')
    >>> len(sale.shipments), len(sale.invoices), len(sale.payments)
    (0, 0, 1)

When the sale is paid invoice is generated::

    >>> pay_sale.form.payment_amount
    Decimal('10.00')
    >>> pay_sale.execute('pay_')
    >>> payment_statement.reload()
    >>> _, statement_line = payment_statement.lines
    >>> statement_line.amount
    Decimal('10.00')
    >>> statement_line.party == customer
    True
    >>> statement_line.sale == sale
    True
    >>> sale.reload()
    >>> sale.paid_amount
    Decimal('22.00')
    >>> sale.residual_amount
    Decimal('0.00')
    >>> len(sale.shipments), len(sale.invoices), len(sale.payments)
    (0, 1, 2)

An invoice should be created for the sale::

    >>> invoice, = sale.invoices
    >>> config.user = account_user.id
    >>> invoice.state == 'posted'
    True
    >>> invoice.untaxed_amount
    Decimal('20.00')
    >>> invoice.tax_amount
    Decimal('2.00')
    >>> invoice.total_amount
    Decimal('22.00')

When the statement is closed the invoices are paid and sale is done::

    >>> close_statment = Wizard('close.statement')
    >>> close_statment.execute('validate')
    >>> close_statment.form.result == 'Statement Default - Default closed.'
    True
    >>> payment_statement.reload()
    >>> payment_statement.state == 'validated'
    True
    >>> all(l.invoice == invoice for l in payment_statement.lines)
    True
    >>> payment_statement.balance
    Decimal('22.00')
    >>> invoice.reload()
    >>> invoice.state == 'paid'
    True
    >>> config.user = sale_user.id
    >>> sale.reload()
    >>> sale.state == 'done'
    True
