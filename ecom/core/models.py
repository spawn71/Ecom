from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


STATUS_CHOICE = (
    ("process","Processing"),
    ("shipped","Shipped"),
    ("deliverd","Deliverd"),
)

STATUS = (
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("in_review","In_Review"),
    ("published","Published"),
)

RATING = (
    (1,"★✰✰✰✰"),
    (2,"★★✰✰✰"),
    (3,"★★★✰✰"),
    (4,"★★★★✰"),
    (5,"★★★★★"),
)

# INACTIVE = 0
# ACTIVE = 1
# STATUS = (
#     (INACTIVE, ('Inactive')),
#     (ACTIVE, ('Active')),
# )



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    
    
    cid = ShortUUIDField(unique=True, length= 10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")
    # category_status = models.IntegerField(default=0, choices=STATUS)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50px" height="50"  />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    
    scid = ShortUUIDField(unique=True, length= 10, max_length=20, prefix="scat", alphabet="abcdefgh12345")
    
    Category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    
    title = models.CharField(max_length=100, default="Foood")
    image = models.ImageField(upload_to="sub_category", default="subcategory.png")
    # sub_category_status = models.IntegerField(default=0, choices=STATUS)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "SubCategories"
    
    def subcategory_image(self):
        return mark_safe('<img src="%s" width="50px" height="50"  />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Tags(models.Model):
    pass

class Vendor(models.Model):
    
    vid = ShortUUIDField(unique=True, length= 10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Gorffers")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    # description = models.TextField(null=True, blank=True, default="I am Fast delivery Vendor")
    description = RichTextUploadingField(null=True, blank=True, default="I am Fast delivery Vendor")
    
    address = models.CharField(max_length=100,default="123 Main Street")
    phone = models.CharField(max_length=100, default="+91 888-888-8888")
    # vendor_status = models.IntegerField(default=0, choices=STATUS)
    
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vendors"
    
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50px" height="50"  />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Product(models.Model):
    
    pid = ShortUUIDField(unique=True, length= 10, max_length=20, prefix="prd", alphabet="abcdefgh12345")
    
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True ,related_name="subcategory")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="product")
    
    title = models.CharField(max_length=100, default="Fresh Apple")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="This is Product")
    description = RichTextUploadingField(null=True, blank=True, default="This is Product")
    
    price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="12.99")
    old_price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="22.99")
    
    # specifiaction = models.TextField(null=True, blank=True)
    specifiaction = RichTextUploadingField(null=True, blank=True)
    
    type = models.CharField(max_length=100, default="Organic", null=True, blank=True)
    stock_conut = models.CharField(max_length=100, default="10", null=True, blank=True)
    life = models.CharField(max_length=100, default="100", null=True, blank=True)
    waranty = models.CharField(max_length=100, default="100", null=True, blank=True)
    
    mfd = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    tags = TaggableManager(blank=True)
    
    product_status = models.CharField(default="in_review", choices=STATUS, max_length=10)
    
    status = models.BooleanField(default=True)
    
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length= 4, max_length=10, prefix="sku", alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Products"
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50px" height="50"  />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        disc = new_price-100
        return disc
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="products.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="p_images")
    date= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"
    


# ================================Cart Order, OderItems and Address==================================#
# ================================Cart Order, OderItems and Address==================================#
# ================================Cart Order, OderItems and Address==================================#
# ================================Cart Order, OderItems and Address==================================#

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="12.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(default="processing", choices=STATUS_CHOICE, max_length=30)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Cart Orders"
    
    
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    items = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="12.99")
    total = models.DecimalField(max_digits=99999999999, decimal_places=2, default="12.99")
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50px" height="50"  />' % (self.image.url))
    
    


# ================================Product Review, Whishlist, Address ==================================#
# ================================Product Review, Whishlist, Address ==================================#
# ================================Product Review, Whishlist, Address ==================================#
# ================================Product Review, Whishlist, Address ==================================#

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = RichTextUploadingField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
   
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class Whishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Whishlists"
   
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    locality = models.CharField(max_length=100,null=True)
    pincode = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=100,null=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Address"