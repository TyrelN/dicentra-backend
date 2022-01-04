from django.urls import path, include
from rest_framework.routers import DefaultRouter
from data import views
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r'volunteerforms', views.VolunteerFormViewSet)
router.register(r'fosterforms', views.FosterFormViewSet)
router.register(r'adoptforms', views.AdoptFormViewSet)
router.register(r'articles', views.ArticlePostViewSet)
router.register(r'petposts', views.PetPostViewSet)
router.register(r'wantedads', views.HelpWantedViewSet)
router.register(r'currentevent', views.CurrentEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)