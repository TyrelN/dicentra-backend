from rest_framework import serializers

from .models import CurrentEvent, AdoptForm, FosterForm, HelpWanted, VolunteerForm, PetPost, ArticlePost
from django.contrib.auth.models import User, Group

class FosterFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FosterForm
        fields = '__all__'
        read_only_fields = ['slug', 'created_on']
        lookup_field = "slug"
class AdoptFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptForm
        fields = '__all__'
        read_only_fields = ['slug', 'created_on']
        lookup_field = "slug"
class VolunteerFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerForm
        fields = '__all__'
        read_only_fields = ['slug', 'created_on']
        lookup_field = "slug"    
class ArticlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlePost
        fields = ('title', 'slug', 'created_on', 'content', 'content_second', 'content_third', 'header_image', 'content_image', 'content_image_second', 'category', 'caption', 'caption_second', 'get_content_image', 'get_content_image_second', 'url1', 'url2', 'url3', 'url4', 'is_published')
        read_only_fields = ['slug', 'created_on']
        lookup_field = "slug"     
class PetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetPost
        fields = ('name', 'color', 'slug', 'description', 'age', 'available', 'sex', 'spayed', 'image', 'get_thumbnail_image', 'get_detail_image', 'is_published')
        read_only_fields = ['slug', 'created_on']
        lookup_field = "slug"
class HelpWantedSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpWanted
        fields = '__all__'
        lookup_field = "slug"
class CurrentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentEvent
        fields = ('id','message', 'get_image','image')

    