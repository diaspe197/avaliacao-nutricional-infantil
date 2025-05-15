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
