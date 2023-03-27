from django.contrib import admin,messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.http import HttpRequest
from . import models
from django.urls import reverse

# Register your models here.



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug':['title']
    }
    actions = ['clear_invertory']
    list_display = ['title','unit_price','inventory','inventery_status','collection']
    list_editable = ['unit_price']
    list_per_page = 200
    list_filter = ['last_update','collection']
    search_fields = ['product']
    @admin.display(ordering='inventory')
    def inventery_status(self,product)->str:
        if product.inventory<10:
            return 'Low'
        return 'Ok'
    
    @admin.action(description='Clear Invertory')
    def clear_invertory(self, request,queryset):
        update_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{update_count} products were successfully updated',
            messages.ERROR)
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = (reverse('admin:store_product_changelist')
               + '?'+
               urlencode({
                   'collection_id':str(collection.id)
               }))
        return format_html('<a href= "{}">{}</a>',url,collection.products_count)
        
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','membership_choice', 'orders']
    list_editable = ['membership_choice']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 5
    model = models.OrderItem
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    ordering = ['id','Payment_status','customer']
    list_per_page = 10