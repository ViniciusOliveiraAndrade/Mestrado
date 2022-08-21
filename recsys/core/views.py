from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.

def projetos(request):
    projects = MProject.objects.all()
    output = ', '.join([p.__str__() for p in projects])
    return HttpResponse("Tela de projetos %s" % output)


def projeto_detail(request, projeto_id):
    return HttpResponse("Tela do projeto %s" % projeto_id)


def projeto_cadastro(request):
    return HttpResponse("Tela de cadastrar projeto")


def desenvolvedores(request):
    return HttpResponse("Tela do desenvolvedores")


def desenvolverdor_detalhe(request, desenvolvedor_id):
    return HttpResponse("Tela do desenvolveor %s" % desenvolvedor_id)


def desenvolverdor_cadastro(request):
    return HttpResponse("Tela do cadastro de desenvolvedores")


def recomendacao(request, projeto_id):
    return HttpResponse("Tela da recomendação do projeto %s" % projeto_id)
