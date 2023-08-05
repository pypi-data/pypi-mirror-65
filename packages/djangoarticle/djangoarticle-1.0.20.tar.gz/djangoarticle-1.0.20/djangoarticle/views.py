""" Import functions and methods. """
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
""" Import from local app. """
from .models import CategoryModelScheme, ArticleModelScheme
from .forms import CategoryFormScheme, ArticleFormScheme
""" Import from external apps. """
from djangotools.mixins import OnlyAuthorAccess
from djangocomment.models import CommentModel
from djangocomment.forms import CommentForm


""" Password protected view, Dashboard view for apptwo app. """
# ArticleListDashboard view returns the list of articles.
class ArticleListDashboard(LoginRequiredMixin, ListView):
    template_name = 'djangoadmin/djangoarticle/article_list_dashboard.html'
    context_object_name = 'article_filter'

    def get_queryset(self):
        article_filter = ArticleModelScheme.objects.author(self.request.user)
        query = self.request.GET.get("query")
        if query:
            article_match = ArticleModelScheme.objects.author(self.request.user).filter(Q(title__icontains=query))
            if article_match:
                return article_match
            else:
                return article_filter
        else:
            return article_filter
        return article_filter


""" Password protected view, manage category view for apptwo app. """
# CategoryListDashboard returns the list of category
class CategoryListDashboard(LoginRequiredMixin, ListView):
    template_name = 'djangoadmin/djangoarticle/category_list_dashboard.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        category_list = CategoryModelScheme.objects.published()
        query = self.request.GET.get("query")
        if query:
            category_match = CategoryModelScheme.objects.published().filter(Q(title__icontains=query))
            if category_match:
                return category_match
            else:
                return category_list
        else:
            return category_list
        return category_list


""" Djangoarticle Home view. """
class ArticleListView(ListView):
    template_name = 'djangoadmin/djangoarticle/article_list_view.html'
    context_object_name = 'article_filter'

    def get_queryset(self):
        return ArticleModelScheme.objects.published().filter(is_promote=False)

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['is_promoted'] = ArticleModelScheme.objects.promoted().filter(is_trend=False)
        context['is_trending'] = ArticleModelScheme.objects.trending()
        context['promo'] = ArticleModelScheme.objects.promotional()
        return context


""" Djangoarticle Category view. """
class CategoryDetailView(ListView):
    template_name = 'djangoadmin/djangoarticle/category_detail_view.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'article_filter'

    def get_queryset(self):
        page = self.request.GET.get("page")
        self.category_detail = get_object_or_404(CategoryModelScheme, slug=self.kwargs['category_slug'])
        article_filter = ArticleModelScheme.objects.filter(category=self.category_detail).filter(is_promote=False)
        article_filter = Paginator(article_filter, 4)
        return article_filter.get_page(page)

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context["category_detail"] = self.category_detail
        context['is_promoted'] = ArticleModelScheme.objects.promoted().filter(category=self.category_detail)
        context['is_trending'] = ArticleModelScheme.objects.trending().filter(category=self.category_detail)
        context['promo'] = ArticleModelScheme.objects.promotional().filter(category=self.category_detail)
        return context


""" Start a full featured ArticleDetailView for GET method. """
class ArticleDetailGetView(DetailView):
    model = ArticleModelScheme
    template_name = 'djangoadmin/djangoarticle/article_detail_view.html'
    context_object_name = 'article_detail'
    slug_url_kwarg = 'article_slug'

    def get_object(self, **kwargs):
        object = super(ArticleDetailGetView, self).get_object(**kwargs)
        object.total_views += 1
        object.save()
        return object

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailGetView, self).get_context_data(**kwargs)
        article_detail = ArticleModelScheme.objects.get(slug=self.kwargs['article_slug'])
        context["comments"] = CommentModel.objects.filter_comments_by_instance(article_detail)
        context['commentform'] = CommentForm()
        return context

class ArticleDetailFormView(FormView):
    template_name = 'djangoadmin/djangoarticle/article_detail_view.html'
    form_class = CommentForm

    def form_valid(self, form):
        article_detail = ArticleModelScheme.objects.get(slug=self.kwargs['article_slug'])
        form.instance.author = self.request.user
        form.instance.content_type = article_detail.get_for_model
        form.instance.object_id = article_detail.id 
        form.save()
        return redirect("djangoarticle:article_detail_view", article_slug=self.kwargs['article_slug'])

class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        view = ArticleDetailGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArticleDetailFormView.as_view()
        return view(request, *args, **kwargs)


""" Password protected view, category create view for apptwo app. """
class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CategoryFormScheme
    template_name = 'djangoadmin/djangoarticle/category_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    success_message = "Category created successfully."

    def get_success_message(self, cleaned_data):
        return "{0} {1}".format(cleaned_data["title"], self.success_message)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(CategoryCreateView, self).form_valid(form)

    def form_invalid(self, form):
        message = f"{form.instance.title} category not created! Please try some different keywords."
        messages.add_message(self.request, messages.WARNING, message)
        return redirect("djangoarticle:category_list_dashboard")

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['category_form'] = context['form']
        return context


""" Password protected view, category update view for apptwo app. """
class CategoryUpdateView(LoginRequiredMixin, OnlyAuthorAccess, SuccessMessageMixin, UpdateView):
    model = CategoryModelScheme
    form_class = CategoryFormScheme
    template_name = 'djangoadmin/djangoarticle/category_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    slug_url_kwarg = 'category_slug'
    success_message = "Category updated successfully."

    def get_success_message(self, cleaned_data):
        return "{} {}".format(cleaned_data["title"], self.success_message)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(CategoryUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        message = f"Sorry! {form.instance.title} category not updated."
        messages.add_message(self.request, messages.WARNING, message)
        return redirect("djangoarticle:category_list_dashboard")

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['category_form'] = context['form']
        return context


""" Password protected view, category delete view for apptwo app. """
class CategoryDeleteView(LoginRequiredMixin, OnlyAuthorAccess, DeleteView):
    model = CategoryModelScheme
    context_object_name = 'category_detail'
    template_name = 'djangoadmin/djangoarticle/category_delete_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    slug_url_kwarg = 'category_slug'
    success_message = "category deleted successfully."

    def delete(self, request, *args, **kwargs):
        message = f"{kwargs['category_slug']} {self.success_message}"
        messages.add_message(self.request, messages.WARNING, message)
        return super(CategoryDeleteView, self).delete(request, *args, **kwargs)


""" Password protected view, article create view for apptwo app. """
class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ArticleFormScheme
    template_name = 'djangoadmin/djangoarticle/article_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    success_message = "article created successfully."

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data['title']} {self.success_message}"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(ArticleCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['article_form'] = context['form']
        return context


""" Password protected view, article update view for apptwo app. """
class ArticleUpdateView(LoginRequiredMixin, OnlyAuthorAccess, SuccessMessageMixin, UpdateView):
    model = ArticleModelScheme
    form_class = ArticleFormScheme
    template_name = 'djangoadmin/djangoarticle/article_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    slug_url_kwarg = 'article_slug'
    success_message = "article updated successfully."

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data['title']} {self.success_message}"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(ArticleUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        context['article_form'] = context['form']
        return context


""" Password protected view, article delete view for apptwo app. """
class ArticleDeleteView(LoginRequiredMixin, OnlyAuthorAccess, DeleteView):
    model = ArticleModelScheme
    context_object_name = 'article_detail'
    template_name = 'djangoadmin/djangoarticle/article_delete_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    slug_url_kwarg = 'article_slug'
    success_message = "article deleted successfully."

    def delete(self, request, *args, **kwargs):
        message = f"{kwargs['article_slug']} {self.success_message}."
        messages.warning(self.request, message)
        return super(ArticleDeleteView, self).delete(request, *args, **kwargs)
