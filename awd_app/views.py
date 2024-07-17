from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
# provides tools and component to implement user authentication and authorization
from django.contrib.auth import authenticate, login, logout
# checks whether the user has login into the application
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db.models import F

from .models import UserProfile, Post, LikePost, Follower
from .serializers import UserProfileSerializer, EditProfileSerializer, PostSerializer, LikePostSerializer, FollowerSerializer

# Create your views here.

# I wrote this code
# i have made some reference from github 
# https://github.com/tomitokko/django-social-media-website/tree/main

# checks whether the user is login before allowing them to access the homepage
# if user not login the app would redirect the user to the login page if they wanted to access the home page directly by using the url
@login_required(login_url='userLogin')
def index(request):
	user = User.objects.get(username=request.user.username)
	userProfile = UserProfile.objects.get(user=user)
	
	#to set the chat room name when both user follows each other
	#only can chat when both of them are friend
	friendList = []
	chatRoom = []
				
	# Get a queryset of all followers for the current user
	user_followers = Follower.objects.filter(user=user)

	# Iterate through each follower of the current user
	for follower in user_followers:
		# check if the follower is also following the user owner
		mutual_follower = Follower.objects.filter(user=follower.followerUser, followerUser=user)
		
		#if both user follows each other then they allows to chat
		if mutual_follower.exists():
			friend = mutual_follower.first().user
			roomName = [user.username, friend.username]
			roomName.sort()
			friendChat = [friend, roomName]
			friendList.append(friendChat)
				
	#post list requirements that only show the owner and following user post
	followList = []
	posts = []

	followingUser = Follower.objects.filter(followerUser=request.user.id)

	for users in followingUser:
		followList.append(users.user)

	for userNames in followList:
		postLists = Post.objects.filter(user=userNames)
		posts.append(postLists)
		
	#append owner post to the post list in home page
	ownerPost = Post.objects.filter(user=user)
	posts.append(ownerPost)

	postList = [post for postLists in posts for post in postLists]
	
	context = {
		'userProfile': userProfile, 
		'posts': postList, 
		'followList': followList, 
		'friendList': friendList,
	}
	
	template = loader.get_template('index.html')
	return HttpResponse(template.render(context,request))
	
# to sign up new user into the application
def signUp(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']
		
		if password == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request, 'Username taken')
				#redirect to the same page and process
				return HttpResponseRedirect(reverse('signUp'))
			else:
				#saved to the Users in the django administration
				user = User.objects.create_user(username=username, password=password)
				user.save()
				
				#login the user into the application and redirect the user to the profile page
				# this allows user to edit their bio, location, birth date and images
				userSignIn = authenticate(username=username, password=password)
				login(request, userSignIn)
				
				#create profile object for new user in the django administration
				userName = User.objects.get(username=username)
				userProfile = UserProfile.objects.create(user=userName)
				userProfile.save()
				
				return HttpResponseRedirect(reverse('editProfile'))
		else:
			messages.info(request, 'Password and Confirmation must be matched!')
			#redirect to the same page and process
			return HttpResponseRedirect(reverse('signUp'))
	else:
		template = loader.get_template('signUp.html')
		return HttpResponse(template.render({},request))

#to login the existed user into the app		
def userLogin(request):
	# sensitive info use post
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		# if the user is in the database
		if user is not None:
			# authenticate
			# allow the user to login into the application
			login(request, user)
			# redirect back to home page
			return HttpResponseRedirect(reverse('index'))
		else:
			messages.info(request, 'The username is invalid')
			return HttpResponseRedirect(reverse('userLogin'))
	else:
		template = loader.get_template('logIn.html')
		return HttpResponse(template.render({},request))
	
#logout the user from the application	
def userLogout(request):
	#log the user out of the application
	logout(request)
	return HttpResponseRedirect(reverse('userLogin'))
	
#delete user from the app
@login_required(login_url='userLogin')	
def deleteUser(request):
	user = request.user
	user.delete()
	return HttpResponseRedirect(reverse('signUp'))
	
# search for other existing user in the application
@login_required(login_url='userLogin')	
def search(request):
	user = User.objects.get(username=request.user.username)
	userProfile = UserProfile.objects.get(user=user)
	
	if request.method == 'POST':
		#searched username
		username = request.POST['search']
		searchUserName = User.objects.filter(username__icontains=username)
		
		searchUserProfile = []
		searchUserProfileList = []
		
		for users in searchUserName:
			searchUserProfile.append(users)
			
		for names in searchUserProfile:
			profileLists = UserProfile.objects.filter(user=names)
			searchUserProfileList.append(profileLists)
			
		searchUserProfileList = [profile for profiles in searchUserProfileList for profile in profiles]
		
	template = loader.get_template('search.html')
	return HttpResponse(template.render({'userProfile': userProfile, 'searchUserProfileList': searchUserProfileList},request))

#show user profile data
@login_required(login_url='userLogin')	
def profile(request, user):
	userName = User.objects.get(username=user)
	userProfile = UserProfile.objects.get(user=userName)
	userPosts = Post.objects.filter(user=userName.id).order_by('-created')
	userPostNo = len(userPosts)
	
	#account owner
	follower = request.user.id
	#followed user by the owner
	followingUser = userName.id
	
	#follow and unfollow button text
	if Follower.objects.filter(followerUser=follower, user=followingUser).first():
		btnText = 'Unfollow'
	else:
		btnText = 'Follow'
	
	#to count the number of followers and following	
	followerNo = len(Follower.objects.filter(user=followingUser))
	followingNo = len(Follower.objects.filter(followerUser=followingUser))
		
	userData = {
		'userName': userName,
		'userProfile': userProfile,
		'userPosts': userPosts,
		'userPostNo': userPostNo,
		'followerNo': followerNo,
		'followingNo': followingNo,
		'btnText': btnText,
	}
	
	template = loader.get_template('profile.html')
	return HttpResponse(template.render(userData,request))
	
#edit the exisiting profile data
@login_required(login_url='userLogin')
@api_view(['GET','POST'])
def editProfile(request):
	if request.method == 'GET':
		# Retrieve the user's profile
		userProfile = UserProfile.objects.get(user=request.user)
		serializer = EditProfileSerializer(userProfile)
		return render(request, 'editProfile.html', {'userProfile': userProfile})
	elif request.method == 'POST':
		# Retrieve the user's profile
		userProfile = UserProfile.objects.get(user=request.user)
		# Use the EditProfileSerializer to validate and update the profile
		serializer = EditProfileSerializer(userProfile, data=request.data)
		if serializer.is_valid():
			serializer.save()
			if request.FILES.get('profileImage') == None:
				if request.FILES.get('coverImage') == None:
					coverImage = userProfile.coverImg
				else:
					coverImage = request.FILES.get('coverImage')
					
				image = userProfile.profileImg

				userProfile.profileImg = image
				userProfile.coverImg = coverImage
					
				userProfile.save()
			else:
				if request.FILES.get('coverImage') == None:
					coverImage = userProfile.coverImg
				else:
					coverImage = request.FILES.get('coverImage')
					
				image = request.FILES.get('profileImage')

				userProfile.profileImg = image
				userProfile.coverImg = coverImage
					
				userProfile.save()
			
			return HttpResponseRedirect(reverse('editProfile'))

		template = loader.get_template('editProfile.html')
		return HttpResponse(template.render({'userProfile': userProfile, 'error_message': serializer.errors},request))

# upload the post to database
@login_required(login_url='userLogin')
@api_view(['POST'])
def uploadPost(request):
	if request.method == 'POST':
		user = User.objects.get(username=request.user.username)
		data = request.data
		data['user'] = user.id
		serializer = PostSerializer(data=data)
		
		if serializer.is_valid():
			serializer.save()
		return HttpResponseRedirect(reverse('index'))
	else:
		return HttpResponseRedirect(reverse('index'))

#like and unlike post
@login_required(login_url='userLogin')
def likePost(request):
	user = request.user
	postId = request.GET.get('postId')
	post = Post.objects.get(postId=postId)
	
	likeExist = LikePost.objects.filter(user=user, post=post).first()
	
	if likeExist == None:
		newLike = LikePost.objects.create(user=user, post=post)
		newLike.save()
		post.likes = post.likes + 1
		post.save()
		return HttpResponseRedirect(reverse('index'))
	else:
		likeExist.delete()
		post.likes = post.likes - 1
		post.save()
		return HttpResponseRedirect(reverse('index'))

#delete existing post		
@login_required(login_url='userLogin')	
def deletePost(request, postId):
	post = get_object_or_404(Post, postId=postId)
	if post.user == request.user:
		post.delete()
		return HttpResponseRedirect(reverse('index'))
		
	return HttpResponseRedirect(reverse('index'))	
	
#follow and unfollow user	
@login_required(login_url='userLogin')	
@api_view(['POST'])
def follow(request, userId):
	if request.method == 'POST':
		#the user account name (owner)
		follower = request.user
		user = get_object_or_404(UserProfile, user_id=userId)
		
		existFollower = Follower.objects.filter(followerUser=follower, user=user.user).first()
		
		#check whether it is a existing follower
		if existFollower:
			existFollower.delete()
			serializer = FollowerSerializer(existFollower)
			return HttpResponseRedirect(reverse('profile', args=[user]))
		else:
			newFollower = Follower.objects.create(followerUser=follower, user=user.user)
			newFollower.save()
			serializer = FollowerSerializer(newFollower)
			return HttpResponseRedirect(reverse('profile', args=[user]))
	else:
		return HttpResponseRedirect(reverse('index'))

#chat room that enables user who follows each other to chat	
@login_required(login_url='userLogin')	
def chatRoom(request, room_name):
	return render(request, 'chat/chatRoom.html', {'room_name': room_name})
	
# reference made from DJANGO REST framework
#https://www.django-rest-framework.org/
#allows the unauthenticate user to read only the json response data
#authenticate user could read, modify and delete the json response data

#retrieve a list of instance from the UserProfile model
class UserProfileListView(generics.ListAPIView):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

#retrieve a list of instance from the Post model
class PostListView(generics.ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

#retrieve a list of instance from the LikePost model
class LikePostListView(generics.ListAPIView):
	queryset = LikePost.objects.all()
	serializer_class = LikePostSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

#retrieve a list of instance from the Follower model
class FollowerListView(generics.ListAPIView):
	queryset = Follower.objects.all()
	serializer_class = FollowerSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
# end of code i wrote	
