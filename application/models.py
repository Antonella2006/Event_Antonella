from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Organisateurs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_org = models.CharField(max_length=100)
    mail_org = models.CharField(max_length=100, unique=True)
    mdp_org = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nom_org} - {self.mail_org}"

class Participant(models.Model):
    
    nom_user = models.CharField(max_length=100)
    mail_user = models.CharField(max_length=100)
    mdp_user = models.CharField(max_length=128)  

    def set_password(self, password):
        """Cette méthode utilise le hachage de mot de passe de Django"""
        self.mdp_user = make_password(password) 

    def __str__(self):
        return f"{self.nom_user} - {self.mail_user}"
    
class Evenement(models.Model):
    titre = models.CharField(max_length=50)
    lieu = models.CharField(max_length=70, null=True, blank=True)
    description = models.TextField()
    date_debut = models.DateField(default=now)
    date_fin = models.DateField(default=now)
    capacite = models.IntegerField(default=10)
    organisateur = models.ForeignKey(
        Organisateurs,
        on_delete=models.CASCADE,
        default=1,
        related_name='evenements_organises'
    )

    def __str__(self):
        return f"{self.titre} - {self.date_debut} à {self.date_fin} - {self.lieu}"

class Inscription(models.Model):
    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )
    date_inscription = models.DateTimeField(auto_now_add=True)  # Date et heure de l'inscription

    def __str__(self):
        return f"Inscription: {self.participant.nom_user} à {self.evenement.titre} - {self.date_inscription}"

class Notification(models.Model):
    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="L'événement pour lequel cette notification est envoyée."
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="Le participant qui reçoit cette notification."
    )
    organisateur = models.ForeignKey(
        Organisateurs,
        on_delete=models.CASCADE,
        related_name='notifications_envoyees',
        help_text="L'organisateur qui envoie cette notification."
    )
    titre = models.CharField(max_length=100, help_text="Titre de la notification.")
    message = models.TextField(help_text="Contenu de la notification.")
    date_envoi = models.DateTimeField(auto_now_add=True, help_text="Date et heure de l'envoi de la notification.")
    lu = models.BooleanField(default=False, help_text="Indique si la notification a été lue par le participant.")

    def __str__(self):
        return f"Notification: {self.titre} - {self.participant.nom_user} ({self.date_envoi})"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_envoi']
