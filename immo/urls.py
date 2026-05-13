from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', auth_views.LoginView.as_view(template_name='immo/login.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logements/', views.logement_list, name='logement_list'),
    path('logements/<int:pk>/', views.logement_detail, name='logement_detail'),
    path('logements/ajouter/', views.logement_create, name='logement_create'),
    path('logements/<int:pk>/modifier/', views.logement_update, name='logement_update'),
    path('logements/<int:pk>/louer/', views.location_create, name='location_create'),
    path('proprietaires/', views.proprietaire_list, name='proprietaire_list'),
    path('proprietaires/ajouter/', views.proprietaire_create, name='proprietaire_create'),
    path('locataires/', views.locataire_list, name='locataire_list'),
    path('locations/', views.location_list, name='location_list'),
]
