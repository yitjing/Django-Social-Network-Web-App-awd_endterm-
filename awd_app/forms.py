from django import forms
from .models import UserProfile

class ImageForm(forms.ModelForm):
	"""Form for the image model"""
	class Meta:
		model = Image
		fields = ('image')
