import pandas as pd
import os

def carregar_tabela_lms(sexo, idade_meses, indicador):
    sexo = sexo.lower()
    base_path = "data/"

    if indicador == "imc":
        path = os.path.join(base_path, f"bmi-{'girls' if sexo == 'feminino' else 'boys'}-z-who-2007-exp.xlsx")
    elif indicador == "peso":
        if idade_meses <= 60:
            path = os.path.join(base_path, f"wfa_{'girls' if sexo == 'feminino' else 'boys'}_0-to-5-years_zscores.xlsx")
        else:
            path = os.path.join(base_path, f"hfa-{'girls' if sexo == 'feminino' else 'boys'}-z-who-2007-exp_7ea58763-36a2-436d-bef0-7fcfbadd2820.xlsx"
                                  if sexo == 'feminino' else
                                  "hfa-boys-z-who-2007-exp_0ff9c43c-8cc0-4c23-9fc6-81290675e08b.xlsx")
    elif indicador == "altura":
        if idade_meses <= 24:
            path = os.path.join(base_path, f"lhfa_{'girls' if sexo == 'feminino' else 'boys'}_0-to-2-years_zscores.xlsx")
        elif idade_meses <= 60:
            path = os.path.join(base_path, f"lhfa_{'girls' if sexo == 'feminino' else 'boys'}_2-to-5-years_zscores.xlsx")
        else:
            path = os.path.join(base_path, f"hfa-{'girls' if sexo == 'feminino' else 'boys'}-z-who-2007-exp.xlsx"
                                  if sexo == 'feminino' else
                                  "hfa-boys-z-who-2007-exp.xlsx")
    else:
        raise ValueError("Indicador desconhecido.")

    # Lê o arquivo e remove espaços dos nomes de colunas
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    colunas_esperadas = {"Month", "L", "M", "S"}
    if not colunas_esperadas.issubset(set(df.columns)):
        raise ValueError(f"Colunas esperadas {colunas_esperadas} não encontradas em {path}. Colunas reais: {list(df.columns)}")

    df = df[["Month", "L", "M", "S"]].dropna()
    df["Month"] = pd.to_numeric(df["Month"], errors="coerce")

    # Busca pela idade mais próxima
    row = df.iloc[(df["Month"] - idade_meses).abs().argsort()[:1]]

    return row.iloc[0]["L"], row.iloc[0]["M"], row.iloc[0]["S"]

def calcular_zscore(valor, L, M, S):
    if L == 0:
        return (valor / M - 1) / S
    return ((valor / M) ** L - 1) / (L * S)

def buscar_lms_e_calcular_z(idade_meses, valor, sexo, indicador):
    L, M, S = carregar_tabela_lms(sexo, idade_meses, indicador)
    return calcular_zscore(valor, L, M, S)
