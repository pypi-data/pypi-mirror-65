
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from pagination import paginate

from invoices.forms import SearchProductForm
from invoices.models import Sale, Arrival

from apps.products.models import Product


@staff_member_required
def manage_invoice(request, invoice_type, invoice_id):

    context = admin.site.each_context(request)

    context['invoice'] = _get_invoice(invoice_type, invoice_id)
    context['invoice_type'] = invoice_type

    return render(request, 'invoices/manage.html', context)


@csrf_exempt
@require_POST
@staff_member_required
def add_item(request, invoice_type, invoice_id):

    invoice = _get_invoice(invoice_type, invoice_id)

    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    try:
        item = invoice.add_item(product)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    return JsonResponse({
        'status': 'OK',
        'html': item.render(),
        'item_id': item.id,
        'product': {
            'id': product.id,
            'stock': product.stock
        }
    })


@csrf_exempt
@require_POST
@staff_member_required
def set_item_qty(request, invoice_type, invoice_id, item_id):

    try:
        value = int(request.POST['value'])
    except (KeyError, TypeError):
        return HttpResponseBadRequest(_('Incorrect value'))

    invoice = _get_invoice(invoice_type, invoice_id)

    try:
        item = invoice.set_item_qty(item_id, value)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    return JsonResponse({
        'message': _('Quantity updated'),
        'product': {
            'id': item.product.id,
            'stock': item.product.stock
        }
    })


@csrf_exempt
@require_POST
@staff_member_required
def remove_item(request, invoice_type, invoice_id, item_id):

    invoice = _get_invoice(invoice_type, invoice_id)

    try:
        product = invoice.remove_item(item_id)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    return JsonResponse({
        'message': _('Item removed'),
        'product': {
            'id': product.id,
            'stock': product.stock
        }
    })


@staff_member_required
def get_products(request):

    form = SearchProductForm(data=request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest('Invalid form')

    queryset = Product.objects.search(**form.cleaned_data)

    page = paginate(request, queryset, per_page=50)

    return JsonResponse({
        'items': render_to_string('invoices/product-items.html', {
            'page_obj': page
        }),
        'has_next': page.has_next(),
        'next_page_url': '{}?{}'.format(
            request.path, page.next_page_number().querystring)
    })


def _get_invoice(invoice_type, invoice_id):

    models = {
        'sale': Sale,
        'arrival': Arrival
    }

    try:
        model = models[invoice_type]
    except KeyError:
        raise Exception('Unknown invoice type: {}'.format(invoice_type))

    return get_object_or_404(model, pk=invoice_id)
