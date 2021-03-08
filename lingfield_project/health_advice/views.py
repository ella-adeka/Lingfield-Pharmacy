from django.shortcuts import render,get_object_or_404
from .models import HealthAdvice, Category
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.db.models import Q

# Create your views here.
class HealthAdviceDetailView(DetailView):
    model = HealthAdvice
    template_name = "health_advice/health-advice-detail.html"

    def get_context_data(self, *args, **kwargs):
        # Get all details of a specific category(A, B, C, E...) when clicked and returns it.
        context = super(HealthAdviceDetailView, self).get_context_data(*args, **kwargs)
        context['health_advice_list'] = Category.objects.all()
        return context

class HealthAdviceListView(ListView):
    model = HealthAdvice
    template_name = "health_advice/health-advice-list.html"
    
class CategoryListView(ListView):
    # List all the categories.
    model = HealthAdvice
    template_name = "health_advice/health-advice-category-list.html"
    

class SearchResultsView(ListView):
    model = HealthAdvice
    template_name = 'health_advice/search.html'
   
    def get_queryset(self): # new
        query = self.request.GET.get('q_health_advice')
        object_list = HealthAdvice.objects.filter(
            Q(title__icontains=query) 
        )
        return object_list

class CategoryDetailView(DetailView,MultipleObjectMixin):
    model = Category
    template_name = "health_advice/Health-advice-category-detail.html"

    def get_context_data(self, **kwargs):
        object_list = HealthAdvice.objects.filter(category=self.get_object())
        context = super(CategoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context
 
# ----------------- HEALTH ADVICE   -----------------------#
def health_advice_category_list(request):
    context = {'categories':Category.objects.all()}
    return render(request, 'health_advice/health-advice-category-list.html', context)

def health_advice_category_detail(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    healthadvices = HealthAdvice.objects.filter(category__slug=category_slug)
    context = {'category':category,'healthadvices': healthadvices}
    return render(request, 'health_advice/health-advice-category-detail.html', context)


def health_advice_list(request):
    healthadvices = get_object_or_404(HealthAdvice).order_by('categories')
    context = {'healthadvices': healthadvices}
    return render(request, 'health_advice/health-advice-list.html', context)

def health_advice_detail(request,pk):
    categories = Category.objects.filter()
    healthadvices = get_object_or_404(HealthAdvice, pk=pk)
    return render(request, 'health_advice/health-advice-detail.html', {'healthadvices':healthadvices, 'categories':categories})

