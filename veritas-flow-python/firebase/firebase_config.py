import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def get_firestore_client():
    """
    Inicializa o Firebase Admin SDK usando Streamlit Secrets (.streamlit/secrets.toml)
    Retorna a instância do cliente Firestore.
    """
    # Verifica se o firebase já foi inicializado
    if not firebase_admin._apps:
        try:
            # Obtém as credenciais do st.secrets
            cert_dict = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["private_key_id"],
                "private_key": st.secrets["firebase"]["private_key"],
                "client_email": st.secrets["firebase"]["client_email"],
                "client_id": st.secrets["firebase"]["client_id"],
                "auth_uri": st.secrets["firebase"]["auth_uri"],
                "token_uri": st.secrets["firebase"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
            }
            if "universe_domain" in st.secrets["firebase"]:
                cert_dict["universe_domain"] = st.secrets["firebase"]["universe_domain"]
            # Inicializa o app
            cred = credentials.Certificate(cert_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Erro ao inicializar Firebase: Certifique-se de configurar .streamlit/secrets.toml corretamente. Detalhes: {e}")
            return None
    
    # Retorna o cliente do Firestore
    return firestore.client()
