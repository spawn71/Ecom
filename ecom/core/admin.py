from django.contrib import admin
from core.models import *
# Register your models here.

class ProductImageAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = [
        'user','title', 'product_image', 'price','category', 'subcategory','vendor' ,'featured','product_status'
    ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category_image'
    ]

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'subcategory_image'
    ]

class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'vendor_image'
    ]
    
class CartOrderAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'price', 'paid_status','order_date','product_status'
    ]
    
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'invoice_no','items','image','qty','price','total'
    ]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'product','review','rating'
    ]
class WhishlistAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'product','date'
    ]

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'name','phone','address','locality','pincode','city','status'
    ]
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Whishlist,WhishlistAdmin)
admin.site.register(Address,AddressAdmin)
