
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from exchange.models import MultiCurrencyPrice


class InvoiceField(models.ForeignKey):

    def __init__(
            self,
            to,
            verbose_name=_('Invoice'),
            on_delete=models.CASCADE,
            related_name='items',
            *args, **kwargs):

        super().__init__(
            to=to,
            verbose_name=verbose_name,
            on_delete=on_delete,
            related_name=related_name,
            *args, **kwargs)


class InvoiceTypeField(models.PositiveIntegerField):

    def __init__(
            self,
            choices,
            verbose_name=_('Type'),
            *args, **kwargs):

        super().__init__(
            choices=choices,
            verbose_name=verbose_name,
            *args, **kwargs
        )


class Invoice(models.Model):

    type = NotImplemented

    created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    def __str__(self):
        return str(self.created)

    @classmethod
    def create(cls, type):
        return cls.objects.create(type=type)

    @property
    def invoice_type(self):
        return self.__class__.__name__.lower()

    @property
    def manage_url(self):
        return reverse_lazy('invoices:manage', args=[
            self.invoice_type,
            self.pk
        ])

    @property
    def print_url(self):
        return reverse_lazy('invoices:print', args=[
            self.invoice_type,
            self.pk
        ])

    @property
    def add_item_url(self):
        return reverse_lazy('invoices:add-item', args=[
            self.invoice_type,
            self.pk
        ])

    @property
    def model_name(self):
        return self._meta.verbose_name

    @transaction.atomic
    def add_item(self, product, qty=1):
        try:
            item = self.items.get(product=product)
            item.qty += qty
            item.save()

        except ObjectDoesNotExist:
            item = self.items.create(
                product=product,
                qty=qty,
                **product.price_values
            )

        self._handle_add_item(product, qty)

        return item

    def _handle_add_item(self, product, qty):
        pass

    @transaction.atomic
    def set_item_qty(self, item_id, value):

        item = self.items.select_related('product').get(pk=item_id)

        if item.qty == value:
            return

        self._handle_set_item_qty(item, value)

        item.qty = value
        item.save(update_fields=['qty'])

        return item

    def _handle_set_item_qty(self, item, value):
        pass

    @transaction.atomic
    def remove_item(self, item_id):

        item = self.items.select_related('product').get(pk=item_id)

        self._handle_remove_item(item)

        product = item.product

        item.delete()

        return product

    def _handle_remove_item(self, item):
        pass

    class Meta:
        abstract = True


class InvoiceItem(MultiCurrencyPrice):

    invoice = NotImplemented

    product = models.ForeignKey(
        'products.Product',
        verbose_name=_('Product'),
        on_delete=models.CASCADE)

    qty = models.IntegerField(_('Quantity'))

    @property
    def set_qty_url(self):
        return reverse_lazy('invoices:set-item-qty', args=[
            self.invoice.invoice_type,
            self.invoice.pk,
            self.pk
        ])

    @property
    def remove_url(self):
        return reverse_lazy('invoices:remove-item', args=[
            self.invoice.invoice_type,
            self.invoice.pk,
            self.pk
        ])

    def render(self):
        return render_to_string('invoices/item.html', {'object': self})

    class Meta:
        abstract = True


class Arrival(Invoice):

    TYPE_INCOME = 1
    TYPE_RETURN = 2
    TYPE_CUSTOM = 2

    TYPES = (
        (TYPE_INCOME, _('Income')),
        (TYPE_RETURN, _('Return')),
        (TYPE_CUSTOM, _('Custom')),
    )

    type = InvoiceTypeField(TYPES)

    def _handle_add_item(self, product, qty):

        product.add_stock(value=qty)

    def _handle_set_item_qty(self, item, value):

        if item.qty > value:
            item.product.subtract_stock(item.qty - value)
        else:
            item.product.add_stock(value - item.qty)

    def _handle_remove_item(self, item):

        if item.qty > 0:
            item.product.subtract_stock(item.qty)

    class Meta:
        verbose_name = _('Arrival')
        verbose_name_plural = _('Arrivals')


class ArrivalItem(InvoiceItem):

    invoice = InvoiceField(Arrival)


class Sale(Invoice):

    TYPE_SALE = 1
    TYPE_CASH_REGISTER = 2
    TYPE_WRITE_OFF = 3
    TYPE_ONLINE = 4
    TYPE_CUSTOM = 5

    TYPES = (
        (TYPE_SALE, _('Sale')),
        (TYPE_CASH_REGISTER, _('Cash register')),
        (TYPE_WRITE_OFF, _('Write off')),
        (TYPE_ONLINE, _('Online')),
        (TYPE_CUSTOM, _('Custom')),
    )

    type = InvoiceTypeField(TYPES)

    def _handle_add_item(self, product, qty):

        product.subtract_stock(value=qty)

    def _handle_set_item_qty(self, item, value):

        if value > item.qty:
            item.product.subtract_stock(value - item.qty)
        else:
            item.product.add_stock(item.qty - value)

    def _handle_remove_item(self, item):

        if item.qty > 0:
            item.product.add_stock(item.qty)

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')


class SaleItem(InvoiceItem):

    invoice = InvoiceField(Sale)
