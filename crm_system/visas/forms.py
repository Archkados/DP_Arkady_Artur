from django import forms
from .models import *
from django.contrib.auth.models import User, Group

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль" 
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Группа" 
    )
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'group']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Адрес почты',
        }
        help_texts = {
    'username': ''
    }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            self.cleaned_data['group'].user_set.add(user)
        return user
    
class CustomUserEditForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", required=False, widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
        label="Группы"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'groups']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Адрес почты',
        }
        help_texts = {
        'username': ''
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m() 
        return user

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['full_name']

class CarNumberForm(forms.ModelForm):
    class Meta:
        model = CarNumber
        fields = ['number']

class TrailerNumberForm(forms.ModelForm):
    car_number = forms.ModelChoiceField(queryset=CarNumber.objects.all(), required=False, empty_label="Не привязан", label="Выберите машину")

    class Meta:
        model = TrailerNumber
        fields = ['number', 'car_number']


class VisaForm(forms.ModelForm):
    class Meta:
        model = Visa
        fields = ['person', 'visa_issue_date', 'visa_expiry_date']
        widgets = {
            'visa_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'visa_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TruckInsuranceForm(forms.ModelForm):
    class Meta:
        model = TruckInsurance
        fields = ['truck_number', 'insurance_issue_date', 'insurance_expiry_date']
        widgets = {
            'insurance_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'insurance_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TrailerInsuranceForm(forms.ModelForm):
    class Meta:
        model = TrailerInsurance
        fields = ['trailer_number', 'insurance_issue_date', 'insurance_expiry_date']
        widgets = {
            'insurance_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'insurance_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TruckInspectionForm(forms.ModelForm):
    class Meta:
        model = TruckInspection
        fields = ['truck_number', 'inspection_issue_date', 'inspection_expiry_date']
        widgets = {
            'inspection_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'inspection_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TrailerInspectionForm(forms.ModelForm):
    class Meta:
        model = TrailerInspection
        fields = ['trailer_number', 'inspection_issue_date', 'inspection_expiry_date']
        widgets = {
            'inspection_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'inspection_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }




class ShippingApplicationForm(forms.ModelForm):
    loading_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    freight_cost = forms.DecimalField(
        widget=forms.TextInput(attrs={'type': 'text'}),
        max_digits=15,
        decimal_places=2,
        label="Стоимость фрахта"
    )
    insurance = forms.ChoiceField(
        choices=[(True, "Да"), (False, "Нет")],
        widget=forms.RadioSelect,
        label="Страхование груза"
    )
    class Meta:
        model = ShippingApplication
        fields = [
            'consignee', 'loading_address', 'sender_contact', 'loading_date',
            'route', 'cargo_name', 'cargo_details', 'freight_cost', 'insurance'
        ]
        widgets = {
            'consignee': forms.Textarea(attrs={'readonly': True}),
            'loading_address': forms.Textarea(attrs={'readonly': True}),
            'sender_contact': forms.Textarea(attrs={'readonly': True}),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

class SubCompanyForm(forms.ModelForm):
    class Meta:
        model = SubCompany
        fields = ['name']

class SubCompanyDataForm(forms.ModelForm):
    class Meta:
        model = SubCompany
        fields = ['consignee_info', 'loading_address', 'sender_contact_info']

class FreightCompanyForm(forms.ModelForm):
    class Meta:
        model = FreightCompany
        fields = ['name', 'contact_info']

class TrackingRequestForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(
        queryset=CarNumber.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Выберите машину"
    )
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label="Дата выезда"
    )

    class Meta:
        model = TrackingRequest
        fields = ['vehicle', 'status', 'departure', 'destination', 'departure_date']
        labels = {
            'status': 'Статус',
            'departure': 'Место отправки',
            'destination': 'Место получения',
            'departure_date': 'Дата выезда',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'departure': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
        }
