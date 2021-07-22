from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile, Post, Comment
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core import validators


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        label="Nazwa użytkownika",
        strip=False,
        help_text="\nDo 150 znaków. Tylko litery, cyfry i znaki @/./+/-/_ .",
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                ('Nazwa użytkownika zawiera niedozwolony znak!')
            ),
        ],

    )
    password1 = forms.CharField(
        label="Hasło",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Hasło nie może być powiązane z nazwą użytkownika. \n"
                  "Hasło musi posiadać przynajmniej 8 znaków. \n"
                  "Hasło nie może być powszechnym hasłem. \n"
                  "Hasło nie może się składać z samych cyfr. "
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Wpisz takie samo hasło co wcześniej w celu weryfikacji"
    )
    desc = forms.CharField(
        label="Własny opis",
        strip=False,
        widget=forms.Textarea
    )
    ROLES = (
        ('R', 'Redaktor'),
        ('C', 'Czytelnik')
    )
    role = forms.ChoiceField(
        label="Rola na portalu",
        widget=forms.RadioSelect,
        choices=ROLES
    )

    def __init__(self, *args, **kwargs):
        self.error_messages['password_mismatch'] = 'Hasła się nie zgadzają!'
        super().__init__(*args, **kwargs)

    error_messages = {
        'duplicate_username': 'Ta nazwa posiada niedozwolone znaki lub jest już użyta'
    }

    class Meta:
        model = UserProfile
        fields = ['username', 'desc', 'role']

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            UserProfile._default_manager.get(username=username)
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )
        except UserProfile.DoesNotExist:
            return username


class CreatePost(forms.ModelForm):
    title = forms.CharField(
        label="Tytuł artykułu",
        strip=False,
    )
    main_text = forms.CharField(
        label="Treść artykułu",
        strip=False,
        widget=forms.Textarea
    )
    tags = forms.CharField(
        label="Słowa klucze",
        strip=False,
        widget=forms.Textarea(attrs={"rows":5, "cols":20})
    )

    class Meta:
        model = Post
        fields = ['title', 'main_text', 'tags']


class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(
        label="Treść komentarza:",
        strip=False,
        widget=forms.Textarea(attrs={"rows":5, "cols":20})
    )

    class Meta:
        model = Comment
        fields = ['comment_text']


Rat = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
)


class RateForm(forms.Form):

    rate = forms.TypedChoiceField(
        choices=Rat,
        widget=forms.RadioSelect,
        label="Ocena:"
    )

    class Meta:
        fields = ['rate']


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Nazwa użytkownika',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Hasło",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Błędny dane logowania. Pamiętaj o wielkich literach!'
        super().__init__(*args, **kwargs)
