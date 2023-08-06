
from django.urls import path

from invoices import views


app_name = 'invoices'


urlpatterns = [

    path('<str:invoice_type>/<int:invoice_id>/',
         views.manage_invoice,
         name='manage'),

    path('<str:invoice_type>/<int:invoice_id>/add-item/',
         views.add_item,
         name='add-item'),

    path('<str:invoice_type>/<int:invoice_id>/print/',
         views.add_item,
         name='print'),

    path('<str:invoice_type>/<int:invoice_id>/set-item-qty/<int:item_id>/',
         views.set_item_qty,
         name='set-item-qty'),

    path('<str:invoice_type>/<int:invoice_id>/remove-item/<int:item_id>/',
         views.remove_item,
         name='remove-item'),

    path('products/', views.get_products, name='products')

]
