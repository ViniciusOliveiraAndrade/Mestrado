from django.contrib import admin
from .models import MDev, MProject, JiraIssues, Recommendation,Experiencia

# Register your models here.

admin.site.register(MDev)
admin.site.register(MProject)
admin.site.register(JiraIssues)
admin.site.register(Recommendation)
admin.site.register(Experiencia)