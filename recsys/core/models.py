from django.db import models


# Create your models here.
class Linguagem(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class MProject(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    linguagens = models.ManyToManyField(Linguagem, default=None, blank=True)

    def __str__(self):
        return self.name + " - " + ("Ativo" if self.status else "Inativo")


class MDev(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=150)
    id_jira = models.CharField(max_length=50, default="ID não definido")
    linguagens = models.ManyToManyField(Linguagem, default=None, blank=True)

    def __str__(self):
        return self.name

class Squad(models.Model):
    nome = models.CharField(max_length=100)
    sprint = models.CharField(max_length=3)
    projeto = models.ForeignKey(MProject, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome + " - " + self.projeto.name


class AlocacaoP(models.Model):
    projeto = models.ForeignKey(MProject, on_delete=models.CASCADE)
    dev = models.ForeignKey(MDev, on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.projeto.name + " - " + self.dev.name

class Termo(models.Model):
    palavra = models.CharField(max_length=25)
    quantidade = models.IntegerField(default=0)

class JiraIssues(models.Model):
    storyPoint = models.IntegerField(default=1)
    key = models.CharField(max_length=15)
    description = models.TextField(blank=False)
    feature = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    dev = models.ForeignKey(MDev, on_delete=models.CASCADE, default=None, blank=True, null=True)
    prioridade = models.CharField(max_length=20, default="Low")
    plataforma = models.CharField(max_length=20)


class Recommendation(models.Model):
    issue = models.ForeignKey(JiraIssues, on_delete=models.CASCADE)
    dev = models.ForeignKey(MDev, on_delete=models.CASCADE)

    def __str__(self):
        return self.issue.key + " - " + self.dev.name


class Experiencia(models.Model):
    exp = models.CharField(max_length=100)
    dev = models.ManyToManyField(MDev, blank=True)
    projeto = models.ManyToManyField(MProject, blank=True)

    def __str__(self):
        return self.exp


class User_jira(models.Model):
    login = models.CharField(max_length=150)
    token = models.CharField(max_length=150)
