from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .mixins import (
    FieldsMixin, 
    FormValidMixin,
    AuthorAccessMixin,
    SuperUserMixin,
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from blog.models import Article

# Create your views here.

class ArticleList(LoginRequiredMixin,ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)

class ArticleCreate(LoginRequiredMixin,FormValidMixin,FieldsMixin,CreateView):
    model = Article
    fields = ["author", "title", "slug", "category", "description", "thumbnail", "publish", "status",]
    template_name = 'registration/article-create-update.html'

class ArticleUpdate(AuthorAccessMixin,FormValidMixin,FieldsMixin,UpdateView):
    model = Article
    fields = ["author", "title", "slug", "category", "description", "thumbnail", "publish", "status",]
    template_name = 'registration/article-create-update.html'

class ArticleDelete(SuperUserMixin,DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_confirm_delete.html'