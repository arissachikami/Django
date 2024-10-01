from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

class Empresa(models.Model):
    name = models.CharField(max_length=100)
    ceo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ceoEmpresa')
    funcionarios = models.ManyToManyField(User, blank='true',related_name='funcionariosEmpresa')
    
class Projeto(models.Model):
    name = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projetosCriados')
    membros = models.ManyToManyField(User, blank=True,related_name='participanteProjeto')
    empresas = models.ForeignKey(Empresa, on_delete=models.CASCADE,related_name='ceoEmpresa')