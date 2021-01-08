from django.shortcuts import render, get_object_or_404
from .models import HealthNews, Category
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.db.models import Q
from django.views.generic.dates import DayArchiveView
# Create your views here.
# class HealthNewsDetailView(DetailView):
#     model = HealthNews
#     template_name = "health_news/health-news-detail.html"
#     def get_context_data(self, *args, **kwargs):
#         context = super(HealthNewsDetailView, self).get_context_data(*args, **kwargs)
#         context['health_news_list'] = Category.objects.all()
#         return context

class HealthNewsListView(ListView):
    template_name = "health_news/health-news-list.html"

    

class SearchResultsView(ListView):
    model = HealthNews
    template_name = 'health_news/search.html'
   
    def get_queryset(self): # new
        query = self.request.GET.get('q_health_news')
        object_list = HealthNews.objects.filter(
            Q(title__icontains=query) 
        )
        return object_list

class HealthNewsDayArchiveView(DayArchiveView):
    queryset = HealthNews.objects.all()
    date_field = "created_at"
    allow_future = True

#   ------------------- HEALTH NEWS ------------------------#
def health_news_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    healthnews = HealthNews.objects.all()
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        healthnews = healthnews.filter(category=category)
    context = {'categories':categories,'category':category,'healthnews': healthnews}
    return render(request, 'health_news/health-news-list.html', context)


def health_news_detail(request,id):
    healthnews = get_object_or_404(HealthNews, id=id)
    return render(request, 'health_news/health-news-detail.html', {'healthnews':healthnews})

