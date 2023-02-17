from django import forms

from .models import Post
class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['text'].label = "Текст поста"
        # self.fields['text'].help_text = "Текст нового поста"
        # self.fields['group'].help_text = "Группа, к которой будет относиться пост"
        self.fields['group'].empty_label = "Группа не выбрана"

    class Meta:
        model = Post
        labels = {'group': 'Группа', 'text': 'Сообщение'}
        help_texts = {'group': 'Выберите группу', 'text': 'Введите ссообщение'}
        fields = ['text', 'group']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
