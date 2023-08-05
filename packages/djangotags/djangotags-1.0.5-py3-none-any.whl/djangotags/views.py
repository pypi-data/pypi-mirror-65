from itertools import chain
from django.views.generic import DetailView
""" Import from External Apps. """
from taggit.models import Tag
from djangopost.models import ArticleModel
from djangoarticle.models import ArticleModelScheme


# Create your homepage views here.
class TaggitTagDetailView(DetailView):
    template_name = "djangoadmin/djangotags/taggit_tag_detail_view.html"
    model = Tag
    slug_url_kwarg = "tag_slug"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Access for tag conent.
        lookup_instance = self.kwargs['tag_slug']
        context['article_filter'] = ArticleModel.objects.published().filter(tags__slug=lookup_instance)[0:4]
        context['is_promoted'] = ArticleModelScheme.objects.published().filter(tags__slug=lookup_instance)[0:4]
        # Access for promotional content.
        post_promo = ArticleModel.objects.promotional()[0:3]
        article_promo = ArticleModelScheme.objects.promotional()[0:3]
        context['promo'] = chain(post_promo, article_promo)
        # Access for trending content.
        post_trending = ArticleModel.objects.trending()[0:2]
        article_trending = ArticleModelScheme.objects.trending()[0:2]
        context['is_trending'] = chain(post_trending, article_trending)
        # return for templating.
        return context
