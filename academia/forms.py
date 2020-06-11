from django.forms import ModelForm, TextInput, Textarea, DateInput
from .models import Cliente, Endereco
from django.utils.translation import gettext as _

class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = ['complemento', 'bairro', 'cidade', 'estado']
        labels = {'complemento': _('ENDEREÇO'), 'bairro': _('BAIRRO'), 'cidade': _('CIDADE'), 'estado': _('ESTADO')}

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf', 'nome', 'identidade', 'dataNascimento', 'telefone']
        labels = {'cpf': _('CPF'), 'nome': _('NOME'), 'identidade': _('IDENTIDADE'),
                  'dataNascimento':_('DATA DE NASCIMENTO'),
                  'telefone':"TELEFONE",
                  }
        widgets = {'cpf':TextInput(attrs={'data-mask':"000.000.000-00", 'data-mask-reverse':"true", 'placeholder':"000.000.000-00"}),
                   'dataNascimento':DateInput(attrs={'data-mask':"00/00/0000",'placeholder':"__/__/____", "class":"datepicker"}),
                   'telefone':TextInput(attrs={'data-mask':"(00) 900000000", 'placeholder':"(00) 000000000"})
                   }


