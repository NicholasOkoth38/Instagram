from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Profile(models.Model):
   
    user = models.OneToOneField(User,on_delete=models.CASCADE, default=0)
    profile_photo = CloudinaryField('profiles-pic')
    # profile_photo = models.ImageField(upload_to='images/', default='default.png')
    bio = models.CharField(max_length=50)   
    following = models.ManyToManyField(User,blank=True,related_name='follow')

    def __str__(self):
        return self.user.username
    
    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete() 

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

    @classmethod        
    def update_profile(cls, id, profile):
        cls.objects.filter(id=id).update(profile=profile)

class Image(models.Model):
    image = CloudinaryField('posts')
    # image = models.ImageField(upload_to='posts/')
    image_name= models.CharField(max_length=50, blank=True)
    image_caption= models.CharField(max_length=400)
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE)  
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    comments = models.CharField(max_length=30,blank=True)

    
    def __str__(self):
        return self.image_name

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()   

    @property
    def comments(self):
        return self.comments.all()

    def likes(self):
        return self.likes.count()

class Comment(models.Model):
    comment= models.TextField()
    comment_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_post = models.ForeignKey(Image, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True, null=True)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()       