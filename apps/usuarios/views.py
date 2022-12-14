from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    """Cadastra uma nova pessoa no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O campo nome nao pode ficar em branco!!')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O campo email nao pode ficar em branco!!')
            return redirect('cadastro')
        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas nao sao iguais!!')
            print('As senhas nao sao iguais!!')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuario ja cadastrado!!')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuario ja cadastrado!!')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        print('Usuario Cadastrado com Sucesso!!')
        messages.success(request, 'Usuario Cadastrado com Sucesso!!')
        return redirect('login')
    return render(request, 'usuarios/cadastro.html')

def login(request):
    """Realiza o login de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'OS campos email e senha nao podem ficar em branco!')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso!!')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def dashboard(request):
    """Pagina para o usuario logado criar e acessar suas receitas"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)
        
        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def logout(request):
    """Faz o logout de uma pessoa do sistema"""
    auth.logout(request)
    return redirect('index')

def campo_vazio(campo):
    """Verifica????o se o campo esta vazio"""
    return not campo.strip()

def senhas_nao_sao_iguais(senha, senha2):
    """Verifica se as senhas nao sao iguais"""
    return senha != senha2

