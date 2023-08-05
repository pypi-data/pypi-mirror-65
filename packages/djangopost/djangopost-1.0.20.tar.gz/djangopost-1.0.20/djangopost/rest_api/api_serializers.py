from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
from djangopost.models import CategoryModel
from djangopost.models import ArticleModel


""" CategorySerializer. """
class CategorySerializer(ModelSerializer):
    api_detail_url = HyperlinkedIdentityField(
        view_name = "djangopost:category_retrieve_viewset",
        lookup_field = "slug"
    )

    api_published_article_list_url = HyperlinkedIdentityField(
        view_name = "djangopost:category_detail_article_list_viewset",
        lookup_field = "slug",
        lookup_url_kwarg = "slug"
    )

    api_update_url = HyperlinkedIdentityField(
        view_name = "djangopost:category_update_viewset",
        lookup_field = "slug"
    )

    api_delete_url = HyperlinkedIdentityField(
        view_name = "djangopost:category_destroy_viewset",
        lookup_field = "slug"
    )

    detail_url = HyperlinkedIdentityField(
        view_name = "djangopost:category_detail_view",
        lookup_field = "slug",
        lookup_url_kwarg = "category_slug"
    )

    class Meta:
        model = CategoryModel
        fields = ['serial', 'title', 'slug', 'description', 'author', 'status', 'verification',
                  'created_at', 'updated_at', 'api_detail_url', 'api_published_article_list_url',
                  'api_update_url', 'api_delete_url', 'detail_url']


""" ArticleSerializer. """
class ArticleSerializer(ModelSerializer):
    api_detail_url = HyperlinkedIdentityField(
        view_name = "djangopost:article_retrieve_viewset",
        lookup_field = "slug"
    )

    api_update_url = HyperlinkedIdentityField(
        view_name = "djangopost:article_update_viewset",
        lookup_field = "slug"
    )

    api_delete_url = HyperlinkedIdentityField(
        view_name = "djangopost:article_destroy_viewset",
        lookup_field = "slug"
    )

    detail_url = HyperlinkedIdentityField(
        view_name = "djangopost:article_detail_view",
        lookup_field = "slug",
        lookup_url_kwarg = "article_slug"
    )

    class Meta:
        model = ArticleModel
        fields = ['serial', 'cover_image', 'title', 'slug', 'category', 'description', 'shortlines',
                  'content', 'author', 'status', 'verification', 'is_promote', 'is_trend',
                  'total_views', 'created_at', 'updated_at', 'api_detail_url', 'api_update_url',
                  'api_delete_url', 'detail_url']
