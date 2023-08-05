""" Import functions and methods. """
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
""" Import from local apps. """
from djangopost.models import CategoryModel
from djangopost.models import ArticleModel
from djangopost.forms import CategoryForm
from djangopost.forms import ArticleForm
""" Import from External apps. """
from djangotools.decorators import OnlyAuthorAccess
from djangocomment.models import CommentModel
from djangocomment.forms import CommentForm


""" password protected view, Dashboard view for appone app. """
# ArticleListDashboard returns the list of articles associated with registred admin user.
@login_required()
def ArticleListDashboard(request):
    template_name = 'djangoadmin/djangopost/article_list_dashboard.html'
    article_filter = ArticleModel.objects.author(request.user)
    query = request.GET.get("query")
    if query:
        match = ArticleModel.objects.author(request.user).filter(Q(title__icontains=query))
        if match:
            message = f"Search Results for: {query}."
            messages.add_message(request, messages.SUCCESS, message)
            context = {"article_filter": match}
            return render(request, template_name, context)
        else:
            message = "Nothing matched! Please try again with some different keywords."
            messages.add_message(request, messages.WARNING, message)
            return redirect("djangopost:article_list_dashboard")
    context = {'article_filter': article_filter}
    return render(request, template_name, context)


""" password protected view, Dashboard view for managing categories. """
# CategoryListDashboard returns the list of categories.
@login_required()
def CategoryListDashboard(request):
    template_name = 'djangoadmin/djangopost/category_list_dashboard.html'
    category_list = CategoryModel.objects.published()
    query = request.GET.get("query")
    if query:
        match = CategoryModel.objects.published().filter(Q(title__icontains=query))
        if match:
            message = f"Search Results for: {query}."
            messages.success(request, message)
            context = {"category_list": match}
            return render(request, template_name, context)
        else:
            message = "Nothing matched! Please try again with some different keywords."
            messages.warning(request, message)
            return redirect("djangopost:category_list_dashboard")
    context = {'category_list': category_list}
    return render(request, template_name, context)


# Create your home views here.
def ArticleListView(request):
    template_name = 'djangoadmin/djangopost/article_list_view.html'
    category_filter = CategoryModel.objects.published()
    article_filter = ArticleModel.objects.published().filter(is_promote=False)
    is_promoted = ArticleModel.objects.promoted().filter(is_trend=False)
    is_trending = ArticleModel.objects.trending()
    promo = ArticleModel.objects.promotional()
    context = { 'category_filter': category_filter, 'article_filter': article_filter,
                'is_promoted': is_promoted, 'is_trending': is_trending, 'promo': promo }
    return render(request, template_name, context)


# Create your category view here
def CategoryDetailView(request, category_slug):
    template_name = 'djangoadmin/djangopost/category_detail_view.html'
    page = request.GET.get("page")
    category_detail = CategoryModel.objects.get(slug=category_slug)
    article_filter = ArticleModel.objects.filter(category=category_detail).filter(is_promote=False)
    article_filter = Paginator(article_filter, 4)
    article_filter = article_filter.get_page(page)
    is_promoted = ArticleModel.objects.promoted().filter(category=category_detail)
    is_trending = ArticleModel.objects.trending().filter(category=category_detail)
    promo = ArticleModel.objects.promotional().filter(category=category_detail)
    context = {'category_detail': category_detail, 'article_filter': article_filter, 'is_promoted': is_promoted, 'is_trending': is_trending, "promo": promo}
    return render(request, template_name, context)


# Create your article view here
def ArticleDetailView(request, article_slug):
    template_name = 'djangoadmin/djangopost/article_detail_view.html'
    article_detail = ArticleModel.objects.get(slug=article_slug)
    comments = CommentModel.objects.filter_comments_by_instance(article_detail)
    if request.method == "POST":
        commentform = CommentForm(request.POST or None)
        if commentform.is_valid():
            instance = commentform.save(commit=False)
            instance.author = request.user
            instance.content_type = article_detail.get_for_model
            instance.object_id = article_detail.id 
            instance.save()
        return redirect("djangopost:article_detail_view", article_slug = article_slug)
    else:
        commentform = CommentForm()
        context = {'article_detail': article_detail, 'comments': comments, 'commentform': commentform}
        return render(request, template_name, context)


""" password protected view, create new category. """
# CategoryCreateView is here, Login required.
@login_required()
def CategoryCreateView(request):
    template_name = 'djangoadmin/djangopost/category_create_view_form.html'
    if request.method == 'POST':
        categoryform = CategoryForm(request.POST or None)
        if categoryform.is_valid():
            instance = categoryform.save(commit=False)
            instance.author = request.user
            instance.save()
            # Without this next line the tags won't be saved.
            categoryform.save_m2m()
            message = f"{categoryform.cleaned_data['title']} category created successfully."
            messages.success(request, message)
            return redirect('djangopost:category_list_dashboard')
        else:
            message = f"{request.POST['title']} category not created! Please try some different keywords."
            messages.warning(request, message)
            return redirect('djangopost:category_create_view')
    else:
        categoryform = CategoryForm()
        context = { 'category_form': categoryform }
        return render(request, template_name, context)


""" password protected view, update any existting category. """
# CategoryUpdateView is here, Login required.
@OnlyAuthorAccess(CategoryModel)
@login_required()
def CategoryUpdateView(request, category_slug):
    template_name = 'djangoadmin/djangopost/category_create_view_form.html'
    category_detail = CategoryModel.objects.get(slug=category_slug)
    if request.method == 'POST':
        categoryform  = CategoryForm(request.POST or None, instance=category_detail)
        if categoryform.is_valid():
            categoryform.save()
            message = f"{categoryform.cleaned_data.get('title')} category updated successfully."
            messages.success(request, message)
            return redirect('djangopost:category_list_dashboard')
        else:
            message = f"Sorry! {request.POST['title']} category not updated."
            messages.warning(request, message)
            return redirect('djangopost:category_list_dashboard')
    else:
        categoryform = CategoryForm(instance=category_detail)
        context = { 'category_form': categoryform }
        return render(request, template_name, context)


""" password protected view, category category. """
# CategoryDeleteView is here, Login required.
@OnlyAuthorAccess(CategoryModel)
@login_required()
def CategoryDeleteView(request, category_slug):
    template_name = 'djangoadmin/djangopost/category_delete_view_form.html'
    category_detail = CategoryModel.objects.get(slug=category_slug)
    if request.method == 'POST':
        category_detail.delete()
        message = f"{category_detail.title} category deleted successfully."
        messages.success(request, message)
        return redirect('djangopost:category_list_dashboard')
    else:
        context = {'category_detail': category_detail }
        return render(request, template_name, context)


""" password protected view, create article view. """
# ArticleCreateView is here, Login required.
@login_required()
def ArticleCreateView(request):
    template_name = 'djangoadmin/djangopost/article_create_view_form.html'
    if request.method == 'POST':
        articleform = ArticleForm(request.POST or None, request.FILES or None)
        if articleform.is_valid():
            instance = articleform.save(commit=False)
            instance.author = request.user
            instance.save()
            message = f"{articleform.cleaned_data['title']} article created successfully."
            messages.success(request, message)
            return redirect('djangopost:article_list_dashboard')
        else:
            message = f"{request.POST['title']} article not created! Please try some different keywords."
            messages.warning(request, message)
            return redirect('djangopost:article_create_view')
    else:
        articleform = ArticleForm()
        context = {'article_form': articleform}
        return render(request, template_name, context)


""" password protected view, update any existting article. """
# ArticleUpdateView is here, Login required.
@OnlyAuthorAccess(ArticleModel)
@login_required()
def ArticleUpdateView(request, article_slug):
    template_name = 'djangoadmin/djangopost/article_create_view_form.html'
    article_detail = ArticleModel.objects.get(slug=article_slug)
    if request.method == 'POST':
        articleform  = ArticleForm(request.POST or None, request.FILES or None, instance=article_detail)
        if articleform.is_valid():
            instance = articleform.save(commit=False)
            instance.author = request.user
            instance.save()
            message = f"{articleform.cleaned_data['title']} article updated successfully."
            messages.success(request, message)
            return redirect('djangopost:article_list_dashboard')
        else:
            message = f"{request.POST['title']} article not updated! Please try some different keywords."
            messages.warning(request, message)
            return redirect('djangopost:article_list_dashboard')
    else:
        articleform = ArticleForm(instance=article_detail)
        context = { 'article_form': articleform }
        return render(request, template_name, context)


""" password protected view, article delete view. """
# ArticleDeleteView is here, Login required.
@OnlyAuthorAccess(ArticleModel)
@login_required()
def ArticleDeleteView(request, article_slug):
    template_name = 'djangoadmin/djangopost/article_delete_view_form.html'
    article_detail = ArticleModel.objects.get(slug=article_slug)
    if request.method == 'POST':
        article_detail.delete()
        message = f"{article_detail.title} article deleted successfully."
        messages.success(request, message)
        return redirect('djangopost:article_list_dashboard')
    else:
        context = {'article_detail': article_detail }
        return render(request, template_name, context)
