from datetime import datetime
from scripts.lms_utils import buscar_lms_e_calcular_z

def calcular_idade_meses(data_nascimento, data_avaliacao):
    anos = data_avaliacao.year - data_nascimento.year
    meses = data_avaliacao.month - data_nascimento.month
    dias = data_avaliacao.day - data_nascimento.day
    idade_meses = anos * 12 + meses
    if dias < 0:
        idade_meses -= 1
    return idade_meses

def calcular_imc(peso, altura_cm):
    if altura_cm == 0:
        return 0
    altura_m = altura_cm / 100
    return round(peso / (altura_m ** 2), 2)

def calcular_zscore_manual(sexo, idade_meses, imc):
    return buscar_lms_e_calcular_z(idade_meses, imc, sexo, indicador="imc")

def calcular_zpeso_idade(sexo, idade_meses, peso):
    if idade_meses > 120:
        return "faixa etária > 10 anos não estão disponíveis nos dados da OMS)"
    return buscar_lms_e_calcular_z(idade_meses, peso, sexo, indicador="peso")

def calcular_zaltura_idade(sexo, idade_meses, altura):
    return buscar_lms_e_calcular_z(idade_meses, altura, sexo, indicador="altura")

def classificar_imc(z):
    if z < -3:
        return "Magreza grave"
    elif -3 <= z < -2:
        return "Magreza moderada"
    elif -2 <= z < -1:
        return "Magreza leve"
    elif -1 <= z <= 1:
        return "Eutrofia"
    elif 1 < z <= 2:
        return "Risco de sobrepeso"
    elif 2 < z <= 3:
        return "Sobrepeso"
    else:
        return "Obesidade"
    
def interpretar_imc(imc):
    if imc < 14:
        return "Abaixo do adequado"
    elif 14 <= imc < 17:
        return "Adequado"
    elif 17 <= imc < 19:
        return "Sobrepeso"
    else:  # imc >= 19
        return "Obesidade"

def interpretar_z_imc(z):
    if z < -3:
        return "Magreza grave"
    elif -3 <= z < -2:
        return "Magreza moderada"
    elif -2 <= z < -1:
        return "Magreza leve ou risco de magreza"
    elif -1 <= z <= 1:
        return "Eutrofia (peso adequado)"
    elif 1 < z <= 2:
        return "Sobrepeso"
    elif 2 < z <= 3:
        return "Obesidade"
    else:  # z > 3
        return "Obesidade grave"

def interpretar_z_peso(z):
    if isinstance(z, str):
        return z  # caso seja mensagem como "não disponível"
    if z < -3:
        return "Peso muito baixo"
    elif -3 <= z < -2:
        return "Baixo peso"
    elif -2 <= z <= 2:
        return "Peso adequado"
    else:  # z > 2
        return "Peso elevado"

def interpretar_z_altura(z):
    if z < -3:
        return "Baixa estatura acentuada"
    elif -3 <= z < -2:
        return "Baixa estatura"
    elif -2 <= z <= 2:
        return "Estatura adequada"
    else:  # z > 2
        return "Estatura elevada"