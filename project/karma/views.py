from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import *
from django.db.models import Sum,F
from django.http import Http404,HttpResponseRedirect,HttpResponse

# Create your views here.


def base(request):
    return render(request, 'karma/base.html')


def index(request):
    last_product = Product.objects.order_by('-date')[:8]
    best_product = Product.objects.filter(popular__gte = 1000)[:8]
    context = {
        'last_product': last_product,
        'best_product': best_product
    }
    return render(request, 'karma/index.html', context)

def blog(request):
    return render(request, 'karma/blog.html')


def category_detail(request):
    return render(request, 'karma/category_detail.html')

def checkout(request):
    return render(request, 'karma/checkout.html')

def confirmation(request):
    return render(request, 'karma/confirmation.html')

def contact(request):
    return render(request, 'karma/contact.html')

def elements(request):
    return render(request, 'karma/elements.html')

def single_blog(request):
    return render(request, 'karma/single-blog.html')


def tracking(request):
    return render(request, 'karma/tracking.html')


# Profile


def profile(request):
    return render(request, 'karma/profile.html')


def update_profile(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            profile = request.user.profile
            profile.phone = request.POST.get('phone')
            profile.address = request.POST.get('address')
            profile.save()
        return redirect('profile')
    return redirect('home')


#  Register =============


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            profile = Profile()
            profile.user = request.user
            profile.save()
            # log the user in
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'karma/register.html', {'form': form})

def product_detail(request, slug):
    product_detail = Product.objects.get(slug=slug)
    product_detail.popular += 1
    product_detail.save()
    context = {
        'product_detail': product_detail

    }
    return render(request, 'karma/single-product.html', context)


#  Add to Cart
def add_to_cart(request):
    product_slug = request.GET.get("id")
    product = Product.objects.get(id=product_slug)
    if request.user.is_authenticated:
        if request.method == 'GET':
            if not request.user.cartitem_set.filter(product=product).exists():
                item = CartItem()
                item.product = product
                item.user = request.user
                item.count = request.GET.get('qty')
                item.save()
            else:
                item = request.user.cartitem_set.get(product=product)
                item.count += int(request.GET.get('qty'))
                item.save()
                print(item)
            return HttpResponse('Done')
        return HttpResponse('Unexpected method')
    return HttpResponse('Authenticated user is null')



def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = CartItem.objects.annotate(
        item_price=F("count")* F("product__price")
    ).aggregate(Sum("item_price")).get("item_price__sum",0)

    context = {
        'cart_items':cart_items,
        'total_amount':total_amount

    }
    return render(request,'karma/cart.html',context)

def update_cart(request,item_id):
    item = CartItem.objects.get(id=item_id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            item.count = request.POST.get('count')
            item.save()
            if int(item.count) < 1 :
                item.delete()
            return redirect('cart')
        return HttpResponse('Unexpected method')
    return HttpResponse('Authenticated user is null')




def delete_cart(request, item_id):
    item = CartItem.objects.get(id=item_id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            item.delete()
            return redirect('cart')
        return HttpResponse('Unexpected method')
    return HttpResponse('Authenticated user is null')


def order(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            order = Order()
            order.user = request.user
            order.order_status = OrderStatus.objects.get(system_name__exact='new')
            order.payment_type = PaymentType.objects.get(system_name__exact=request.POST.get('payment_type'))
            order.save()
            items = CartItem.objects.filter(user=request.user)

            for item in items:
                order_product = Orderproduct()
                order_product.order = order
                order_product.product = item.product
                order_product.count = item.count
                order_product.product_price = item.product.price
                order_product.product_name = item.product.title
                order_product.save()
            if order.payment_type.system_name == 'payme':
                pass
            return redirect('cart')
        return HttpResponse('Unexpected method')
    return HttpResponse('Authenticated user is null')

# Orders =================

def orders(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:

            orders = Order.objects.order_by('-date')
            order_statuses = OrderStatus.objects.all()
            return render(request, 'karma/orders.html', {'orders': orders, 'order_statuses': order_statuses})
    return redirect('home')

    
def change_status(request, order_id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            order = Order.objects.get(id=order_id)
            order.order_status = OrderStatus.objects.get(id=request.POST.get('order_status'))
            order.save()
            return redirect('orders')
    return redirect('home')