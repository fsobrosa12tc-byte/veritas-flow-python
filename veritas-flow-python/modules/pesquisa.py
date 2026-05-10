import streamlit as st
import pandas as pd
from services.firestore_service import FirestoreService

def render_pesquisa():
    st.header("🔍 Pesquisa de Histórico")
    
    termo = st.text_input("Buscar por Placa ou Nome", placeholder="Digite a placa (ex: ABC1234) ou parte do nome...")
    
    if st.button("Buscar", type="primary"):
        if not termo:
            st.warning("Digite um termo para pesquisar.")
            return
            
        with st.spinner("Pesquisando..."):
            db = FirestoreService()
            resultados = db.search_atendimentos(termo)
            
            if resultados:
                st.success(f"{len(resultados)} registro(s) encontrado(s)!")
                
                # Prepara os dados para o dataframe
                df = pd.DataFrame(resultados)
                
                # Formatando a data se existir
                if 'created_at' in df.columns:
                    # Tenta converter de datetime com timezone UTC para local formatado
                    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
                    df = df.rename(columns={'created_at': 'Data/Hora'})
                
                # Reordenando e renomeando as colunas pra exibir bonito
                colunas_exibicao = ['Data/Hora', 'placa', 'solicitante', 'outorgante', 'valor', 'pagamento']
                # Filtrando as colunas que existem no df
                colunas_exibicao = [c for c in colunas_exibicao if c in df.columns]
                
                df_exibicao = df[colunas_exibicao].copy()
                df_exibicao.columns = [c.capitalize() if c != 'Data/Hora' else c for c in df_exibicao.columns]
                
                st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
            else:
                st.info(f"Nenhum resultado encontrado para: {termo}")
