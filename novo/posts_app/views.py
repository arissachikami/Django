from django.shortcuts import render,get_object_or_404, redirect
from posts_app.models import Posts,Empresa,Projeto
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from posts_app.forms import PostsForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.
@login_required(login_url='login')
def listaEmpresa(request):
    template_name = 'home.html' 
    try:
        posts = request.user.funcionariosEmpresa.all()
    except:
        posts=[]

    context = { 
        'posts': posts,
        }
    print(posts)
    return render(request, template_name, context) 
    

def listaProjeto(request, empresa_id):
    template_name = 'listaProjeto.html'
    try:
        projetos = Projeto.objects.filter(empresas=empresa_id, membros=request.user)
    except:
        projetos = []
    print(projetos)
    context = {
        'empresa': Empresa.objects.get(id=empresa_id),
        'projetos': projetos,
    }
    return render(request, template_name, context) 

    

#CRUDS básicas usuário

@login_required
def editar_usuario(request):
    if request.method == 'POST':
        request.user.username = request.POST['username']
        request.user.email = request.POST['email']
        request.user.save()
        return redirect('home')
        
    
    return render(request, 'editar_usuario.html', {'user': request.user})

@login_required
def excluir_usuario(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    
    return render(request, 'excluir_usuario.html')

#CRUDS básicas de empresas e projetos:

@login_required
def criar_empresa(request):
    funcionarios = User.objects.all() 
    if request.method == 'POST':
        name = request.POST['name']
        empresa = Empresa.objects.create(name=name, ceo=request.user)
        func = request.POST.getlist('funcionarios')
        empresa.funcionarios.set(User.objects.filter(id__in=map(int,func)))
        return redirect('home')
    
    return render(request, 'criar_empresa.html',{'funcionarios':funcionarios})


@login_required
def editar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    funcionarios = User.objects.all()  
    if request.user != empresa.ceo:
        return HttpResponseForbidden("Somente o criador da empresa pode edita-lo.") 
    if request.method == 'POST':
        empresa.name = request.POST['name']
        func = request.POST.getlist('funcionarios')
        empresa.funcionarios.set(User.objects.filter(id__in=map(int,func)))
        empresa.save()

        return redirect('home')
        
    
    return render(request, 'editar_empresa.html', {'empresa': empresa,'funcionarios':funcionarios})


@login_required
def criar_projeto(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    membros = User.objects.all()
    if request.method == 'POST':
        nome = request.POST['name']
        projeto = Projeto.objects.create(name=nome, criador=request.user, empresas=empresa)
        membros = request.POST.getlist('membro')
        projeto.membros.set(User.objects.filter(id__in=map(int,membros)))
        return redirect('listaProjeto', empresa_id)
    
    return render(request, 'criar_projeto.html', {'empresa': empresa_id, 'membro':membros})


@login_required
def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    membro = User.objects.all()  
    if request.user != projeto.criador:
        return HttpResponseForbidden("Somente o criador do projeto pode edita-lo.") 

    if request.method == 'POST':
        projeto.name = request.POST['name']
        func = request.POST.getlist('membro')
        projeto.membros.set(User.objects.filter(id__in=map(int,func)))
        projeto.save()

        return redirect('listaProjeto', projeto.empresas.id)  
    return render(request, 'editar_projeto.html', {'projetos': projeto,'membros':membro,'empresa_id':projeto.empresas.id})


@login_required
def excluir_projeto(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    if projeto.criador != request.user:
        return HttpResponseForbidden("Somente o criador do projeto pode excluí-lo.")
    empresa_id = projeto.empresas.id
    projeto.delete()
    return redirect('listaProjeto', empresa_id)

def excluir_empresa(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    if empresa.ceo != request.user:
        return HttpResponseForbidden("Somente o criador da empresa pode excluí-la.")
    empresa.delete()
    return redirect('home')

