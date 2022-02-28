from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from data.models import CurrentEvent, HelpWanted, AdoptForm, FosterForm, VolunteerForm, ArticlePost, PetPost
from data.serializers import CurrentEventSerializer, HelpWantedSerializer, AdoptFormSerializer, FosterFormSerializer, VolunteerFormSerializer, ArticlePostSerializer, PetPostSerializer
# Create your tests here.

class HelpWantedViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.help_wanteds = [HelpWanted.objects.create(title="yes"+str(i)) for i in range(3)]
        cls.help_wanted = cls.help_wanteds[0]
        
    def test_can_browse_all_posts(self):
        response = self.client.get(reverse("posts:helpwanted-list"))
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.help_wanteds), len(response.data))
        
        for ad in self.help_wanteds:
            
            self.assertIn(
                HelpWantedSerializer(instance=ad).data,
                response.data
            )