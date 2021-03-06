from django import forms
from django.contrib.auth.forms import UserCreationForm
from .utils import get_words_from_sentence


class SearchForm(forms.Form):
    """
    define the search form for search product on openfoodfacts
    """
    search = forms.CharField(label="Recherche", max_length=255, required=True,
                             min_length=2)

    def clean_search(self):
        data = tuple(get_words_from_sentence(self.cleaned_data['search']))
        if not data:
            raise forms.ValidationError("Entrez une recherche valide.")

        return " ".join(data)


class CustomUserCreationForm(UserCreationForm):
    """add email field to the registration form"""

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email')
