from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Form used to create (and could be reused to edit) a Post."""

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your post a title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post here...',
            }),
        }


class CommentForm(forms.ModelForm):
    """Form used by readers to leave a comment on a post."""

    class Meta:
        model = Comment
        fields = ['author_name', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add a comment...',
            }),
        }
