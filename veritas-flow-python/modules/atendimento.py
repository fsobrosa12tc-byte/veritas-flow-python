import streamlit as st
from services.firestore_service import FirestoreService
from services.validation_service import validar_placa

def render_atendimento():
    st.header("📝 Novo Atendimento")
    
    # Controle de estado para reset automático
    if 'form_key' not in st.session_state:
        st.session_state.form_key = 0

    # Usando form para reset e submit agrupado
    with st.form(key=f"form_atendimento_{st.session_state.form_key}", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Uppercase via form input: Streamlit não tem uppercase automático no front em forms nativos, 
            # então faremos o upper no processamento (backend) ou usando a lib streamlit-js-eval,
            # mas manteremos nativo e validado na submissão.
            placa = st.text_input("Placa do Veículo", max_chars=7, help="Ex: ABC1234 ou ABC1D23")
            solicitante = st.text_input("Nome do Solicitante")
            outorgante = st.text_input("Nome do Outorgante (Proprietário)")
            
        with col2:
            obito = st.selectbox("Comunicação de Óbito?", ["Não", "Sim"])
            valor = st.number_input("Valor do Serviço (R$)", min_value=0.0, format="%.2f")
            pagamento = st.selectbox("Forma de Pagamento", ["PIX", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])
            
        submit = st.form_submit_button("Salvar Atendimento", use_container_width=True)

    if submit:
        # Validações
        if not placa or not solicitante or not outorgante:
            st.warning("Preencha os campos obrigatórios (Placa, Solicitante e Outorgante).")
            return
            
        valido, placa_formatada = validar_placa(placa)
        if not valido:
            st.error(placa_formatada)
            return
            
        # Preparando dados
        dados = {
            "placa": placa_formatada,
            "solicitante": solicitante.strip().upper(),
            "outorgante": outorgante.strip().upper(),
            "obito": obito,
            "valor": float(valor),
            "pagamento": pagamento
            # data_hora e created_at serão injetados no service
        }
        
        db = FirestoreService()
        if db.create_atendimento(dados):
            st.success(f"Atendimento para placa {placa_formatada} registrado com sucesso!")
            # Atualiza a key para forçar re-render limpo
            st.session_state.form_key += 1
            st.rerun()
