from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Article, Category, Tag, ArticleFeedback
from .forms import FeedbackForm, SearchForm

class ArticleListView(ListView):
    model = Article
    template_name = 'knowledgebase/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().filter(is_published=True)
        # Category filter
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=self.category)
        else:
            self.category = None
        # Search
        self.query = self.request.GET.get('q')
        if self.query:
            qs = qs.filter(
                Q(title__icontains=self.query) |
                Q(content__icontains=self.query) |
                Q(excerpt__icontains=self.query) |
                Q(tags__name__icontains=self.query)
            ).distinct()
        # Ordering
        order = self.request.GET.get('order')
        if order == 'popular':
            qs = qs.order_by('-views')
        elif order == 'recent':
            qs = qs.order_by('-published_at')
        else:
            qs = qs.order_by('title')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_public=True)
        context['current_category'] = getattr(self, 'category', None)
        context['search_query'] = getattr(self, 'query', '')
        context['popular_articles'] = Article.objects.filter(is_published=True).order_by('-views')[:5]
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'knowledgebase/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_published:
            obj.increment_views()
            # Log view (optional)
            ArticleView.objects.create(
                article=obj,
                user=self.request.user if self.request.user.is_authenticated else None,
                ip_address=self.request.META.get('REMOTE_ADDR'),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related articles (same category)
        context['related_articles'] = Article.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:5]
        # Feedback form
        context['feedback_form'] = FeedbackForm()
        # Check if user already gave feedback
        if self.request.user.is_authenticated:
            context['user_feedback'] = ArticleFeedback.objects.filter(
                article=self.object,
                user=self.request.user
            ).first()
        else:
            context['user_feedback'] = None
        return context


def article_feedback(request, slug):
    """
    Handle feedback (helpful / not helpful) via POST.
    """
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            helpful = form.cleaned_data['helpful']
            comment = form.cleaned_data.get('comment', '')
            # Check if user already gave feedback
            user = request.user if request.user.is_authenticated else None
            existing = ArticleFeedback.objects.filter(article=article, user=user).first()
            if existing:
                # Update existing feedback
                existing.helpful = helpful
                existing.comment = comment or existing.comment
                existing.save()
                messages.info(request, "Your feedback has been updated.")
            else:
                # Create new feedback
                feedback = ArticleFeedback(
                    article=article,
                    user=user,
                    helpful=helpful,
                    comment=comment
                )
                feedback.save()
                # Update article helpful counts
                article.record_helpful(helpful)
                messages.success(request, "Thank you for your feedback!")
            return redirect('knowledgebase:detail', slug=slug)
    return redirect('knowledgebase:detail', slug=slug)


def autocomplete_search(request):
    """
    JSON endpoint for live search suggestions.
    """
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)
    articles = Article.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query),
        is_published=True
    )[:10]
    data = [{'title': a.title, 'url': a.get_absolute_url()} for a in articles]
    return JsonResponse(data, safe=False)
