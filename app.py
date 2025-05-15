import streamlit as st
from datetime import datetime, date
import pandas as pd
from io import BytesIO
import os
from scripts.calculos import (
    calcular_idade_meses,
    calcular_imc,
    calcular_zscore_manual,
    classificar_imc,
    calcular_zpeso_idade,
    calcular_zaltura_idade,
    interpretar_z_imc,
    interpretar_z_peso,
    interpretar_z_altura,
    interpretar_imc
)

# Estilo visual
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Título
st.markdown("<h1 style='text-align: center; color: #0072b1;'>Avaliação Nutricional Infantil</h1>", unsafe_allow_html=True)

with st.form("form_avaliacao"):
    nome = st.text_input("Nome Completo", key="input_nome")
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino"], key="input_sexo")
    data_nascimento = st.date_input("Data de nascimento", min_value=date(2013, 1, 1), key="input_nascimento")
    data_avaliacao = st.date_input("Data da avaliação", value=datetime.today(), key="input_avaliacao")
    peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f", key="input_peso")
    altura = st.number_input("Altura (cm)", min_value=0.0, format="%.2f", key="input_altura")
    enviar = st.form_submit_button("Calcular")

if enviar:
    idade_meses = calcular_idade_meses(data_nascimento, data_avaliacao)
    imc = calcular_imc(peso, altura)
    z_imc = calcular_zscore_manual(sexo, idade_meses, imc)
    z_peso = calcular_zpeso_idade(sexo, idade_meses, peso)
    z_altura = calcular_zaltura_idade(sexo, idade_meses, altura)
    classificacao = classificar_imc(z_imc)

    imc_class = interpretar_imc(imc)
    z_imc_class = interpretar_z_imc(z_imc)
    z_peso_class = interpretar_z_peso(z_peso)
    z_altura_class = interpretar_z_altura(z_altura)

    df_resultado = pd.DataFrame([{
        "nome": nome,
        "sexo": sexo,
        "data de nascimento": data_nascimento,
        "data da avaliação": data_avaliacao,
        "idade(meses)": idade_meses,
        "peso(kg)": peso,
        "altura(cm)": altura,
        "IMC": imc,
        "IMC - classificação": imc_class,
        "Z-IMC/idade": round(z_imc, 2),
        "Z-IMC/idade - interpretação": z_imc_class,
        "Z-peso/idade": z_peso if isinstance(z_peso, str) else round(z_peso, 2),
        "Z-peso/idade - interpretação": z_peso_class,
        "Z-altura/idade": round(z_altura, 2),
        "Z-altura/idade - interpretação": z_altura_class,
        "classificação nutricional": classificacao,
        "observações": ""
    }])

    st.session_state["resultado_atual"] = df_resultado

    st.subheader("Resultado da Avaliação")
    st.write(f"**Idade em meses:** {idade_meses}")
    st.write(f"**IMC:** {imc:.2f} → {imc_class}")
    st.write(f"**Z-IMC/idade:** {z_imc:.2f} → {z_imc_class}")
    st.write(f"**Z-peso/idade:** {z_peso if isinstance(z_peso, str) else f'{z_peso:.2f}'} → {z_peso_class}")
    st.write(f"**Z-altura/idade:** {z_altura:.2f} → {z_altura_class}")
    st.write(f"**Classificação nutricional:** {classificacao}")

# Salvar avaliação
if "resultado_atual" in st.session_state:
    if st.button("Salvar avaliação"):
        df_resultado = st.session_state["resultado_atual"]
        csv_path = "avaliacoes.csv"
        if os.path.exists(csv_path):
            df_existente = pd.read_csv(csv_path)
            df_final = pd.concat([df_existente, df_resultado], ignore_index=True)
        else:
            df_final = df_resultado

        df_final.to_csv(csv_path, index=False)
        st.success("✅ Avaliação salva com sucesso!")

        if st.button("Nova Avaliação"):
            for chave in ["resultado_atual"]:
                if chave in st.session_state:
                    del st.session_state[chave]
            st.rerun()

# Exportar histórico
if os.path.exists("avaliacoes.csv"):
    df_historico = pd.read_csv("avaliacoes.csv")
    
    buffer_todas = BytesIO()
    df_historico.to_excel(buffer_todas, index=False, engine="openpyxl")
    buffer_todas.seek(0)

    st.markdown("##### Exportar Histórico Completo")
    st.download_button(
        label="Baixar Avaliações",
        data=buffer_todas,
        file_name="avaliacoes_historico.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Tabela interativa para visualizar e excluir
if os.path.exists("avaliacoes.csv"):
    df_historico = pd.read_csv("avaliacoes.csv")
    df_historico["Excluir"] = False

    with st.expander("🔍 Visualizar Avaliações Anteriores", expanded=False):

        edited_df = st.data_editor(
            df_historico,
            use_container_width=True,
            key="tabela_edicao",
            disabled=[
                "nome", "sexo", "data de nascimento", "data da avaliação", "idade(meses)", 
                "peso(kg)", "altura(cm)", "IMC", "IMC - classificação", "Z-IMC/idade",
                "Z-IMC/idade - interpretação", "Z-peso/idade", "Z-peso/idade - interpretação",
                "Z-altura/idade", "Z-altura/idade - interpretação", "classificação nutricional", 
                "observações"
            ]
        )

        if st.button("Excluir Avaliações Selecionadas"):
            df_restante = edited_df[edited_df["Excluir"] != True].drop(columns=["Excluir"])
            df_restante.to_csv("avaliacoes.csv", index=False)
            st.success("✅ Avaliações Excluídas Com Sucesso.")
            st.rerun()
