from django.db import models


# Create your models here.
class MProject(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " - " + ("Ativo" if self.status else "Inativo")


class MDev(models.Model):
    project = models.ForeignKey(MProject, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=150)


class JiraIssues(models.Model):
    storyPoint = models.IntegerField(default=1)
    key = models.CharField(max_length=15)
    description = models.TextField(blank=False)
    feature = models.CharField(max_length=100)
    title = models.CharField(max_length=250)


class Recommendation(models.Model):
    issue = models.ForeignKey(JiraIssues, on_delete=models.CASCADE)
    dev = models.ForeignKey(MDev, on_delete=models.CASCADE)
