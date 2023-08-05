# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval


class User(metaclass=PoolMeta):
    __name__ = "res.user"
    sale_device = fields.Many2One('sale.device', 'Sale Device',
            domain=[('channel', '=', Eval('current_channel'))],
            depends=['current_channel']
    )

    @classmethod
    def __setup__(cls):
        super(User, cls).__setup__()
        if 'sale_device' not in cls._preferences_fields:
            cls._preferences_fields.extend([
                    'sale_device',
                    ])
