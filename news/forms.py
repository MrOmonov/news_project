from django import forms

from news.models import ContactModel, Comments


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, required=True, label='FIO')
    email = forms.CharField(max_length=150,
                            required=True,
                            widget=forms.EmailInput(),
                            label='E-mail')
    message = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={'cols':30, 'rows':7}),
                           label='Matn')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body',)
