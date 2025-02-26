from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Movie,Theatre, Ticket



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster_url']
        # widgets = {
        #     'poster_url': forms.URLInput(attrs={'class': 'form-control'}),
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        # }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # Update the attributes for better styling
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('username', 'password')

class MoviedetailsForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__' 
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter movie title'}),
            'poster_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter poster URL'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter director name'}),
            'screenplay': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter screenplay writer'}),
            'dialogues': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dialogue writers'}),
            'production': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter producers'}),
            'cast': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter main cast'}),
            'cinematography': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cinematographer'}),
            'editor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter editor'}),
            'music': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter music director'}),
            'production_companies': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter production companies'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'running_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter running time in minutes'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter language'}),
        }
class TheatreForm(forms.ModelForm):
    class Meta:
        model = Theatre
        fields = ['name', 'location', 'show_time']
        widgets = {
            'name': forms.RadioSelect
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class SeatSelectionForm(forms.Form):
    seat_id = forms.IntegerField(widget=forms.HiddenInput())  # Stores the selected seat's ID
    show_time = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    number_of_tickets = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        # Extract show_time_choices from kwargs if provided
        show_time_choices = kwargs.pop('show_time_choices', [])
        super().__init__(*args, **kwargs)
        
        # Update the show_time field with provided choices
        self.fields['show_time'].choices = show_time_choices

        # Update widget attributes
        self.fields['show_time'].widget.attrs.update({'class': 'form-control'})
        self.fields['number_of_tickets'].widget.attrs.update({'class': 'form-control'})

        
class BookTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['user', 'movie', 'theatre', 'seat', 'show_time']
        widgets = {
            'user': forms.TextInput(attrs={'readonly': 'readonly'}),
            'movie': forms.TextInput(attrs={'readonly': 'readonly'}),
            'theatre': forms.TextInput(attrs={'readonly': 'readonly'}),
            'seat': forms.TextInput(attrs={'readonly': 'readonly'}),
            'show_time': forms.TextInput(attrs={'readonly': 'readonly'}),
        }