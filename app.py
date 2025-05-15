import streamlit as st
from datetime import datetime, date
import pandas as pd
from io import BytesIO
from scripts.calculos import (
    calcular_idade_meses,
    calcular_imc,
    calcular_zscore_manual,
    classificar_imc,
    calcular_zpeso_idade,
    calcular_zaltura_idade
)

# Estilo visual
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Título estilizado
st.markdown("<h1 style='text-align: center; color: #0072b1;'>Avaliação Nutricional Infantil</h1>", unsafe_allow_html=True)

with st.form("form_avaliacao"):
    nome = st.text_input("Nome")
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
    data_nascimento = st.date_input("Data de nascimento", min_value=date(2013, 1, 1))
    data_avaliacao = st.date_input("Data da avaliação", value=datetime.today())
    peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
    altura = st.number_input("Altura (cm)", min_value=0.0, format="%.2f")
    enviar = st.form_submit_button("Calcular")

if enviar:
    idade_meses = calcular_idade_meses(data_nascimento, data_avaliacao)
    imc = calcular_imc(peso, altura)
    z_imc = calcular_zscore_manual(sexo, idade_meses, imc)
    z_peso = calcular_zpeso_idade(sexo, idade_meses, peso)
    z_altura = calcular_zaltura_idade(sexo, idade_meses, altura)
    classificacao = classificar_imc(z_imc)

    st.subheader("Resultado da Avaliação")
    st.write(f"**Idade em meses:** {idade_meses}")
    st.write(f"**IMC:** {imc}")
    st.write(f"**Z-IMC/idade:** {z_imc:.2f}")
    st.write(f"**Z-peso/idade:** {z_peso if isinstance(z_peso, str) else f'{z_peso:.2f}'}")
    st.write(f"**Z-altura/idade:** {z_altura:.2f}")
    st.write(f"**Classificação nutricional:** {classificacao}")

    df_resultado = pd.DataFrame([{
        "nome": nome,
        "sexo": sexo,
        "data de nascimento": data_nascimento,
        "data da avaliação": data_avaliacao,
        "idade(meses)": idade_meses,
        "peso(kg)": peso,
        "altura(cm)": altura,
        "IMC": imc,
        "Z-IMC/idade": round(z_imc, 2),
        "Z-peso/idade": z_peso if isinstance(z_peso, str) else round(z_peso, 2),
        "Z-altura/idade": round(z_altura, 2),
        "classificação nutricional": classificacao,
        "observações": ""
    }])

    buffer = BytesIO()
    df_resultado.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    st.download_button(
        label="📥 Baixar resultado",
        data=buffer,
        file_name="avaliacao_nutricional.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
