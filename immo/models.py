from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profil(models.Model):
    ROLE_LOCATAIRE = 'locataire'
    ROLE_PROPRIETAIRE = 'proprietaire'
    ROLE_CHOICES = [
        (ROLE_LOCATAIRE, 'Locataire'),
        (ROLE_PROPRIETAIRE, 'Propriétaire'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=30, blank=True)
    adresse = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} - {self.get_role_display()}'


class Proprietaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fiche_proprietaire')
    nom = models.CharField(max_length=150)
    tel = models.CharField(max_length=30)
    adresse = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class ImageLogement(models.Model):
    photo = models.ImageField(upload_to='logements/')
    legende = models.CharField(max_length=160, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.legende or self.photo.name


class Logement(models.Model):
    TYPE_APPARTEMENT = 'Appartement'
    TYPE_STUDIO = 'Studio'
    TYPE_VILLA = 'Villa'
    TYPE_BUREAU = 'Bureau'
    TYPE_CHOICES = [
        (TYPE_APPARTEMENT, 'Appartement'),
        (TYPE_STUDIO, 'Studio'),
        (TYPE_VILLA, 'Villa'),
        (TYPE_BUREAU, 'Bureau'),
    ]

    adresse = models.CharField(max_length=255)
    surface = models.FloatField(help_text='Surface en m²')
    loyer = models.PositiveIntegerField(help_text='Loyer mensuel')
    caution = models.PositiveIntegerField(help_text='Montant de la caution')
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, related_name='logements')
    image = models.ForeignKey(ImageLogement, on_delete=models.SET_NULL, null=True, blank=True, related_name='logements')
    est_disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f'{self.type} - {self.adresse}'

    def get_absolute_url(self):
        return reverse('logement_detail', args=[self.pk])


class Locataire(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fiche_locataire')
    nom = models.CharField(max_length=150)
    tel = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class LocationContrat(models.Model):
    locataire = models.ForeignKey(Locataire, on_delete=models.CASCADE, related_name='locations')
    logement = models.ForeignKey(Logement, on_delete=models.CASCADE, related_name='locations')
    date_debut = models.DateField()
    date_fin = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_debut']
        constraints = [
            models.CheckConstraint(condition=models.Q(date_fin__gt=models.F('date_debut')), name='date_fin_apres_date_debut'),
        ]

    def __str__(self):
        return f'{self.locataire} loue {self.logement}'
