from pathlib import Path
from urllib import request
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from interno.forms import CategoriaForm
from . import models


def home(request):
    return render(request,"home.html")


def categoria_index(request):
    categorias = models.Categoria.objects.all()
    property(categorias)
    contexto={
        "categorias": categorias
    }
    return render(request,"categorias/index.html", context=contexto)


def categoria_cadastrar(request):
    if request.method == "GET":
        return render(request,"categorias/cadastrar.html")
    
    nome = request.POST.get("nome").strip()
    categoria=models.Categoria(nome=nome)
    categoria.save()
    return redirect("categorias")


def categoria_apagar(request, id: int):
    categoria = models.Categoria.objects.get(pk=id)
    categoria.delete()

    return redirect ("categorias")

def categoria_editar(request, id: int):
    categoria = models.Categoria.objects.get(pk=id)
    if request.method == "GET":
        contexto = {"categoria": categoria}
        return render(request,"categorias/editar.html", context=contexto)
    
    categoria.nome = request.POST.get("nome").strip()
    categoria.save()
    return redirect ("categorias")


def estado_index(request):
    estados = models.Estado.objects.all()
    property(estados)
    contexto ={
        "estados": estados
    }
    return render(request,"estados/index.html", context=contexto)
    

def estado_cadastrar(request):
    if request.method == "GET":
        return render (request,"estados/cadastrar.html")
    
    nome= request.POST.get("nome").strip()
    uf=request.POST.get("uf")
    estado=models.Estado(nome=nome, sigla=uf)
    estado.save()
    return redirect("estados")


def estado_apagar(request, id: int):
    estado=models.Estado.objects.get(pk=id)
    estado.delete()
    return redirect("estados")


def estado_editar(request, id: int):
    estado = models.Estado.objects.get(pk=id)
    if request.method == "GET":
        contexto ={"estado": estado}
        return render(request, "estados/editar.html", context=contexto)
    estado.nome = request.POST.get("nome").strip()
    estado.save()
    return redirect ("estados")

# Create your views here.

def categoria_form_index(request):
    categorias = models.Categoria.objects.all()
    property(categorias)
    contexto={
        "categorias": categorias
    }
    return render(request,"categorias_forms/index.html", context=contexto)
    
    
def categoria_form_cadastrar(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categorias_form")
    else:
        form = CategoriaForm()  
    contexto = {"form": form} 
    return render(request, "categorias_forms/cadastrar.html", context=contexto)


def categoria_form_apagar(request,id:int):
    categoria = models.Categoria.objects.get(pk=id)
    categoria.delete()

    return redirect ("categorias_form")


def categoria_form_editar(request,id:int):
    categoria = models.Categoria.objects.get(pk=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("categorias_form")
    else:
        form = CategoriaForm(instance=categoria)    

    contexto = {
            "form": form,
            "categoria": categoria
            }
    return render(request,"categorias_forms/editar.html", contexto)




def produto_index(request):
    produtos = models.Produto.objects.all()
    contexto = {"produtos": produtos}
    return render(request, "produtos/index.html", context=contexto)


def produto_cadastrar(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        id_categoria = request.POST.get("categoria")
        descricao = request.POST.get("descricao")
        imagem =__upload_imagem(request)
        produto = models.Produto(
            nome=nome,
            preco=preco,
            descricao=descricao,
            categoria_id=id_categoria,
            imagem=imagem,
        )
        produto.save()
        return redirect("produtos")
    categorias = models.Categoria.objects.all()
    contexto = {"categorias": categorias}
    return render(request, "produtos/cadastrar.html", contexto)


def __upload_imagem(request):
    if not request.FILES:
        return None
    imagem = request.FILES.get("imagem", None)
    if not imagem:
        return None
    salvador = FileSystemStorage()
    caminha_arquivo = Path("produtos_imagens")/ imagem.name
    nome_arquivo = salvador.save(caminha_arquivo, imagem)
    return nome_arquivo


def produto_apagar(request, id: int):
    produto = models.Produto.objects.get(pk=id)
    produto.delete()
    return redirect("produtos")


def produto_editar(request, id: int):
    produto = models.Produto.objects.get(pk=id)

    if request.method == "POST":
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        id_categoria = request.POST.get("categoria")
        descricao = request.POST.get("descricao")
        produto.nome = nome
        produto.preco = preco
        produto.descricao = descricao
        produto.categoria_id = id_categoria
        produto.save()
        return redirect("produtos")

    categorias = models.Categoria.objects.all()
    contexto = {
        "categorias": categorias,
        "produto": produto,
    }
    return render(request, "produtos/editar.html", contexto)


def cidade_index(request):
    cidades = models.Cidade.objects.all()
    contexto ={"cidades": cidades}
    return render(request, "cidades/index.html", context=contexto)

def cidade_cadastrar(request):
    if request.method == "POST":
        nome = request.POST.get("cidade")
        estado= request.POST.get("estado")
        quantidade_habitantes= request.POST.get("quantidade_habitantes")
        clima= request.POST.get("clima")
        data_fundacao= request.POST.get("data_fundacao")
        cidade = models.Cidade(
            nome=nome,
            estado=estado,
            quantidade_habitantes=quantidade_habitantes,
            clima=clima,
            data_fundacao=data_fundacao,
        )
        cidade.save()
        return redirect("cidades")
    estados = models.Estado.objects.all()
    contexto ={"estados": estados}
    return render (request,"cidades/cadastrar.html", contexto)

def cidade_editar(request):
    cidade = models.Cidade.objects.get(pk=id)

    if request.method == "POST":
        nome = request.POST.get("cidade")
        estado= request.POST.get("estado")
        quantidade_habitantes= request.POST.get("quantidade_habitantes")
        clima= request.POST.get("clima")
        data_fundacao= request.POST.get("data_fundacao")
        cidade.nome = nome
        cidade.estado = estado
        cidade.quantidade_habitantes= quantidade_habitantes
        cidade.clima = clima
        cidade.data_fundacao = data_fundacao
        cidade.save()
        return redirect("cidades")
    
    estados = models.Estado.objects.all()
    contexto= {
        "estados": estados,
        "cidades": cidade,
    }
    return render(request, "cidades/editar.html", contexto)
