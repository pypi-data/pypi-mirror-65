# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls.payment_authorize_on.states = cls.channel.states
        cls.payment_capture_on.states = cls.channel.states

    @classmethod
    def default_payment_authorize_on(cls):
        pool = Pool()
        Channel = pool.get('sale.channel')
        if Transaction().context.get('current_channel'):
            channel = Channel(Transaction().context['current_channel'])
            if channel.payment_authorize_on:
                return channel.payment_authorize_on
        return super(Sale, cls).default_payment_authorize_on()

    @classmethod
    def default_payment_capture_on(cls):
        pool = Pool()
        Channel = pool.get('sale.channel')
        if Transaction().context.get('current_channel'):
            channel = Channel(Transaction().context['current_channel'])
            if channel.payment_capture_on:
                return channel.payment_capture_on
        return super(Sale, cls).default_payment_capture_on()

    def on_change_channel(self):
        pool = Pool()
        SaleConfiguration = pool.get('sale.configuration')
        super(Sale, self).on_change_channel()
        if not self.channel:
            return
        if self.channel.payment_authorize_on:
            self.payment_authorize_on = self.channel.payment_authorize_on
        else:
            self.payment_authorize_on = \
                SaleConfiguration(1).payment_authorize_on
        if self.channel.payment_capture_on:
            self.payment_capture_on = self.channel.payment_capture_on
        else:
            self.payment_capture_on = SaleConfiguration(1).payment_capture_on
