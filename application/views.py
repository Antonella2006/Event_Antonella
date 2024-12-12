from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import  redirect
from .forms import  EvenementForm, OrganisateurForm, NotificationForm
from .models import Organisateurs
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Evenement, Organisateurs, Participant, Inscription, Notification
from .forms import EvenementForm,ParticipantLoginForm, ParticipantCreationForm
from django.core.mail import send_mail
from django.contrib.auth.models import AnonymousUser

def home(request):
    evenements = Evenement.objects.all()
    print(evenements)
    return render(request, 'home.html', {'evenements': evenements})

def authentification_organisateur(request):
    if request.method == "POST":
        email = request.POST.get('mail_org')
        password = request.POST.get('mdp_org')
        try:
            organisateur = Organisateurs.objects.get(mail_org=email)
            if organisateur.mdp_org == password:
                return redirect('create_evenement') 
            else:
                error = "Mot de passe incorrect"
        except Organisateurs.DoesNotExist:
            error = "Adresse email non reconnue"
        
        return render(request, 'authentification_organisateur.html', {'error': error})

    return render(request, 'authentification_organisateur.html')


def about(request):
    return render(request, 'about.html')

def pageAdmin(request):
    evenements = Evenement.objects.all() 
    return render(request, 'pageAdmin.html', {'evenements': evenements})


def inscri_event(request):
    return render(request, 'inscri_event.html')

@login_required
def create_evenement(request):
    if request.method == "POST":
        form = EvenementForm(request.POST)
        if form.is_valid():
            evenement = form.save(commit=False)

            # Récupérer ou créer un organisateur pour l'utilisateur connecté
            organisateur, created = Organisateurs.objects.get_or_create(user=request.user)
            
            # Assigner l'organisateur à l'événement
            evenement.organisateur = organisateur
            evenement.save()

            messages.success(request, "Événement créé avec succès.")
            return redirect('liste_evenements')  # Redirige vers la liste des événements
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = EvenementForm()

    return render(request, 'create_evenement.html', {'form': form})

def add_organisateur(request):
    if request.method == "POST":
        form = OrganisateurForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom_org']
            email = form.cleaned_data['mail_org']
            password = form.cleaned_data['mdp_org']
            user = User.objects.create_user(username=email, email=email, password=password)
            organisateur = form.save(commit=False)
            organisateur.user = user
            organisateur.save()

            return redirect('authentification_organisateur')
    else:
        form = OrganisateurForm()

    return render(request, 'add_organisateur.html', {'form': form})

def liste_organisateurs(request):
    organisateurs = Organisateurs.objects.all()
    return render(request, 'liste_organisateurs.html', {'organisateurs': organisateurs})

def liste_evenements(request):
    evenements = Evenement.objects.all() 
    return render(request, 'liste_evenements.html', {'evenements': evenements})

def inscri_event(request):
    evenements = Evenement.objects.all() 
    return render(request, 'inscri_event.html', {'evenements': evenements})

def supprimer_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    try:
        organisateur = Organisateurs.objects.get(user=request.user)
        if evenement.organisateur == organisateur:
            evenement.delete()
            return redirect('liste_evenements') 
        else:
            return render(request, 'erreur.html', {
                'message': "Vous n'êtes pas autorisé à supprimer cet événement."
            })
    except Organisateurs.DoesNotExist:
        return render(request, 'erreur.html', {
            'message': "Vous n'êtes pas un organisateur."
        })

def supprimer_organisateur(request, id):
    organisateur = get_object_or_404(Organisateurs, id=id)
    if request.method == "POST":
        organisateur.delete()
        messages.success(request, "Organisateur supprimé avec succès.")
        return redirect('liste_organisateurs')
    return redirect('liste_organisateurs')

def modifier_organisateur(request, id):
    organisateur = get_object_or_404(Organisateurs, id=id)
    if request.method == 'POST':
        form = OrganisateurForm(request.POST, instance=organisateur)
        if form.is_valid():
            form.save()
            messages.success(request, "Organisateur modifié avec succès.")
            return redirect('liste_organisateurs')  
    else:
        form = OrganisateurForm(instance=organisateur)
    return render(request, 'modifier_organisateur.html', {'form': form})

def modifier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    if request.method == 'POST':
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            form.save()
            return redirect('liste_evenements')
    else:
        form = EvenementForm(instance=evenement)

    return render(request, 'modifier_evenement.html', {'form': form, 'evenement': evenement})

def login_participant(request):
    if request.method == "POST":
        form = ParticipantLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                participant = Participant.objects.get(mail_user=email)
                if participant.mdp_user == password:
                    request.session['participant_id'] = participant.id
                    return redirect('home')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Participant.DoesNotExist:
                messages.error(request, "Aucun compte trouvé avec cet email.")
    else:
        form = ParticipantLoginForm()
    return render(request, 'login_participant.html', {'form': form})


def inscrire_evenement(request, evenement_id):
    if 'participant_id' not in request.session:
        messages.error(request, "Veuillez vous connecter pour vous inscrire.")
        return redirect('login_participant')

    participant = Participant.objects.get(id=request.session['participant_id'])
    evenement = get_object_or_404(Evenement, id=evenement_id)

    # Vérifier si le participant est déjà inscrit
    if Inscription.objects.filter(evenement=evenement, participant=participant).exists():
        messages.warning(request, "Vous êtes déjà inscrit à cet événement.")
    else:
        Inscription.objects.create(evenement=evenement, participant=participant)
        messages.success(request, f"Inscription réussie à l'événement : {evenement.titre}")
    return redirect('inscri_event')

def create_participant_account(request):
    if request.method == "POST":
        form = ParticipantCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_participant')
    else:
        form = ParticipantCreationForm()

    return render(request, 'create_participant.html', {'form': form})

def listes_inscriptions(request):
    inscriptions = Inscription.objects.select_related('participant', 'evenement').all()
    return render(request, 'listes_inscriptions.html', {'inscriptions': inscriptions})

def Envoyer_rappel(request):
    inscriptions = Inscription.objects.select_related('participant', 'evenement').all()
    return render(request, 'Envoyer_rappel.html', {'inscriptions': inscriptions})

@login_required
def envoyer_rappel(request, inscription_id):
    if request.method == "POST":
        inscription = get_object_or_404(Inscription, id=inscription_id)

        # Contenu de l'email
        sujet = f"Rappel : {inscription.evenement.titre}"
        message = (
            f"Bonjour {inscription.participant.nom_user},\n\n"
            f"Ceci est un rappel pour l'événement '{inscription.evenement.titre}' "
            f"qui aura lieu du {inscription.evenement.date_debut} au {inscription.evenement.date_fin} "
            f"à {inscription.evenement.lieu}.\n\n"
            "Merci de votre participation !\n"
            "L'équipe de Gestion d'Événements."
        )
        destinataire = inscription.participant.mail_user

        # Envoi de l'email
        try:
            send_mail(
                sujet,
                message,
                'noreply@gestionevent.com', 
                [destinataire],
            )

            # Création de la notification
            Notification.objects.create(
                evenement=inscription.evenement,
                participant=inscription.participant,
                organisateur=inscription.evenement.organisateur,
                titre=sujet,
                message=message
            )

            messages.success(request, f"Rappel envoyé et notification créée pour {inscription.participant.nom_user}.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi du rappel : {str(e)}")

        return redirect('envoyer_rappel')
    
def envoyer_rappel(request, inscription_id):
    if request.method == "POST":
        inscription = get_object_or_404(Inscription, id=inscription_id)
        
        message = (
            f"Ceci est un rappel pour l'événement '{inscription.evenement.titre}' "
            f"qui aura lieu du {inscription.evenement.date_debut} au {inscription.evenement.date_fin} "
            f"à {inscription.evenement.lieu}.\n\n"
            "Merci de votre participation !"
        )
        notification = Notification(
            evenement=inscription.evenement,
            participant=inscription.participant,
            organisateur=inscription.evenement.organisateur,  
            titre=f"Rappel : {inscription.evenement.titre}",
            message=message
        )
        notification.save()
        messages.success(request, f"Rappel envoyé sous forme de notification à {inscription.participant.nom_user}.")

        return redirect('listes_inscriptions')
    
@login_required
def notifications(request):
    try:
        # Vérifiez si l'utilisateur est un participant
        participant = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        # Si l'utilisateur n'est pas un participant, redirigez-le
        messages.error(request, "Vous devez être un participant pour accéder aux notifications.")
        return redirect('login_participant')  # Remplacez 'home' par la page où vous souhaitez rediriger
    
    # Récupérez les notifications du participant
    notifications = Notification.objects.filter(participant=participant)
    return render(request, 'notifications.html', {'notifications': notifications})

def connecter(request):
    return render(request, 'connecter.html')
