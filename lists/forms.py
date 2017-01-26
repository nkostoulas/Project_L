from django import forms
from .models import Object

class EmailForm(forms.Form):
    email = forms.EmailField(label=u'Type Email')

class ChoicesForm(forms.Form):
	choice_1 = forms.ModelChoiceField(queryset=Object.objects.all(), required=True)
	choice_2 = forms.ModelChoiceField(queryset=Object.objects.all(), required=True)
	choice_3 = forms.ModelChoiceField(queryset=Object.objects.all(), required=True)
	choice_4 = forms.ModelChoiceField(queryset=Object.objects.all(), required=True)
	choice_5 = forms.ModelChoiceField(queryset=Object.objects.all(), required=True)

	def clean(self):
		cleaned_data = super(ChoicesForm,self).clean()
		choice_1 = cleaned_data.get('choice_1')
		choice_2 = cleaned_data.get('choice_2')
		choice_3 = cleaned_data.get('choice_3')
		choice_4 = cleaned_data.get('choice_4')
		choice_5 = cleaned_data.get('choice_5')

		if choice_1 and choice_2 and choice_3 and choice_4 and choice_5:
			if choice_1==choice_2:
				self._errors['choice_2'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_2']
			elif choice_1==choice_3:
				self._errors['choice_3'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_3']
			elif choice_1==choice_4:
				self._errors['choice_4'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_4']
			elif choice_1==choice_5:
				self._errors['choice_5'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_5']
			elif choice_2==choice_3:
				self._errors['choice_3'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_3']
			elif choice_2==choice_4:
				self._errors['choice_4'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_4']
			elif choice_2==choice_5:
				self._errors['choice_5'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_5']
			elif choice_3==choice_4:
				self._errors['choice_4'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_4']
			elif choice_3==choice_5:
				self._errors['choice_5'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_5']
			elif choice_4==choice_5:
				self._errors['choice_5'] = self.error_class(['Choices must be unique'])
				del self.cleaned_data['choice_5']
		return cleaned_data