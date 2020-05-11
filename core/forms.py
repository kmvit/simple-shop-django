from django import forms

PAYMENT_CHOICES = (
	('Y', 'Яндекс касса'),
	('C','Наличными'),
)

class CheckoutForm(forms.Form):
	city = forms.CharField(widget=forms.TextInput(attrs={
			'placeholder':'г.Пятигорск'
	}))
	street_address = forms.CharField(widget=forms.TextInput(attrs={
			'placeholder':'Ул.Зеленая д.15'
	}))
	zip = forms.CharField(widget=forms.TextInput(attrs={
			'class':'fdf'
	}))
	name = forms.CharField()
	phone = forms.CharField(widget=forms.TextInput(attrs={
			'placeholder':'+7928010101'
	}))
	save_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
	save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput())
	payment_option = forms.ChoiceField(
		widget=forms.RadioSelect(),
		choices=PAYMENT_CHOICES
	)


