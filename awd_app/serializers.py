# I wrote this code
from rest_framework import serializers
from .models import UserProfile, Post, Follower, LikePost
from django.utils import timezone

class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = ['user', 'firstName', 'lastName', 'birthDate', 'bio', 'location', 'profileImg', 'coverImg']
		
class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['postId', 'user', 'created', 'caption', 'image', 'likes']
		
class LikePostSerializer(serializers.ModelSerializer):
	class Meta:
		model = LikePost
		fields = ['user', 'post']
		
class FollowerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Follower
		fields = ['user', 'followerUser']
		
		
class EditProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = ['profileImg', 'coverImg', 'firstName', 'lastName', 'birthDate', 'bio', 'location']
	
	def validate(self, attrs):
		#make sure the name length is less than the max_length
		firstName = attrs.get('firstName')
		if firstName and len(firstName) > 50:
			raise serializers.ValidationError("First Name maximum length is 50")
			
		lastName = attrs.get('lastName')
		if lastName and len(lastName) > 50:
			raise serializers.ValidationError("Last Name maximum length is 50")
			
		#check if the birthdate is over the current datetime
		birthDate = attrs.get('birthDate')
		if not birthDate:
			raise serializers.ValidationError("Birth Date field is compulsory")
		elif birthDate and birthDate > timezone.now().date():
			raise serializers.ValidationError("Birth Date cannot be over the current timezone")
			
		#make sure the bio input not exceeded 300
		bio = attrs.get('bio')
		if bio and len(bio) > 300:
			raise serializers.ValidationError("Bio maximum length is 300")
			
		return attrs
		
# end of code i wrote
