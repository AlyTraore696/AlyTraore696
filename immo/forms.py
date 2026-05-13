from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import ImageLogement, Locataire, LocationContrat, Logement, Profil, Proprietaire


class BootstrapMixin:
    def _apply_bootstrap(self):
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css = 'form-check-input'
            field.widget.attrs.setdefault('class', css)


class InscriptionForm(BootstrapMixin, UserCreationForm):
    ROLE_CHOICES = Profil.ROLE_CHOICES
    first_name = forms.CharField(label='Prénom', max_length=150)
    last_name = forms.CharField(label='Nom', max_length=150)
    email = forms.EmailField(label='Email')
    telephone = forms.CharField(label='Téléphone', max_length=30)
    adresse = forms.CharField(label='Adresse', max_length=255, required=False)
    role = forms.ChoiceField(label='Type de compte', choices=ROLE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'adresse', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Un compte existe déjà avec cet email.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profil.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                telephone=self.cleaned_data['telephone'],
                adresse=self.cleaned_data.get('adresse', ''),
            )
            nom = user.get_full_name() or user.username
            if self.cleaned_data['role'] == Profil.ROLE_PROPRIETAIRE:
                Proprietaire.objects.create(user=user, nom=nom, tel=self.cleaned_data['telephone'], adresse=self.cleaned_data.get('adresse', ''), email=user.email)
            else:
                Locataire.objects.create(user=user, nom=nom, tel=self.cleaned_data['telephone'], email=user.email)
        return user


class ProprietaireForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Proprietaire
        fields = ['nom', 'tel', 'adresse', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class ImageLogementForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = ImageLogement
        fields = ['photo', 'legende']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class LogementForm(BootstrapMixin, forms.ModelForm):
    photo = forms.ImageField(label='Photo du logement', required=False)
    legende = forms.CharField(label='Légende photo', max_length=160, required=False)

    class Meta:
        model = Logement
        fields = ['adresse', 'surface', 'loyer', 'caution', 'type', 'proprietaire', 'image', 'photo', 'legende', 'est_disponible']

    def __init__(self, *args, **kwargs):
        proprietaire = kwargs.pop('proprietaire', None)
        super().__init__(*args, **kwargs)
        if proprietaire:
            self.fields['proprietaire'].queryset = Proprietaire.objects.filter(pk=proprietaire.pk)
            self.fields['proprietaire'].initial = proprietaire
        self._apply_bootstrap()

    def save(self, commit=True):
        logement = super().save(commit=False)
        photo = self.cleaned_data.get('photo')
        legende = self.cleaned_data.get('legende', '')
        if photo:
            logement.image = ImageLogement.objects.create(photo=photo, legende=legende)
        if commit:
            logement.save()
            self.save_m2m()
        return logement


class LocataireForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Locataire
        fields = ['nom', 'tel', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class LocationContratForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = LocationContrat
        fields = ['locataire', 'logement', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        locataire = kwargs.pop('locataire', None)
        logement = kwargs.pop('logement', None)
        super().__init__(*args, **kwargs)
        self.fields['logement'].queryset = Logement.objects.filter(est_disponible=True)
        if locataire:
            self.fields['locataire'].queryset = Locataire.objects.filter(pk=locataire.pk)
            self.fields['locataire'].initial = locataire
        if logement:
            self.fields['logement'].queryset = Logement.objects.filter(pk=logement.pk, est_disponible=True)
            self.fields['logement'].initial = logement
        self._apply_bootstrap()

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        if date_debut and date_fin and date_fin <= date_debut:
            raise ValidationError('La date de fin doit être postérieure à la date de début.')
        return cleaned_data
