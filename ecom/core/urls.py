from django.urls import path, include
from core import views
 
app_name = 'core'

urlpatterns = [
    # HomePage
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),
    path("products/details/<pid>/", views.product_detail_view, name="product-detail"),
    
    # Category
    path("category/", views.subcategory_list_view, name="category-list"),
    path("category/<scid>/", views.subcategory_product_list_view, name="category-product-list"),
    
    # Vendor
    path("vendor/", views.vendor_list_view, name="vendor-list"),
    path("vendor/detail/<vid>", views.vendor_detail_view, name="vendor-detail"),
    
    # Tags
    path("products/tag/<slug:tag_slug>/",views.tag_list,name="tags"),
    
    
    # Reviews
    path("ajax-add-review/<int:pid>",views.ajax_add_review,name="ajax-add-review"),
    
    # search
    
    path("search/", views.search_view, name="search"),
    
    # filter
    path("filter-products/", views.filter_product, name="filter-product"),
    
    # Add to Cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    
    path("cart/",views.cart_view, name="cart"),
    path("delete-from-cart/",views.delete_item_cart, name="delete-from-cart"),
    path("update-cart/",views.update_item_cart, name="update-cart"),
    
    # Checkout page
    path("checkout/",views.checkout_view, name="checkout"),
    
    # PayPal
    path("paypal/",include("paypal.standard.ipn.urls")),
    
    # Payment Completed
    path("payment-completed/",views.payment_completed_view, name="payment-completed"),
    
    
    # Payment Failed
    
    path("payment-failed/",views.payment_failed_view, name="payment-failed"),
    
    
    # Customer Dashboard
    path("customer/",views.customer_dashboard, name="customer-dashboard"),
    
]
