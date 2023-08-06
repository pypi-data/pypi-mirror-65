
from django import forms
from categories.models import Category


class SearchProductForm(forms.Form):

    code = forms.CharField(required=False)

    bar_code = forms.CharField(required=False)

    query = forms.CharField(required=False)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.HiddenInput)

    def clean(self):

        cleaned_data = {}

        for k, v in self.cleaned_data.items():
            if v:
                cleaned_data[k] = v

        return cleaned_data
