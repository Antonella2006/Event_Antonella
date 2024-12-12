from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('authentification_organisateur/', views.authentification_organisateur, name='authentification_organisateur'),
    path('about/', views.about, name='about'),
    path('create_evenement/', views.create_evenement, name='create_evenement'),
    path('add_organisateur/', views.add_organisateur, name='add_organisateur'),
    path('pageAdmin/', views.pageAdmin, name='pageAdmin'),
    path('inscri_event/', views.inscri_event, name='inscri_event'),
    path('organisateurs/', views.liste_organisateurs, name='liste_organisateurs'),
    path('liste_evenements/', views.liste_evenements, name='liste_evenements'),
    path('supprimer_evenement/<int:id>/', views.supprimer_evenement, name='supprimer_evenement'),
    path('modifier_evenement/<int:id>/', views.modifier_evenement, name='modifier_evenement'),
    path('supprimer_organisateur/<int:id>/', views.supprimer_organisateur, name='supprimer_organisateur'),
    path('modifier_organisateur/<int:id>/', views.modifier_organisateur, name='modifier_organisateur'),
    path('login/', views.login_participant, name='login_participant'),
    path('evenements/inscrire/<int:evenement_id>/', views.inscrire_evenement, name='inscrire_evenement'),
    path('create-participant/', views.create_participant_account, name='create_participant'),
     path('inscriptions/', views.listes_inscriptions, name='listes_inscriptions'),
     path('deconnexion/',  auth_views.LogoutView.as_view(next_page='home'), name='deconnexion'),
     path('envoyer_rappel', views.Envoyer_rappel, name='envoyer_rappel'),
     path('inscription/<int:inscription_id>/rappel/', views.envoyer_rappel, name='envoyer_rappel'),
      path('notifications/', views.notifications, name='notifications'),
    path('', views.connecter, name='connecter'),
]
