from io import BytesIO #images \
import sys
import random
import string
from PIL import Image
from django.db import models 
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField #this import is how we will store checkbox questions
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete, pre_save, post_save, post_delete
from django.core.cache import cache
from django.utils.text import slugify
import cloudinary
from django.dispatch import receiver
import cloudinary_storage

#function to create a random string as slug ending to decrease chance of identical slug
def random_slug():
    return f''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))

#an abstract base class for the specific form implementations
class Applicant(models.Model):
    HOME = 'Home'
    CELL = 'Cell'
    BUSINESS = 'Business'
    PHONE_CHOICES = [
        (HOME, 'Home'),
        (CELL, 'Cell'),
        (BUSINESS, 'Business'),
    ]
    MORNING = 'Morning'
    EVENING = 'Evening'
    AFTERNOON = 'Afternoon'
    HOURS_CHOICES = [
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon'),
        (EVENING, 'Business'),
    ]
    APPROVED = 'approved'
    IN_PROCESS = 'in_process'
    REJECTED = 'rejected'
    REVIEW_STATUS = [
    (APPROVED, "approved"),
    (IN_PROCESS,"in process"),
    (REJECTED,"rejected"),
    ]
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    city = models.CharField(max_length=150)
    zip = models.CharField(max_length=17)
    dayphone = models.CharField(max_length=17)
    dayphonetype = models.CharField(max_length=20, choices=PHONE_CHOICES)
    eveningphone = models.CharField(max_length=20)
    eveningphonetype = models.CharField(max_length=20, choices=PHONE_CHOICES)
    email = models.EmailField()
    calltimes = models.CharField(max_length=40)
    created_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REVIEW_STATUS, default=IN_PROCESS);
    class Meta:
        abstract = True
        ordering = ['-created_on']

    def _str_(self):
        return self.firstname, self.lastname

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_addon = random_slug()
            slug_text = self.firstname + '-' + self.lastname + '-' + slug_addon
            self.slug = slugify(slug_text, allow_unicode=True)
        super().save(*args, **kwargs)

#the number of questions here reflects the number of questions in the frontend for this form
class AdoptForm(Applicant):
    question1 = models.CharField(max_length=255)
    question2 = models.CharField(max_length=255)
    question3 = models.CharField(max_length=255)
    question4 = models.CharField(max_length=255, blank=True)
    question5 = models.CharField(max_length=255)
    question6 = models.CharField(max_length=255)
    question7 = models.CharField(max_length=255)
    question8 = models.CharField(max_length=255)
    question9 = models.CharField(max_length=255)
    question10 = models.CharField(max_length=255)
    question11 = models.CharField(max_length=255)
    question12 = models.CharField(max_length=255)
    question13 = models.CharField(max_length=255)
    question14 = models.CharField(max_length=255)
    question15 = models.CharField(max_length=255)
    question16 = models.CharField(max_length=255)
    question17 = models.CharField(max_length=255)
    question18 = models.CharField(max_length=255)
    question19 = models.CharField(max_length=255)
    question20Name = models.CharField(max_length=255)
    question20Phone = models.CharField(max_length=255)
    question21Ref = models.CharField(max_length=255)
    question21Phone = models.CharField(max_length=255)
    question21Ref2 = models.CharField(max_length=255)
    question21Phone2 = models.CharField(max_length=255)

#blank modifications to questions mean they are optional
class VolunteerForm(Applicant):
    question1 = models.CharField(max_length=255, blank=True)
    question2 = models.CharField(max_length=255, blank=True)
    question3 = models.CharField(max_length=255, blank=True)
    question4 = models.CharField(max_length=255, blank=True)
    question5 = models.CharField(max_length=255)
    question6 = models.CharField(max_length=255)
    question7 = models.CharField(max_length=255)
    question8 = models.CharField(max_length=255)
    question9 = models.CharField(max_length=255)
    question10 = models.CharField(max_length=255)
    question11 = models.CharField(max_length=255)
    question12 = models.CharField(max_length=255, default="")
    question13 = models.CharField(max_length=255, default="")
    question14 = models.CharField(max_length=255, default="", blank=True)

class FosterForm(Applicant):
    question1 = models.CharField(max_length=255)
    question2 = models.CharField(max_length=255)
    question3 = models.CharField(max_length=255)
    question4 = models.CharField(max_length=255)
    question5 = models.CharField(max_length=255)
    question6 = models.CharField(max_length=255)
    question7 = models.CharField(max_length=255)
    question8 = models.CharField(max_length=255)
    question9 = models.CharField(max_length=255)
    question10 = models.CharField(max_length=255)
    question11 = models.CharField(max_length=255)
    question12 = models.CharField(max_length=255)
    question13 = models.CharField(max_length=255)
    question14 = models.CharField(max_length=255)
    question15 = models.CharField(max_length=255)
    question16 = models.CharField(max_length=255)
    
class HelpWanted(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    description = models.TextField()
    created_on = models.DateField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_on']
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = self.title
            self.slug = slugify(slug_text, allow_unicode=True)
        super().save(*args, **kwargs)

#there will only be one current event, so a singleton model is implemented
class CurrentEvent(models.Model):
    message = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    def get_image(self):
        if self.image:
            img = cloudinary.CloudinaryImage(self.image.name)
            return img.build_url(dpr="auto", fetch_format='auto', width="auto", crop="scale", quality=65, client_hints="true", sizes="100vw")
            
        return ''
    #disallow deletion since only one should exist
    def delete(self, *args, **kwargs):
        pass
    
                
class ArticlePost(models.Model):
    #choices designed according to django documentation guidelines
    INFORMATION = 'information'
    NEWS = 'news'
    EVENT = 'event'
    SEASONAL = 'seasonal'
    CATEGORY_CHOICES = [
        (INFORMATION, 'information'),
        (NEWS, 'news'),
        (EVENT, 'event'),
        (SEASONAL, 'seasonal'),
    ]
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(blank=True, null=True)
    content_second = models.TextField(blank=True, null=True)
    content_third = models.TextField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    header_image = models.ImageField(upload_to='images/', blank=True, null=True)
    content_image = models.ImageField(upload_to='images/', blank=True, null=True)
    content_image_second = models.ImageField(upload_to='images/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank = True, null=True, default='')
    caption_second = models.CharField(max_length=255, blank = True, null=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    url1= models.URLField(max_length=250, blank=True, null=True)
    url2= models.URLField(max_length=250, blank=True, null=True)
    url3= models.URLField(max_length=250, blank=True, null=True)
    url4= models.URLField(max_length=250, blank=True, null=True)
    is_published = models.BooleanField(default=False);
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title
#methods for returning a modified cloudinary url for optimized images
    def get_header_image(self):
        if self.header_image:
            img = cloudinary.CloudinaryImage(self.header_image.name)
            return img.build_url(fetch_format = 'auto', quality="60")
        return ''

    def get_content_image(self):
        if self.content_image:
            img = cloudinary.CloudinaryImage(self.content_image.name)
            return img.build_url(fetch_format = 'auto', quality=50)   
        return ''
    def get_content_image_second(self):
        if self.content_image_second:
            img = cloudinary.CloudinaryImage(self.content_image_second.name)
            return img.build_url(fetch_format = 'auto', quality=50) 
        return ''
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_addon = random_slug()
            slugText = self.title + '-' + slug_addon
            self.slug = slugify(slugText, allow_unicode=True)
        super(ArticlePost, self).save(*args, **kwargs)

class PetPost(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    SEX_CHOICES = [
        (MALE, 'male'),
        (FEMALE, 'female'),
    ]
    AVAILABLE = 'available'
    NOTAVAILABLE = 'not available'
    ADOPTED = 'adopted'
    AVAILABLE_CHOICES = [
       (AVAILABLE, 'available'),
        (NOTAVAILABLE, 'not available'),
        (ADOPTED, 'adopted'),
    ]
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description =  models.TextField(blank=True, null=True)
    age = models.CharField(max_length=100, blank=True)
    available = models.CharField(max_length=150, choices=AVAILABLE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=6, choices = SEX_CHOICES, default = FEMALE);
    spayed = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True)
    created_on = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    
    #order based on when object was created (descending)
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name
    
    def get_thumbnail_image(self):
        if self.image:
            img = cloudinary.CloudinaryImage(self.image.name, format='png')
            return img.build_url(fetch_format = 'auto', quality=50, width=290, height=290, crop="fill")
        return ''
    
    def get_detail_image(self):
        if self.image:
            img = cloudinary.CloudinaryImage(self.image.name)
            return img.build_url(fetch_format = 'auto', quality=60)
        return ''
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_addon = random_slug()
            slug_text = self.name + '-' + slug_addon
            self.slug = slugify(slug_text, allow_unicode=True)
    
        super(PetPost, self).save(*args, **kwargs)