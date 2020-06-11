from django.urls import path
from . import views


app_name = 'academia'

urlpatterns = [
    path(r'clientes/', views.ClientView.as_view(), name='clientes'),
    path(r'busca_nome', views.busca_por_nome, name="busca_nome"),
    path(r'clientes/<str:cpf>', views.ClienteDetailView.as_view(), name='cliente'),
    path(r'busca_cliente', views.BuscaCliente.as_view(), name="busca_cliente"),
    path(r'matricular/', views.realizar_matricula, name="matricular"),
    path(r'gerenciar_cliente/', views.adicionar_cliente, name="adicionar_cliente"),
    path(r'excluir_cliente/', views.index, name="excluir"),
    path(r'excluir_cliente/<str:cpf>', views.excluir_cliente, name="excluir_cliente"),
    path(r'gerenciar_cliente/<str:cpf>', views.editar_cliente, name="editar_cliente"),
    path(r'registrar_pagamento', views.registrar_pagamento, name="registrar_pagamento"),
    path(r'registrar_ferias', views.registrar_ferias, name="registrar_ferias"),
]