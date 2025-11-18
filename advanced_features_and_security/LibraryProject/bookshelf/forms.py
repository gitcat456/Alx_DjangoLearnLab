# LibraryProject/bookshelf/forms.py

from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': 200}),
            'author': forms.TextInput(attrs={'maxlength': 100}),
            'publication_year': forms.NumberInput(),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if "<script>" in title.lower():
            raise forms.ValidationError("Invalid characters in title.")
        return title

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if "<script>" in author.lower():
            raise forms.ValidationError("Invalid characters in author.")
        return author

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year < 1000 or year > 2100:
            raise forms.ValidationError("Enter a valid year.")
        return year