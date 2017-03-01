from django import forms
from smart_selects.form_fields import ChainedModelChoiceField
from lists.models import Category

class AnalyticsForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    object = ChainedModelChoiceField('lists', 'Object', 'category', 'category', 'lists', 'Object', 'category', False, False)
    attribute = forms.ChoiceField(choices=(('gender', 'Gender'),('locale', 'Locale'),('age_range', 'Age Range')))
