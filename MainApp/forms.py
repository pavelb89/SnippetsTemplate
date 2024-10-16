from django.forms import ModelForm, ValidationError, TextInput, Textarea
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code']
        labels = {'name': '', 'lang': '', 'code': ''}
        widgets = {
            'name': TextInput(attrs={
                    'class': 'form-control',
                    'style': 'max-width: 300px',
                    'placeholder': 'Название сниппета'
                }),
            'code': Textarea(attrs={
                    'class': 'input-large',
                    'style': 'width: 50% !important; resize: vertical !important;',
                    'placeholder': 'Код сниппета',
                    'rows': 5,
                }),
        }

    def clean_name(self):
        snippet_name = self.cleaned_data.get('name')
        if snippet_name is not None and len(snippet_name) > 3:
            return snippet_name
        raise ValidationError("Snippet's name too short!")