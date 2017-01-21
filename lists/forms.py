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
	choice_1 = ChainedModelChoiceField('lists', 'Object', 'category', 'category', 'lists', 'Object', 'category', False, False
										,widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))
	choice_2 = ChainedModelChoiceField('lists', 'Object', 'category', 'category', 'lists', 'Object', 'category', False, False)
										#,widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))

class CategoryForm(forms.Form):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))

class ChoicesForm(forms.Form):
	choice_1 = forms.ModelChoiceField(queryset=Object.objects.all(), required=True)
	choice_2 = forms.ModelChoiceField(queryset=Object.objects.all(), required=True)
	
	def clean(self):
		cleaned_data = super(ChoicesForm,self).clean()
		choice_1 = cleaned_data.get('choice_1')
		choice_2 = cleaned_data.get('choice_2')
		if choice_1 and choice_2 and choice_1==choice_2:
			self._errors['choice_2'] = self.error_class(['Choices must be unique'])
			del self.cleaned_data['choice_2']
		return cleaned_data