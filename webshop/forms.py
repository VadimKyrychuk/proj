from .models import Order
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_date'].label = _('Дата получения заказа')

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'adress', 'buy_type', 'order_date', 'comment')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Логин')
        self.fields['password'].label = _('Пароль')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError (_('Пользователь с логином ') +  username + _(' не найден'))
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(_('Неверный пароль'))
        return self.cleaned_data

class Registration(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password','first_name','last_name','adress', 'phone', 'email']


    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    adress = forms.CharField(required=False)
    email = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Логин')
        self.fields['password'].label = _('Пароль')

        self.fields['confirm_password'].label = _('Подтвердите пароль')
        self.fields['first_name'].label = _('Имя')
        self.fields['last_name'].label = _('Фамилия')
        self.fields['phone'].label = _('Номер телефона')
        self.fields['adress'].label = _('Адресс')
        self.fields['email'].label = _('Ел. почта')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Почтовый адрес уже испоользуется'))
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Данный логин уже используется'))
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError(_('Пароли не совпадают'))
        return self.cleaned_data
