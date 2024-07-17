from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from awd_app.models import *
from awd_app.views import *
from awd_app.serializers import *

#rest_framework imports
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from datetime import datetime
# for creating the mock image file used for testing
from PIL import Image
from io import BytesIO

# Create your tests here.
# I wrote this code
#test the models objects whether they works as intended representation
class UserProfileModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testUsername', password='testPassword')
		self.user_profile = UserProfile.objects.create(
			user = self.user,
			firstName = 'James',
			lastName = 'Wong',
			birthDate = datetime(1993, 10, 10),
			bio = 'Test bio',
			location = 'Test location',
		)

	def test_user_profile_str(self):
		self.assertEqual(str(self.user_profile), self.user.username)

class PostModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testUsername', password='testPassword')
		self.post = Post.objects.create(
			user = self.user,
			created = timezone.now(),
			caption =' Test caption',
			image = 'testImage.jpg',
		)

	def test_post_str(self):
		self.assertEqual(str(self.post), self.user.username)

class LikePostModelTest(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', password='testPassword1')
		self.user2 = User.objects.create_user(username='user2', password='testPassword2')
		self.post = Post.objects.create(
			user=self.user1,
			caption='Test caption',
		)
		self.like_post = LikePost.objects.create(user=self.user2, post=self.post)

	def test_like_post_str(self):
		self.assertEqual(str(self.like_post), self.user2.username)

class FollowerModelTest(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', password='testPassword1')
		self.user2 = User.objects.create_user(username='user2', password='testPassword2')
		self.follower = Follower.objects.create(user=self.user1, followerUser=self.user2)

	def test_follower_str(self):
		self.assertEqual(str(self.follower), self.user1.username)
		
#to test serializers
class UserProfileSerializerTest(TestCase):
	def test_user_profile_serializer(self):
		self.user = User.objects.create_user(username='testUsername', password='testPassword')
		user_profile_data = {
			'user': self.user.id,
			'firstName': 'James',
			'lastName': 'Wong',
			'birthDate': '1993-10-10',
			'bio': 'Test bio',
			'location': 'Test location',
		}
		
		serializer = UserProfileSerializer(data=user_profile_data)
		self.assertTrue(serializer.is_valid())

	def test_user_profile_serializer_validation(self):
		self.user = User.objects.create_user(username='testUsername', password='testPassword')
		user_profile_data = {
			'user': self.user.id,
			#max length is 50
			'firstName': 'James' * 11,
			'lastName': 'Wong',
			#birthDate cannot be in future
			'birthDate': datetime(2030, 10, 10),
			'bio': 'A',
			#location max length is 90
			'location': 'Test location'* 20,
		}
		serializer = UserProfileSerializer(data=user_profile_data)
		self.assertFalse(serializer.is_valid())
		self.assertIn('firstName', serializer.errors)
		self.assertIn('birthDate', serializer.errors)
		self.assertIn('location', serializer.errors)

class PostSerializerTest(TestCase):
	def test_post_serializer(self):
		self.user = User.objects.create_user(username='testUsername', password='testPassword')
		
		post_data = {
			'user': self.user.id,
			'created': timezone.now(),
			'caption': 'Test caption',
			'likes': 0,
		}
		serializer = PostSerializer(data=post_data)
		self.assertTrue(serializer.is_valid())

class LikePostSerializerTest(TestCase):
	def test_like_post_serializer(self):
		self.user = User.objects.create_user(username='testUsername', password='testPassword')
		self.post = Post.objects.create(user=self.user, created=timezone.now(), caption='test caption', likes=0)
		
		like_post_data = {
			'user': self.user.pk,
			'post': self.post.pk,
		}
		serializer = LikePostSerializer(data=like_post_data)
		self.assertTrue(serializer.is_valid())

class FollowerSerializerTest(TestCase):
	def test_follower_serializer(self):
		user1 = User.objects.create_user(username='testUsername', password='testPassword1')
		user2 = User.objects.create_user(username='testUsername2', password='testPassword2')
		follower_data = {
			'user': user1.id,
			'followerUser': user2.id,
		}
		serializer = FollowerSerializer(data=follower_data)
		self.assertTrue(serializer.is_valid())

class EditProfileSerializerTest(TestCase):
	def test_edit_profile_serializer(self):
		profile_data = {
			'firstName': 'James',
			'lastName': 'Wong',
			'birthDate': '1993-10-10',
			'bio': 'Test bio',
			'location': 'Test location',
		}
		serializer = EditProfileSerializer(data=profile_data)
		self.assertTrue(serializer.is_valid())

	#tes whether the validation for edit profile data works
	def test_edit_profile_serializer_validation(self):
		profile_data = {
			#max length is 50
			'firstName': 'James' * 11,
			'lastName': 'Wong',
			#birthDate cannot be in future
			'birthDate': datetime(2030, 10, 10),
			#bio max length is 300
			'bio': 'A' * 301,
			'location': 'Test location',
		}
		serializer = EditProfileSerializer(data=profile_data)
		self.assertFalse(serializer.is_valid())
		self.assertIn('firstName', serializer.errors)
		self.assertIn('birthDate', serializer.errors)
		self.assertIn('bio', serializer.errors)
		
#test views
class ViewsTest(TestCase):
	#set up new account client to test
	def setUp(self):
		#initialize the APIClient
		self.client = Client()
		self.user = User.objects.create_user(username='testUser', password='testPassword')
		#login to the client account
		self.client.login(username='testUser', password='testPassword')
		self.user_profile = UserProfile.objects.create(user=self.user, firstName='James', lastName='Wong')
		
	#test whether the user could sign up new account to access the app
	def test_sign_up_view(self):
		response = self.client.get(reverse('signUp'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
	#test whether user could login into the app
	def test_user_login_view(self):
		response = self.client.get(reverse('userLogin'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
	#test whether the user could logout of the app and redirect to the index page
	def test_user_logout_view(self):
		response = self.client.get(reverse('userLogout'))
		self.assertEqual(response.status_code, status.HTTP_302_FOUND)

	#test to check whether the index view works as expected
	def test_index_view(self):
		response = self.client.get(reverse('index'))
		#status 200 works as expected ok
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
	#test whether it will redirects the user to other page when the user is deleted
	def test_delete_view(self):
		response = self.client.get(reverse('deleteUser'))
		#status 300 redirects as expected ok
		self.assertEqual(response.status_code, status.HTTP_302_FOUND)
		
	def tearDown(self):
		self.client.logout()
	
#test whether the search for user views works
class SearchViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testUser', password='testPassword')
		self.user_profile = UserProfile.objects.create(user=self.user, firstName='James', lastName='Wong')
		
	def test_search(self):
		#initialize the APIClient
		self.client = Client()
		#login with the client account
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(reverse('search'), {'search': 'testUser'})

		#success when it redirect from the index to search page for results
		self.assertEqual(response.status_code, status.HTTP_200_OK)

#test whether the user could edit the user profile data in edit profile page		
class EditProfileViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testUser', password='testPassword')
		self.user_profile = UserProfile.objects.create(user=self.user, firstName='James', lastName='Wong')
		
	def tearDown(self):
		#clean the client test data
		self.user_profile.delete()
		self.user.delete()

	def test_edit_profile(self):
		#initialize the APIClient
		self.client = Client()
		#login with the client account
		self.client.login(username='testUser', password='testPassword')
		#insert the new profile data to edit the profile
		profileData = {
			'firstName': 'James',
			'lastName': 'Wong',
			'birthDate': datetime(1993, 10, 10),
			'bio': 'Test bio',
			'location': 'Test location',
		}
		
		response = self.client.post(reverse('editProfile'), profileData, format='multipart')

		self.assertEqual(response.status_code, status.HTTP_200_OK)

#test whether user could upload a new post		
class UploadPostViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testUser', password='testPassword')
		#initialize the APIClient
		self.client = APIClient()
		#login with the client account
		self.client.login(username='testUser', password='testPassword')

	def test_upload_post(self):
		# create a mock image
		width, height = 400, 400
		image = Image.new("RGB", (width, height), "white")

		# save the image to a BytesIO
		imageFile = BytesIO()
		image.save(imageFile, "JPEG")
		imageFile.seek(0)

		postData = {
			'user': self.user,
			'created': timezone.now(),
			'caption': 'Test caption',
			'image': imageFile,
			'likes': 0,
		}

		response = self.client.post(reverse('uploadPost'), postData, format='multipart')

		#redirects the index page
		self.assertEqual(response.status_code, status.HTTP_302_FOUND)
		
#test whether user could like and unlike a created post
class LikePostViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testUser', password='testPassword')
		#create a post
		self.post = Post.objects.create(
			user = self.user,
			created = timezone.now(),
			caption =' Test caption',
			image = 'testImage.jpg',
		)

	def test_like_post(self):
		#login with the client account
		self.client.login(username='testUser', password='testPassword')

		response = self.client.get(reverse('likePost') + f'?postId={self.post.postId}')

		self.assertEqual(response.status_code, status.HTTP_302_FOUND)

#test whether the user could delete a existed post
class DeletePostViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testUser', password='testPassword')
		#create a post
		self.post = Post.objects.create(
			user = self.user,
			created = timezone.now(),
			caption =' Test caption',
			image = 'testImage.jpg',
		)

	def test_delete_post(self):
		#login with the client account
		self.client.login(username='testUser', password='testPassword')

		response = self.client.post(reverse('deletePost', args=[self.post.postId]))

		self.assertEqual(response.status_code, status.HTTP_302_FOUND)

#test whether user could follow and unfollow other user
class FollowViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testUser', password='testPassword')
		self.user_profile = UserProfile.objects.create(
			user = self.user,
			firstName = 'James',
			lastName = 'Wong',
			birthDate = datetime(1993, 10, 10),
			bio = 'Test bio',
			location = 'Test location',
		)
		self.userFollow = UserProfile.objects.get(user=self.user)

	def test_follow(self):
		#login with the client account
		self.client.login(username='testUser', password='testPassword')

		response = self.client.post(reverse('follow', args=[self.userFollow.user.id]))

		self.assertEqual(response.status_code, status.HTTP_302_FOUND)
		
# end of code i wrote
