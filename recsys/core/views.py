from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.

def projetos(request):
    projects = MProject.objects.all()
    args = {'projects': projects}
    return render(request, 'core/projects.html', args)


def projeto_detail(request, projeto_id):
    return HttpResponse("Tela do projeto %s" % projeto_id)


def projeto_cadastro(request):
    return HttpResponse("Tela de cadastrar projeto")


def desenvolvedores(request):
    desenvolvedores = MDev.objects.all()
    args = {"desenvolvedores":desenvolvedores}
    return render(request, 'core/desenvolvedores.html', args)


def desenvolverdor_detalhe(request, desenvolvedor_id):
    return HttpResponse("Tela do desenvolveor %s" % desenvolvedor_id)


def desenvolverdor_cadastro(request):
    return HttpResponse("Tela do cadastro de desenvolvedores")


def recomendacao(request, projeto_id):
    return HttpResponse("Tela da recomendação do projeto %s" % projeto_id)
