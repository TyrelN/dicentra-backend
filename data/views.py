from io import BytesIO
import sys
import concurrent.futures
from PIL import Image
from functools import partial
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import filters
from .models import CurrentEvent, HelpWanted, AdoptForm, FosterForm, VolunteerForm, ArticlePost, PetPost
from .serializers import CurrentEventSerializer, HelpWantedSerializer, AdoptFormSerializer, FosterFormSerializer, VolunteerFormSerializer, ArticlePostSerializer, PetPostSerializer

#function to optimize image quality and reduce resolution to below 1500x1500 before upload to cloudinary
def compress_image(files, image_name=None):
        max_size = (1500, 1500)
        image = files.get(image_name)
        if image is None:
            return None
        image_temp = Image.open(image)
        #scales down all images to their aspect ratio below max size
        image_temp.thumbnail(max_size, Image.ANTIALIAS)
        output_stream = BytesIO()
        #save this image to the output stream
        image_temp.save(output_stream, format='JPEG', optimize=True, quality=60)
        #return the stream position back to zero with seek
        output_stream.seek(0)
        image = InMemoryUploadedFile(output_stream, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output_stream), None)
        return image
  
#helper functions to check that there are images submitted, and utilize multiple threads for articles. 
def handle_petpost_image(self, serializer):
    files = self.request.FILES
    if files:
        serializer.validated_data["image"] = compress_image(files, "image") 
    serializer.save()
def handle_article_image(self, serializer):
    files = self.request.FILES
    if files:
        #A multithreaded approach is taken here to eke out some performance on the IO side.
        #The platform the project is deployed on only has 1 CPU core available, so multi-processing would not help.
        images = ("header_image", "content_image", "content_image_second")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            process_image = partial(compress_image, files)
            futures = {executor.submit(process_image, image): image for image in images}
            
            for future in concurrent.futures.as_completed(futures):
                image_name = futures[future]
                if future.result():
                    serializer.validated_data[image_name] = future.result()
    serializer.save()  
    
#applications allow users to create forms and only authenticated users to view them
class AdoptFormViewSet(viewsets.ModelViewSet):
    queryset = AdoptForm.objects.all()
    serializer_class = AdoptFormSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    filterset_fields = ['status']
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
class FosterFormViewSet(viewsets.ModelViewSet):
    queryset = FosterForm.objects.all()
    serializer_class = FosterFormSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    filterset_fields = ['status']
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class VolunteerFormViewSet(viewsets.ModelViewSet):
    queryset = VolunteerForm.objects.all()
    serializer_class = VolunteerFormSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    filterset_fields = ['status']
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

#posts allow admins to perform manipulation queries while users may only view.
class ArticlePostViewSet(viewsets.ModelViewSet):
    queryset = ArticlePost.objects.all()
    serializer_class = ArticlePostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    filterset_fields = ['is_published']
    def get_permissions(self):
        if self.action == 'retrieve' or self.action == "list" or self.action == 'get_latest':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, permission_classes=[AllowAny])
    def get_latest(self, request):
        latest = ArticlePost.objects.all().first()
        serializer = ArticlePostSerializer(latest)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        handle_article_image(self, serializer)

    def perform_update(self, serializer):
        handle_article_image(self, serializer)
        
class PetPostViewSet(viewsets.ModelViewSet):
    queryset = PetPost.objects.all()
    serializer_class = PetPostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    filterset_fields = ['is_published']
    def get_permissions(self):
        if self.action == 'retrieve' or self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        handle_petpost_image(self, serializer)
    def perform_update(self, serializer):
        handle_petpost_image(self, serializer)
        
class HelpWantedViewSet(viewsets.ModelViewSet):
    queryset = HelpWanted.objects.all()
    serializer_class = HelpWantedSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class CurrentEventViewSet(viewsets.ModelViewSet):
    queryset = CurrentEvent.objects.all()
    serializer_class = CurrentEventSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action == 'retrieve' or self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    #override the create method to update if the only instance needed exists
    def create(self, request):
        serializer = CurrentEventSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            if "image" in request.data:
                serializer.validated_data["image"] = compress_image(request.FILES, "image")
            CurrentEvent.objects.update_or_create(pk=1, defaults={**serializer.validated_data})
            return Response({'status': 'post created'})