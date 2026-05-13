# Generated manually for the initial ImmoGestion schema.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLogement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='logements/')),
                ('legende', models.CharField(blank=True, max_length=160)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Locataire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('tel', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fiche_locataire', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['nom']},
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('locataire', 'Locataire'), ('proprietaire', 'Propriétaire')], max_length=20)),
                ('telephone', models.CharField(blank=True, max_length=30)),
                ('adresse', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proprietaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('tel', models.CharField(max_length=30)),
                ('adresse', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fiche_proprietaire', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['nom']},
        ),
        migrations.CreateModel(
            name='Logement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=255)),
                ('surface', models.FloatField(help_text='Surface en m²')),
                ('loyer', models.PositiveIntegerField(help_text='Loyer mensuel')),
                ('caution', models.PositiveIntegerField(help_text='Montant de la caution')),
                ('type', models.CharField(choices=[('Appartement', 'Appartement'), ('Studio', 'Studio'), ('Villa', 'Villa'), ('Bureau', 'Bureau')], max_length=40)),
                ('est_disponible', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logements', to='immo.imagelogement')),
                ('proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logements', to='immo.proprietaire')),
            ],
            options={'ordering': ['-date_creation']},
        ),
        migrations.CreateModel(
            name='LocationContrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('locataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='immo.locataire')),
                ('logement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='immo.logement')),
            ],
            options={'ordering': ['-date_debut']},
        ),
        migrations.AddConstraint(
            model_name='locationcontrat',
            constraint=models.CheckConstraint(condition=models.Q(('date_fin__gt', models.F('date_debut'))), name='date_fin_apres_date_debut'),
        ),
    ]
