
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from cap.decorators import template_list_item

from invoices.models import Arrival, Sale


@admin.register(Arrival, Sale)
class InvoiceAdmin(admin.ModelAdmin):

    add_form_template = 'invoices/addform.html'

    list_display = ['id', 'created', 'type', 'get_item_actions']
    list_display_links = ['id', 'created']
    list_filter = ['type', 'created']

    def response_post_save_add(self, request, obj):
        return redirect(obj.manage_url)

    @template_list_item('invoices/list_item_actions.html', _('Actions'))
    def get_item_actions(self, obj):
        return {'object': obj}
