from django import forms
from .models import Evenement,Organisateurs, Participant, Inscription

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'lieu', 'description', 'date_debut', 'date_fin', 'capacite'] 

class AuthentificationForm(forms.Form):
    mail_org = forms.EmailField(label='Email', max_length=100)
    mdp_org = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    
class OrganisateurForm(forms.ModelForm):
    class Meta:
        model = Organisateurs
        fields = ['nom_org', 'mail_org', 'mdp_org']
        labels = {
            'nom_org': "Nom",
            'mail_org': "Email",
            'mdp_org': "Mot de passe",
        }

        
class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['nom_user', 'mail_user', 'mdp_user']

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['evenement']  

class ParticipantLoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class ParticipantCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label="Mot de passe"
    )

    class Meta:
        model = Participant
        fields = ['nom_user', 'mail_user'] 
        labels = {
            'nom_user': "Nom",
            'mail_user': "Email",
        }

    def save(self, commit=True):
        participant = super().save(commit=False)
        participant.set_password(self.cleaned_data['password'])
        if commit:
            participant.save()
        return participant
    

class NotificationForm(forms.Form):
    titre = forms.CharField(max_length=100, label="Titre de la notification")
    message = forms.CharField(widget=forms.Textarea, label="Message")
