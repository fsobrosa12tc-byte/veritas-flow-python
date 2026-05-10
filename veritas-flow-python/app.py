import streamlit as st

# Configuração Base da Página (DEVE SER O PRIMEIRO COMANDO STREAMLIT)
st.set_page_config(
    page_title="Veritas Flow",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importando os módulos da aplicação
from modules.atendimento import render_atendimento
from modules.pesquisa import render_pesquisa
from modules.dashboard import render_dashboard
from modules.fechamento import render_fechamento

def main():
    # Estilização CSS para Mobile-First e UX Limpa
    st.markdown("""
        <style>
            /* Esconde botão de deploy e hambúrguer padrão do Streamlit para usuários */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Ajustes Mobile e Botões */
            .stButton > button {
                width: 100%;
                border-radius: 8px;
                font-weight: bold;
                height: 3em;
            }
            .stTextInput > div > div > input {
                border-radius: 6px;
                text-transform: uppercase;
            }
        </style>
    """, unsafe_allow_html=True)

    # Menu Lateral
    with st.sidebar:
        st.title("🚗 Veritas Flow")
        st.caption("Sistema de Balcão Operacional")
        st.divider()
        
        # Navegação
        menu = st.radio(
            "Navegação Principal",
            options=["Atendimento", "Pesquisa", "Dashboard", "Fechamento Diário"],
            label_visibility="collapsed"
        )
        
        st.divider()
        st.caption("Versão 2.0 (Streamlit)")

    # Roteamento das telas
    if menu == "Atendimento":
        render_atendimento()
    elif menu == "Pesquisa":
        render_pesquisa()
    elif menu == "Dashboard":
        render_dashboard()
    elif menu == "Fechamento Diário":
        render_fechamento()

if __name__ == "__main__":
    main()
