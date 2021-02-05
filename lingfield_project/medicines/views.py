from django.shortcuts import render
from .models import  Category, Medicine
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.db.models import Q

# Create your views here.
class MedicineDetailView(DetailView):
    model = Medicine
    template_name = "medicines/medicine-detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MedicineDetailView, self).get_context_data(*args, **kwargs)
        context['medicine_list'] = Category.objects.all()
        return context

class MedicineListView(ListView):
    model = Medicine
    template_name = "medicines/medicine-list.html"


class SearchResultsView(ListView):
    model = Medicine
    template_name = 'medicines/search.html'
   
    def get_queryset(self): # new
        query = self.request.GET.get('q_medicines')
        object_list = Medicine.objects.filter(
            Q(title__icontains=query) 
        )
        return object_list

class CategoryDetailView(DetailView,MultipleObjectMixin):
    model = Category
    template_name = "medicines/medicine-category-detail.html"

    def get_context_data(self, **kwargs):
        object_list = Medicine.objects.filter(category=self.get_object())
        context = super(CategoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context
 

def medicine_category_list(request):
    context = {'categories':Category.objects.all()}
    return render(request, 'medicines/medicine-category-list.html',context)

