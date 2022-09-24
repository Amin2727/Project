from django.views.generic import ListView, DetailView
from account.models import User 
from account.mixins import AuthorAccessMixin
from django.shortcuts import get_object_or_404
from .models import Article, Category
from django.db.models import Count ,Q
from datetime import datetime, timedelta


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 10

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       last_month =  datetime.today() - timedelta(days=30)
       context['popular_articles'] = Article.objects.published().annotate(
        count = Count('hits', filter=Q(articlehit__created__gt=last_month))
       ).order_by('-count', '-publish')[:1000]
       return context


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return article


class Articlepreview(AuthorAccessMixin,DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)



class CategoryList(ListView):
    paginate_by = 10
    template_name = 'blog/category_list.html'
    
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['category'] = category
       return context


class AuthorList(ListView):
    paginate_by = 10
    template_name = 'blog/author_list.html'
    
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['author'] = author
       return context


class SearchList(ListView):
    paginate_by = 10
    template_name = 'blog/search_list.html'
    
    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['search'] = self.request.GET.get('q')
       return context

