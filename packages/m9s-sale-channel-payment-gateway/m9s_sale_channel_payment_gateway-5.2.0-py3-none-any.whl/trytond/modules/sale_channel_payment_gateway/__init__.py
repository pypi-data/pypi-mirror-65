# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import channel
from . import sale

__all__ = ['register']


def register():
    Pool.register(
        sale.Sale,
        channel.SaleChannel,
        module='sale_channel_payment_gateway', type_='model')
