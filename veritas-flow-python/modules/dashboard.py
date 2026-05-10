import streamlit as st
import pandas as pd
from services.firestore_service import FirestoreService

def render_dashboard():
    st.header("📊 Dashboard Financeiro (Hoje)")
    
    db = FirestoreService()
    
    with st.spinner("Carregando dados..."):
        atendimentos = db.get_atendimentos_hoje()
        
    if not atendimentos:
        st.info("Nenhum atendimento registrado hoje.")
        return
        
    df = pd.DataFrame(atendimentos)
    
    # KPIs
    total_atendimentos = len(df)
    total_faturado = df['valor'].sum() if 'valor' in df.columns else 0.0
    
    # Contagem de Pagamentos
    if 'pagamento' in df.columns:
        # Pega as contagens
        contagem_pagamentos = df['pagamento'].value_counts()
        pix = contagem_pagamentos.get('PIX', 0)
        cc = contagem_pagamentos.get('Cartão de Crédito', 0)
        cd = contagem_pagamentos.get('Cartão de Débito', 0)
        dinheiro = contagem_pagamentos.get('Dinheiro', 0)
    else:
        pix = cc = cd = dinheiro = 0

    # Exibição de Métricas Principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total de Atendimentos", value=f"{total_atendimentos}")
    with col2:
        st.metric(label="Faturamento do Dia", value=f"R$ {total_faturado:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
    st.divider()
    
    # Submétricas de Pagamento
    st.subheader("Receitas por Forma de Pagamento")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PIX", pix)
    c2.metric("Crédito", cc)
    c3.metric("Débito", cd)
    c4.metric("Dinheiro", dinheiro)
    
    # Opcional: Gráfico
    if 'pagamento' in df.columns:
        st.bar_chart(contagem_pagamentos)
