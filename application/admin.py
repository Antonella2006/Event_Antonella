from django.contrib import admin
from .models import Organisateurs,Evenement,Participant,Inscription
admin.site.register(Organisateurs)
admin.site.register(Evenement)
admin.site.register(Participant)
admin.site.register(Inscription)