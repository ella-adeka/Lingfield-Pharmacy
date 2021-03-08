from django.shortcuts import render,get_object_or_404, redirect
from .models import Shop, Category, SubCategory, Order, OrderItem, Payment
from .forms import *
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from accounts.forms import *
from accounts.models import *

# Create your views here.
#               -----------------------------------------------     FUNCTIONS    ------------------------------------------             #

def get_subcategory(request):
    id = request.GET.get('id', '')
    result = list(SubCategory.objects.filter(
    category_id=int(id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_item_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        items = Shop.object.filter(
           Q(title__icontains=q),
            Q(text__icontains=q)
        ).distinct()

        for item in items:
            queryset.append(item)
    return list(set(queryset))

#               -----------------------------------------------    END OF FUNCTIONS    ------------------------------------------             #

#               -----------------------------------------------     CLASS-BASED VIEWS     ----------------------------------------              #
class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            page_title = 'Cart'
            context = {
                'object': order,
                'page_title': page_title,
                
            }
            return render(self.request, 'shopping/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("shopping:product_list")

class CheckOutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            payment_form = PaymentForm()
            delivery_form = CheckOutDelivery()
            u_form = UpdateForm(instance=self.request.user)
            b_form = UserBirthDateForm(instance=self.request.user.userbirthdate)
            p_form = UserProfileForm(instance=self.request.user.userprofile)
            context = {
                'order' : order,  
                'payment_form' : payment_form, 
                'delivery_form' : delivery_form,
                'u_form' : u_form,
                'b_form' : b_form,
                'p_form' : p_form, 
            }
            return render(self.request, "shopping/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info("You do not have an active order.")
            return redirect("shopping:checkout")

    def post(self, *args, **kwargs):
        payment_form = PaymentForm(self.request.POST or None)
        delivery_form = CheckOutDelivery(self.request.POST or None)
        u_form = UpdateForm(request.POST,instance=request.user)
        b_form = UserBirthDateForm(request.POST, request.FILES, instance=request.user.userbirthdate)
        p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if u_form.is_valid() and b_form.is_valid() and p_form.is_valid() and payment_form.is_valid() and delivery_form.is_valid():
                u_form.save()
                b_form.save()
                p_form.save()
                payment_form.save()
                delivery_form.save()
            else:
                u_form = UpdateForm(instance=request.user)
                b_form = UserBirthDateForm(instance=request.user.userbirthdate)
                p_form = UserProfileForm(instance=request.user.userprofile)
            return redirect("shopping:checkout")
        except ObjectDoesNotExist:
            messages.info("You do not have an active order.")
            return redirect("shopping:cart")
    
    

class SearchResultsView(ListView):
    model = Shop
    template_name = 'shopping/search.html'
   
    def get_queryset(self): # new
        query = self.request.GET.get('q_shop_product')
        object_list = Shop.objects.filter(
            Q(title__icontains=query) 
        )
        return object_list

class ShopDetailView(DetailView):
    model = Shop
    template_name = "shopping/product_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ShopDetailView, self).get_context_data(*args, **kwargs)
        context['product_list'] = Category.objects.all()
        return context

class ShopListView(ListView):
    template_name = "shopping/product_list.html"

#               -----------------------------------------------   END OF CLASS-BASED VIEWS     ----------------------------------------              #


# Create your views here.
@login_required
def delivery(request):
    return render(request, 'shopping/delivery.html')

@login_required
def payment(request):
    return render(request, 'shopping/payment.html')

def product_list(request, category_slug=None, subcategory_slug=None):
    category = None
    subcategory = None

    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(category=category)

    shop = Shop.objects.all()
    if subcategory_slug:
        # 1 SubCategory = Many Shop not Many SubCategories = 1 Shop
        # Only post the shop in a specific subcategory
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        shop = shop.filter(subcategory=subcategory)
    context = {'categories':categories, 'category':category,'subcategories':subcategories,'subcategory':subcategory, 'shop': shop}
    return render(request, 'shopping/product_list.html', context)

def product_detail(request,id):
    shop = get_object_or_404(Shop, id=id)
    context = {'shop':shop}
    return render(request, 'shopping/product_detail.html',context)




#       --------------------------------    CARTING SYSTEMS ( ADD & REMOVE FROM CART )      ---------------------------------------------       #
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Shop,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        user = request.user,
        item=item,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.item_quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shopping:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shopping:cart")
    else:
        date_ordered = timezone.now()
        order = Order.objects.create(
            user=request.user, 
            date_ordered=date_ordered
        )
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shopping:cart")

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Shop, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("shopping:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shopping:product_detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shopping:product_detail", slug=slug)

@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Shop, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.item_quantity > 1:
                order_item.item_quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("shopping:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shopping:product_list", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shopping:product_list", slug=slug)

#       --------------------------------  END OF CARTING SYSTEMS ( ADD & REMOVE FROM CART )      ---------------------------------------------       #

