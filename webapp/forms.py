from django import forms
from .models import UserFeedback, Order, User, Product
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class FAQForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rate = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label='Оцените работу сервиса', required=False)
    text = forms.CharField(max_length=1000, widget=forms.Textarea, label='Текст отзыва или вопрос, который Вы хотели бы задать', required=False)

    class Meta:
        model = UserFeedback
        fields = ['text', 'rate']


class ProductForm(forms.Form):
    material = forms.ChoiceField(choices=Product.get_materials(), label='Материал', initial=0)
    use_type = forms.ChoiceField(choices=Product.get_use_types(), label='Вид', initial=0)

    length = forms.IntegerField(min_value=40, max_value=700, validators=[], label='Длина, мм', initial=450)
    width = forms.IntegerField(min_value=40, max_value=700, validators=[], label='Ширина, мм', initial=350)
    height = forms.IntegerField(min_value=10, max_value=80, validators=[], label='Высота, мм', initial=40)

    handles = forms.BooleanField(widget=forms.CheckboxInput, label='Ручки', initial=True, required=False)
    legs = forms.BooleanField(widget=forms.CheckboxInput, label='Ножки', initial=False, required=False)
    groove = forms.BooleanField(widget=forms.CheckboxInput, label='Дренажный канал', initial=False, required=False)

    # Number of products in a given order
    number = forms.IntegerField(min_value=1, max_value=99, validators=[], label='', initial=1)

    price = forms.CharField(max_length=20, widget=forms.TextInput, validators=[], label='', initial='0.00', disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submitted = False
        self.cleaned_data = {}

class OrderForm(forms.Form):
    description = forms.CharField(max_length=1000, widget=forms.Textarea, label='Комментарий для мастера', required=False)
    delivery_type = forms.ChoiceField(choices=Order.get_delivery_types(), label='Способ получения заказа', initial=0)
    address = forms.CharField(max_length=500, widget=forms.Textarea, label='Адрес доставки', required=False)
    delivery_description = forms.CharField(max_length=1000, widget=forms.Textarea, label='Комментарий курьеру', required=False)
    delivery_price = forms.CharField(max_length=20, widget=forms.TextInput, validators=[], label='Стоимость доставки', disabled=True, initial='0.00')

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initial states
        self.fields['description'].widget.attrs.update({'placeholder': 'Детали заказа, которые Вам бы хотелось уточнить'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Адрес, по которому необходимо доставить заказ'})
        self.submitted = False
        self.cleaned_data = {}


class UserUpdateForm(forms.Form):
    help_text = 'Обязательное поле'
    name = forms.CharField(max_length=50, disabled=True, required=False)
    second_name = forms.CharField(max_length=50, disabled=True, required=False)
    last_name = forms.CharField(max_length=50, disabled=True, required=False)
    phone = forms.CharField(max_length=20, disabled=True)
    email = forms.CharField(max_length=50, disabled=True)

    pref_delivery_type = forms.ChoiceField(choices=User.get_delivery_types(), disabled=True)
    main_address = forms.CharField(max_length=150, disabled=True)
    birthdate = forms.DateField(label='', widget=forms.DateInput, disabled=True)

    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SignUpForm(forms.ModelForm):
    help_text = 'Обязательное поле'
    username = forms.CharField(max_length=20, help_text=help_text, label='Логин')
    password = forms.CharField(max_length=50, help_text=help_text, label='Пароль', widget=forms.PasswordInput)
    email = forms.CharField(max_length=150, help_text=help_text, label='Почта')
    phone = forms.CharField(max_length=20, help_text=help_text, label='Телефон')
    name = forms.CharField(max_length=50, help_text=help_text, label='Имя', validators=[])
    last_name = forms.CharField(max_length=50, help_text=help_text, label='Фамилия', validators=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_data = {}

    class Meta:
        success = False
        success_message = 'Регистрация прошла успешно!'
        model = User
        fields = ['username', 'password', 'name', 'email', 'phone', 'last_name']
        labels ={
            'username': 'Логин', 'password': 'Пароль', 'name': 'Имя',
            'last_name': 'Фамилия', 'email': 'Почта', 'phone': 'Телефон'
        }

    # DO form cleaning here
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Указанное имя пользователя уже используется')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Указанная почта уже используется")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Сheck password length
        if len(password) < 8:
            raise ValidationError("Длина пароля должна быть не менее 8 символов")
        # Сheck for number and letters is password
        if password.isalpha() or password.isnumeric():
            raise ValidationError("Пароль должен содержать цифры и буквы")

        return password

    def clean_phone(self):
        phone = self.cleaned_data.get('email')
        if phone == "":
            raise ValidationError("Обязательное поле")
        else:
            if User.objects.filter(phone=phone):
                raise ValidationError("Указанный номер телефона уже используется")
        return phone

    def clean(self):
        self.cleaned_data = super().clean()
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, label='Логин')
    password = forms.CharField(max_length=50, label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {'username': 'Логин', 'password': 'Пароль'}
