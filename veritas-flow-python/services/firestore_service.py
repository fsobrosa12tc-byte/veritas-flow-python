from firebase.firebase_config import get_firestore_client
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime
import streamlit as st

class FirestoreService:
    def __init__(self):
        self.db = get_firestore_client()
        self.collection_name = "atendimentos"

    def is_connected(self):
        return self.db is not None

    def create_atendimento(self, data):
        """Salva um novo atendimento no Firestore."""
        if not self.is_connected():
            return False
        
        try:
            # Garante que data_hora existe e é timestamp do servidor
            if 'data_hora' not in data:
                data['data_hora'] = firestore.SERVER_TIMESTAMP
            
            # Adiciona timestamp local para uso na UI
            data['created_at'] = datetime.now()
                
            self.db.collection(self.collection_name).add(data)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar no Firestore: {e}")
            return False

    def get_atendimentos_hoje(self):
        """Retorna todos os atendimentos do dia atual."""
        if not self.is_connected():
            return []
            
        hoje = datetime.now()
        inicio_dia = datetime(hoje.year, hoje.month, hoje.day, 0, 0, 0)
        fim_dia = datetime(hoje.year, hoje.month, hoje.day, 23, 59, 59)
        
        try:
            docs = self.db.collection(self.collection_name)\
                .where(filter=FieldFilter("created_at", ">=", inicio_dia))\
                .where(filter=FieldFilter("created_at", "<=", fim_dia))\
                .order_by("created_at", direction=firestore.Query.DESCENDING)\
                .stream()
            
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            st.error(f"Erro ao buscar atendimentos do dia: {e}")
            return []

    def search_atendimentos(self, query_term):
        """Busca atendimentos por placa (busca exata) ou partes do solicitante."""
        if not self.is_connected() or not query_term:
            return []
            
        term_upper = query_term.upper().strip()
        resultados = []
        
        try:
            # Busca por placa (que sempre estará em upper case)
            docs_placa = self.db.collection(self.collection_name)\
                .where(filter=FieldFilter("placa", "==", term_upper))\
                .stream()
                
            for doc in docs_placa:
                dic = doc.to_dict()
                dic['id'] = doc.id
                resultados.append(dic)
            
            # Como Firestore não tem 'LIKE', para busca parcial de nome puxamos os recentes 
            # e filtramos em memória, ou pedimos o termo exato. 
            # Para otimizar, buscaremos os últimos 100 e faremos filtro na memória:
            if not resultados:
                docs = self.db.collection(self.collection_name).order_by("created_at", direction=firestore.Query.DESCENDING).limit(100).stream()
                for doc in docs:
                    dic = doc.to_dict()
                    solicitante = dic.get('solicitante', '').upper()
                    outorgante = dic.get('outorgante', '').upper()
                    if term_upper in solicitante or term_upper in outorgante:
                        dic['id'] = doc.id
                        resultados.append(dic)
            
            return resultados
        except Exception as e:
            st.error(f"Erro na pesquisa: {e}")
            return []
