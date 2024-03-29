from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.contrib.contenttypes.admin import GenericTabularInline
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models.query import QuerySet
from store import models
from tags import models as tags_models


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            queryset.filter(inventory__lt=10)

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = tags_models.TaggedItem

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.file.name != '':
            return format_html(f'<img src="{instance.file.url}" class="thumbnail" />')
        return ''


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return product.inventory
        
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            messages.SUCCESS
        )

    # media klass orqali barcha yerga styles.css ni ishlatadigan qilish
    class Media:
        css = {
            'all': ['store/styles.css']
        }



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        return customer.orders_count
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )

# admin.site.register(models.Customer)
admin.site.register(models.Promotion)
admin.site.register(models.OrderItem)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Address)
admin.site.register(models.Review)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )

class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
