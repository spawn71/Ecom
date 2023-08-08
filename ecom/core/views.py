from django.shortcuts import render, get_object_or_404
from core.models import *
from django.db.models import Count, Avg
from core.forms import ProductReviewForm
from taggit.models import Tag
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.

def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published",featured=True)
    
    context = {
        'products':products
    }
    return render(request,'core/index.html',context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    
    context = {
        'products':products
    }
    return render(request,'core/product_list.html',context)
    

def subcategory_list_view(request):
    categories = Category.objects.all()
    
    subcategories = SubCategory.objects.all()
    # subcategories = SubCategory.objects.all().annotate(product_count=Count("product"))
    
    context ={
        'subcategories':subcategories,
        'categories':categories
    }
    return render(request, 'core/category-list.html',context)

def subcategory_product_list_view(request, scid):
    category = Category.objects.all()
    subcategory = SubCategory.objects.get(scid = scid)
    products = Product.objects.filter(product_status="published",subcategory=subcategory)
    # products = Product.objects.filter(product_status="published")
    
    context = {
        'products':products,
        'subcategory':subcategory,
        'category':category
    }
    return render(request, "core/category-product-list.html", context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors':vendors
    }
    return render(request, 'core/vendor-list.html', context)


def vendor_detail_view(request,vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor,product_status="published")
    subcategories = SubCategory.objects.all()
    context = {
        'vendor':vendor,
        'products':products,
        'subcategories':subcategories
    }
    return render(request, 'core/vendor-detail.html', context)


def product_detail_view(request,pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(subcategory=product.subcategory).exclude(pid=pid)
    
    # getting all reviews related a produtc
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    # Getting average review
    
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    # Product Review FOrm
    review_form = ProductReviewForm()
    
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_review_count > 0:
            make_review = False
            
    context = {
        'product':product,
        'p_image':p_image,
        'reviews':reviews,
        'make_review':make_review,
        'review_form':review_form,
        'average_rating':average_rating,
        'products':products
    }
    return render(request, 'core/product-detail.html',context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products":products,
        "tag":tag
    }
    return render(request, "core/tag.html", context)

def ajax_add_review(request, pid):
    product =Product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    
    context = {
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool':True,
            'context':context,
            'average_reviews':average_reviews
        }
    )


def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query,description__icontains=query).order_by("-date")
    
    context = {
        'products': products,
        'query':query,
    }
    
    return render(request, 'core/search.html', context)

def filter_product(request):
    subcategories = request.GET.getlist('subcategory[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
    if len(subcategories) > 0:
        products = products.filter(subcategory__id__in=subcategories).distinct()
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    context = {
        "products": products,
        
    }
    data = render_to_string("core/async/products-list.html",context)
    return JsonResponse({"data": data})
    

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({'data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj'])})
            

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, 'core/cart-view.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']) ,'cart_total_amount':cart_total_amount})            
    else:
        # return render(request, 'core/cart-view.html',{'cart_data':'','totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})            
        messages.warning(request,"Your cart is Empty")
        return redirect("core:index")

def delete_item_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
    context = render_to_string("core/async/cart-list.html",{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']) ,'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context,'totalcartitems':len(request.session['cart_data_obj'])})

# Update Cart List
def update_item_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
    context = render_to_string("core/async/cart-list.html",{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']) ,'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context,'totalcartitems':len(request.session['cart_data_obj'])})


@login_required
def checkout_view(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '200',
        'item_name': "Order-Item-No-3",
        'invoice': "INVOICE_NO-3",
        'currency_code': 'INR', 
        'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("core:payment-completed")),
        'cancel_url': 'http://{}{}'.format(host, reverse("core:payment-failed")),
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial = paypal_dict) 
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
           
    return render(request, 'core/checkout.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']) ,'cart_total_amount':cart_total_amount, 'paypal_payment_button':paypal_payment_button})            
    
@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'core/payment-completed.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']) ,'cart_total_amount':cart_total_amount})            

@login_required
def payment_failed_view(request):
    return render(request,"core/payment-failed.html")

@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    context ={
        'orders': orders,
    }
    return render(request,"core/customer-dashboard.html",context)