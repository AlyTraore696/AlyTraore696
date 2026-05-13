from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import InscriptionForm, LocationContratForm, LogementForm, ProprietaireForm
from .models import Locataire, LocationContrat, Logement, Profil, Proprietaire


def is_admin(user):
    return user.is_authenticated and user.is_staff


def is_proprietaire(user):
    return user.is_authenticated and hasattr(user, 'profil') and user.profil.role == Profil.ROLE_PROPRIETAIRE


def home(request):
    logements = Logement.objects.select_related('proprietaire', 'image').filter(est_disponible=True)[:6]
    stats = {
        'logements': Logement.objects.count(),
        'proprietaires': Proprietaire.objects.count(),
        'locations': LocationContrat.objects.count(),
    }
    return render(request, 'immo/home.html', {'logements': logements, 'stats': stats})


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès.')
            return redirect('dashboard')
    else:
        form = InscriptionForm()
    return render(request, 'immo/inscription.html', {'form': form})


@login_required
def dashboard(request):
    context = {'today': timezone.now().date()}
    if request.user.is_staff:
        context.update({
            'role_label': 'Administrateur',
            'total_users': User.objects.count(),
            'total_proprietaires': Proprietaire.objects.count(),
            'total_logements': Logement.objects.count(),
            'total_locations': LocationContrat.objects.count(),
            'recent_locations': LocationContrat.objects.select_related('locataire', 'logement', 'logement__proprietaire')[:6],
            'logements': Logement.objects.select_related('proprietaire', 'image')[:8],
        })
        return render(request, 'immo/dashboard_admin.html', context)

    if is_proprietaire(request.user):
        proprietaire = get_object_or_404(Proprietaire, user=request.user)
        logements = Logement.objects.select_related('image').filter(proprietaire=proprietaire)
        context.update({
            'role_label': 'Propriétaire',
            'proprietaire': proprietaire,
            'logements': logements,
            'locations': LocationContrat.objects.select_related('locataire', 'logement').filter(logement__proprietaire=proprietaire),
        })
        return render(request, 'immo/dashboard_proprietaire.html', context)

    locataire = get_object_or_404(Locataire, user=request.user)
    context.update({
        'role_label': 'Locataire',
        'locataire': locataire,
        'locations': LocationContrat.objects.select_related('logement', 'logement__proprietaire').filter(locataire=locataire),
        'logements': Logement.objects.select_related('proprietaire', 'image').filter(est_disponible=True)[:6],
    })
    return render(request, 'immo/dashboard_locataire.html', context)


def logement_list(request):
    logements = Logement.objects.select_related('proprietaire', 'image').all()
    type_filter = request.GET.get('type')
    if type_filter:
        logements = logements.filter(type=type_filter)
    return render(request, 'immo/logement_list.html', {'logements': logements, 'types': Logement.TYPE_CHOICES})


def logement_detail(request, pk):
    logement = get_object_or_404(Logement.objects.select_related('proprietaire', 'image'), pk=pk)
    return render(request, 'immo/logement_detail.html', {'logement': logement})


@login_required
@user_passes_test(lambda user: user.is_staff or is_proprietaire(user))
def logement_create(request):
    proprietaire = None
    if is_proprietaire(request.user) and not request.user.is_staff:
        proprietaire = get_object_or_404(Proprietaire, user=request.user)
    if request.method == 'POST':
        form = LogementForm(request.POST, request.FILES, proprietaire=proprietaire)
        if form.is_valid():
            form.save()
            messages.success(request, 'Logement ajouté avec succès.')
            return redirect('dashboard')
    else:
        form = LogementForm(proprietaire=proprietaire)
    return render(request, 'immo/form.html', {'form': form, 'title': 'Ajouter un logement'})


@login_required
@user_passes_test(lambda user: user.is_staff or is_proprietaire(user))
def logement_update(request, pk):
    logement = get_object_or_404(Logement, pk=pk)
    if is_proprietaire(request.user) and logement.proprietaire.user != request.user and not request.user.is_staff:
        messages.error(request, "Vous ne pouvez modifier que vos propres logements.")
        return redirect('dashboard')
    if request.method == 'POST':
        form = LogementForm(request.POST, request.FILES, instance=logement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Logement mis à jour avec succès.')
            return redirect('dashboard')
    else:
        form = LogementForm(instance=logement)
    return render(request, 'immo/form.html', {'form': form, 'title': 'Modifier un logement'})


@login_required
def location_create(request, pk):
    logement = get_object_or_404(Logement, pk=pk, est_disponible=True)
    if is_proprietaire(request.user):
        messages.error(request, 'Un propriétaire ne peut pas louer son propre logement avec ce compte.')
        return redirect('logement_detail', pk=pk)
    locataire = get_object_or_404(Locataire, user=request.user)
    if request.method == 'POST':
        form = LocationContratForm(request.POST, locataire=locataire, logement=logement)
        if form.is_valid():
            contrat = form.save()
            contrat.logement.est_disponible = False
            contrat.logement.save(update_fields=['est_disponible'])
            messages.success(request, 'Votre location a été enregistrée.')
            return redirect('dashboard')
    else:
        form = LocationContratForm(locataire=locataire, logement=logement)
    return render(request, 'immo/form.html', {'form': form, 'title': f'Louer {logement.type}'})


@login_required
@user_passes_test(is_admin)
def proprietaire_list(request):
    proprietaires = Proprietaire.objects.all()
    return render(request, 'immo/proprietaire_list.html', {'proprietaires': proprietaires})


@login_required
@user_passes_test(is_admin)
def proprietaire_create(request):
    if request.method == 'POST':
        form = ProprietaireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Propriétaire enregistré.')
            return redirect('proprietaire_list')
    else:
        form = ProprietaireForm()
    return render(request, 'immo/form.html', {'form': form, 'title': 'Ajouter un propriétaire'})


@login_required
@user_passes_test(is_admin)
def locataire_list(request):
    locataires = Locataire.objects.all()
    return render(request, 'immo/locataire_list.html', {'locataires': locataires})


@login_required
def location_list(request):
    if request.user.is_staff:
        locations = LocationContrat.objects.select_related('locataire', 'logement', 'logement__proprietaire')
    elif is_proprietaire(request.user):
        locations = LocationContrat.objects.select_related('locataire', 'logement').filter(logement__proprietaire__user=request.user)
    else:
        locations = LocationContrat.objects.select_related('logement', 'logement__proprietaire').filter(locataire__user=request.user)
    return render(request, 'immo/location_list.html', {'locations': locations})
