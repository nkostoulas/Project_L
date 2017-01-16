from django import forms
from .models import Category, Object
from smart_selects.form_fields import ChainedModelChoiceField

class EmailForm(forms.Form):
    email = forms.EmailField(label=u'Type Email')

'''
class CategoryForm(forms.Form):
	category = forms.ModelChoiceField(queryset=Category.objects.all())

class ListForm(forms.Form):
	choice = forms.ModelChoiceField(queryset=Object.objects.none())

	def __init__(self, *args, **kwargs):
		category = kwargs.pop('category')
		super(ListForm, self).__init__(*args, **kwargs)
		self.fields['choice'].queryset = Object.objects.filter(category = category)
'''

class ChoiceForm(forms.Form):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
	choice = ChainedModelChoiceField('lists', 'Object', 'category', 'category', 'lists', 'Object', 'category', False, False)

