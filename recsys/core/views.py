from django.shortcuts import render, redirect, get_object_or_404
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
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            url = request.POST['url']
            status = True if request.POST['status'] == "on" else False
            projeto = MProject(name=nome, url=url, status=status)
            projeto.save()
            # args = {"projeto_id": projeto.id}
            return redirect('core:project_detail', projeto_id= projeto.id)
        except (KeyError):
            return render(request, 'core/cadastrar_projeto.html')
    else:
        return render(request, 'core/cadastrar_projeto.html')


def desenvolvedores(request):
    desenvolvedores = MDev.objects.all()
    args = {"desenvolvedores":desenvolvedores}
    return render(request, 'core/desenvolvedores.html', args)


def desenvolverdor_detalhe(request, desenvolvedor_id):
    dev = get_object_or_404(MDev,pk=desenvolvedor_id)
    args= {"dev": dev}
    return render(request, "core/detalhe_desenvolvedor.html", args)


def desenvolverdor_cadastro(request):

    if request.method == "POST":
        try:
            projeto = get_object_or_404(MProject, pk=request.POST['projeto'])
            nome = request.POST['nome']
            email = request.POST['email']
            id_jira = request.POST['id_jira']
            experiencias = request.POST['experiencias']
            desenvolvedor = MDev(name=nome, email=email, project=projeto, id_jira=id_jira)
            desenvolvedor.save()

            experiencias = experiencias.lower()
            experiencias = experiencias.split(",")
            exps = []

            for exp in experiencias:
                exps.append(exp.strip())
            for exp in exps:
                Ex, created = Experiencia.objects.get_or_create(exp=exp)
                Ex.dev.add(desenvolvedor)

            return redirect('core:dev_detail', desenvolvedor_id=desenvolvedor.id)
        except (KeyError):
            projetos = MProject.objects.all()
            args = {"projetos": projetos}
            return render(request, "core/cadastrar_desenvolvedores.html", args)
    else:
        projetos = MProject.objects.all()
        args = {"projetos":projetos}
        return render(request, "core/cadastrar_desenvolvedores.html", args)


def recomendacao(request, projeto_id):
    return HttpResponse("Tela da recomendação do projeto %s" % projeto_id)
