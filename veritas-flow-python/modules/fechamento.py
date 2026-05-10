import streamlit as st
import pandas as pd
from services.firestore_service import FirestoreService

def render_fechamento():
    st.header("🔒 Fechamento Diário")
    
    st.write("Verifique todos os registros de hoje antes de consolidar o caixa.")
    
    db = FirestoreService()
    
    atendimentos = db.get_atendimentos_hoje()
    
    if not atendimentos:
        st.warning("Não há atendimentos para realizar fechamento hoje.")
        return
        
    df = pd.DataFrame(atendimentos)
    
    if 'created_at' in df.columns:
        df['Hora'] = pd.to_datetime(df['created_at']).dt.strftime('%H:%M')
    
    colunas_exibicao = ['Hora', 'placa', 'solicitante', 'valor', 'pagamento']
    colunas_exibicao = [c for c in colunas_exibicao if c in df.columns]
    
    df_exibir = df[colunas_exibicao].copy()
    
    st.dataframe(df_exibir, use_container_width=True, hide_index=True)
    
    st.divider()
    
    total = df['valor'].sum() if 'valor' in df.columns else 0.0
    st.subheader(f"Total em Caixa: R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    if st.button("Confirmar Fechamento", type="primary"):
        # No futuro: pode gerar um PDF, enviar e-mail ou marcar no banco como fechado.
        st.success("Caixa consolidado! Você pode imprimir essa página (Ctrl+P) ou salvar como PDF.")
