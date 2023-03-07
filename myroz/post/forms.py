from django import forms

from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Добавили поле image в форму
        fields = ('group', 'text', 'image')


class CommentForm(forms.Form):
    parent_comment = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )

    comment_area = forms.CharField(
        label="",
        widget=forms.Textarea
    )