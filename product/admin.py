from django.contrib import admin
from .models import Product, ProductImages, Category, Comment
from django.utils.html import format_html
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 1  # Number of extra forms to display


class ProductAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius:10px;" />'.format(object.product_photo.url))

    thumbnail.short_description = 'Product Photo'

    list_display = ('id', 'thumbnail', 'name', 'product_sequence', 'short_text', 'unit_price', 'last_modified', 'create_date', 'category_id', 'create_by')
    list_display_links = ('id', 'name', 'short_text')
    # list_editable = ('publish_status',)
    search_fields = ('id', 'name', 'short_text', 'product_sequence', 'create_date', 'category_id', 'create_by')
    list_filter = ('category_id', 'create_by', 'publish_status')
    inlines = [ProductImageInline]

    fieldsets = [
        ('Standard info', {
            'fields': ['name', 'product_sequence']
        }),
        ('Product Details', {
            'fields': ['short_text', 'description', 'unit_price', 'category_id',
                       'manufacturer_name', 'manufacturer_brand','product_stock', 'cost_price',
                        ],
            'classes': ['wide',],
            'description': 'Enter the main details of the model.',
        }),
        ('Other Details', {
            'fields': ['publish_status', 'visibility','last_published_date_time', 'create_by']
        }),
        ('Product Image', {
            'fields': ['product_photo']
        })
    ]

class ProductImagesAdmin(admin.ModelAdmin):

    list_display = ('product',)
    search_fields = ('product',)
    list_filter = ('product',)



class CategoryAdmin(admin.ModelAdmin):

    # def thumbnail(self, object):
    #     return format_html('<img src="{}" width="40" style="border-radius:10px;" />'.format(object.cat_photo.url))
    #
    # thumbnail.short_description = 'Category Photo'

    list_display = ('id', 'name', 'description', 'last_modified', 'create_date')
    list_display_links = ('id', 'name')
    # list_editable = ('is_featured',)
    search_fields = ('id', 'name', 'description', 'create_date')
    list_filter = ('create_date',)





admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)

