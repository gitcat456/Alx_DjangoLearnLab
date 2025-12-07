from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Post, Comment, Tag


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        help_text='Enter tags separated by commas'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-fill tags for existing posts
            tags = self.instance.tags.all()
            self.initial['tags_input'] = ', '.join(tag.name for tag in tags)
    
    def clean_tags_input(self):
        tags_input = self.cleaned_data.get('tags_input', '')
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        return tags
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Clear existing tags
            post.tags.clear()
            # Add new tags
            for tag_name in self.cleaned_data['tags_input']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
        return post


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)  

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
        

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search posts...'})
    )