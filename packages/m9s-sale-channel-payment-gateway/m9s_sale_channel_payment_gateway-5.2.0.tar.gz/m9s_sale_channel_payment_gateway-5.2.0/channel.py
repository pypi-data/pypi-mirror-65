# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
from trytond.model import fields

STATES = {
    'readonly': ~Eval('active', True),
    }
DEPENDS = ['active']


class SaleChannel(metaclass=PoolMeta):
    __name__ = 'sale.channel'

    payment_authorize_on = fields.Selection(
        'get_authorize_options', 'Payment Authorize', states=STATES,
        depends=DEPENDS,
        help='Configure the payment authorize method for this channel. '
        'If empty, the default from Sale configuration is used.'
    )
    payment_capture_on = fields.Selection(
        'get_capture_options', 'Payment Capture', states=STATES,
        depends=DEPENDS,
        help='Configure the payment capture method for this channel. '
        'If empty, the default from Sale configuration is used.'
    )

    @classmethod
    def get_authorize_options(cls):
        SaleConfiguration = Pool().get('sale.configuration')
        field_name = 'payment_authorize_on'
        selection = SaleConfiguration.fields_get(
            [field_name])[field_name]['selection']
        selection.insert(0, ('', ''))
        return selection

    @classmethod
    def get_capture_options(cls):
        SaleConfiguration = Pool().get('sale.configuration')
        field_name = 'payment_capture_on'
        selection = SaleConfiguration.fields_get(
            [field_name])[field_name]['selection']
        selection.insert(0, ('', ''))
        return selection
