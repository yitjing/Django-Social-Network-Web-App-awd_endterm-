from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.

# I wrote this code
# i have made some reference from github 
# https://github.com/tomitokko/django-social-media-website/tree/main

# to use for authentications, to add in more fields for user to input for login and sign in into the application
# default fields is only username, email address, firstname, lastname
# custom user model (profile)
class UserProfile(models.Model):
	#add users from the Users
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	# blank=True (accepts blank value, not compulsory to fill in)
	firstName = models.CharField(max_length=50, blank=True, default="")
	lastName = models.CharField(max_length=50, blank=True, default="")
	birthDate = models.DateField(null=True, blank=True)
	bio = models.TextField(max_length=300, blank=True)
	location = models.CharField(max_length=90, blank=True)
	#User icon by Icons8
	profileImg = models.ImageField(null=True, blank=True, upload_to="media/profileImg/", default="icons8-user-96.png")
	coverImg = models.ImageField(null=True, blank=True, upload_to="media/coverImg/", default="defaultCover.jpg")
	
	def __str__(self):
		return self.user.username

# to store user posts information		
class Post(models.Model):
	# give each post a unique id
	postId = models.AutoField(primary_key=True)
	# when the user was deleted, all related post will be remove as well (models.CASCADE)
	user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
	created = models.DateTimeField(default=timezone.now)
	caption = models.TextField(max_length=500, blank=False)
	image = models.ImageField(null=True, blank=True, upload_to="media/")
	# number of likes for the post
	likes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.user.username

#to store the which user likes which user post	
class LikePost(models.Model):
	# give each post a unique id
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	
	class Meta:
		unique_together = ('user', 'post')
		
	def __str__(self):
		return self.user.username
	
#to store the followers and following user data	
class Follower(models.Model):
	#username of the person that is being followed by the profile user
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
	#the username of the person user is following (account owner)
	followerUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
	
	class Meta:
		unique_together = ('user', 'followerUser')
		
	def __str__(self):
		return self.user.username
# end of code i wrote
