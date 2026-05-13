# ImmoGestion — Projet Django de gestion de location

ImmoGestion est une application Django complète pour gérer des locations immobilières avec trois profils :

- **Administrateur** : supervise tous les utilisateurs, propriétaires, locataires, logements et contrats de location.
- **Locataire** : crée son compte, consulte les logements disponibles et effectue une location.
- **Propriétaire** : crée son compte, ajoute ses maisons/logements et vérifie leur état ainsi que les locataires associés.

## Fonctionnalités

- Authentification et inscription multi-rôles.
- Dashboard administrateur avec statistiques et actions rapides.
- Dashboard propriétaire avec état des maisons et liste des occupants.
- Dashboard locataire avec locations en cours et logements disponibles.
- Gestion des propriétaires, logements, images, locataires et contrats de location.
- Templates professionnels Bootstrap 5.
- Configuration PostgreSQL via variables d'environnement.

## Modèle de données

Les tables principales sont :

- `Proprietaire` : `id`, `nom`, `tel`, `adresse`, `email`.
- `ImageLogement` : `id`, `photo`, `legende`.
- `Logement` : `id`, `adresse`, `surface`, `loyer`, `caution`, `type`, `proprietaire_id`, `image_id`, `est_disponible`.
- `Locataire` : `id`, `nom`, `tel`, `email`.
- `LocationContrat` : `id`, `locataire_id`, `logement_id`, `date_debut`, `date_fin`.
- `Profil` : rattache un utilisateur Django au rôle `locataire` ou `proprietaire`.

## Installation locale

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Créez ensuite la base PostgreSQL :

```bash
createdb gestion_location
```

Adaptez les variables `POSTGRES_*` dans `.env`, puis lancez :

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

L'application sera disponible sur <http://127.0.0.1:8000/>.

## Variables d'environnement PostgreSQL

```env
POSTGRES_DB=gestion_location
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

## Routes utiles

- `/` : page d'accueil.
- `/inscription/` : création de compte locataire ou propriétaire.
- `/connexion/` : connexion.
- `/dashboard/` : tableau de bord adapté au rôle.
- `/logements/` : catalogue des logements.
- `/admin/` : administration Django.
