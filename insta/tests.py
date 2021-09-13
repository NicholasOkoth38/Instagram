from insta.models import Image, Profile
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
class TestProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", "secret")
        self.profile_test = Profile(profile_photo='test.jpg',bio="this is a test bio",user=self.user)
        self.profile_test.save()

    def test_instance_true(self):
        self.profile_test.save()
        self.assertTrue(isinstance(self.profile_test, Profile))

    def test_save_profile(self):
        self.profile_test.save()
        pp = Profile.objects.all()
        self.assertTrue(len(pp) > 0)

# test for model class Image
class TestImage(TestCase):
    def setUp(self):

        self.user = User.objects.create_user("testuser", "secret")

        self.new_profile = Profile(profile_photo='test.jpg',bio="this is a test bio",user=self.user)
        self.new_profile.save()

        self.new_image = Image(image='test.jpg',image_caption="image", profile=self.new_profile)

    def test_instance_true(self):
        self.new_image.save()
        self.assertTrue(isinstance(self.new_image, Image))

    def test_save_image_method(self):
        self.new_image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images) == 1)

    def tearDown(self):
        Image.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
