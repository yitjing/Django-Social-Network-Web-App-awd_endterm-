from django.urls import path
from . import views

# I wrote this code
urlpatterns = [
	path('', views.index, name='index'),
	path('signUp/', views.signUp, name='signUp'),
	path('userLogin/', views.userLogin, name='userLogin'),
	path('userLogout/', views.userLogout, name='userLogout'),
	path('deleteUser/', views.deleteUser, name='deleteUser'),
	path('profile/<str:user>', views.profile, name='profile'),
	path('editProfile/', views.editProfile, name='editProfile'),
	path('uploadPost/', views.uploadPost, name='uploadPost'),
	path('likePost/', views.likePost, name='likePost'),
	path('follow/<int:userId>', views.follow, name='follow'),
	path('search/', views.search, name='search'),
	path('<str:room_name>/', views.chatRoom, name='chatRoom'),
	path('deletePost/<int:postId>', views.deletePost, name='deletePost'),
	
	#get request to allows user to view the json data
	path('api/userProfile/', views.UserProfileListView.as_view(), name='UserProfileListView'),
	path('api/PostListView/', views.PostListView.as_view(), name='PostListView'),
	path('api/LikePostListView/', views.LikePostListView.as_view(), name='LikePostListView'),
	path('api/FollowerListView/', views.FollowerListView.as_view(), name='FollowerListView')
]
# end of code i wrote
