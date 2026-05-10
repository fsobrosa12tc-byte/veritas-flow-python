# Veritas Flow (Production-Ready)

Sistema operacional de balcão para gestão de procurações veiculares. Desenvolvido com **Python 3.12**, **Streamlit** e banco de dados NoSQL **Firebase Firestore**. Foco em **Mobile-First**, agilidade no cadastro e painel gerencial financeiro intuitivo.

---

## 🛠 Tecnologias Principais
- **Backend/Frontend**: Python 3.12, Streamlit
- **Banco de Dados**: Firebase Firestore (NoSQL)
- **Bibliotecas**: `firebase-admin`, `pandas`, `Pillow`
- **Ambiente**: Streamlit Community Cloud (Deploy)

---

## 📂 Arquitetura Modular

```text
veritas-flow-python/
│
├── app.py                   # Ponto de entrada e UI Base Mobile-First
├── requirements.txt         # Dependências do projeto
├── runtime.txt              # Força o Streamlit Cloud a usar Python 3.12
├── Dockerfile               # Configuração opcional para deploy via Container
├── .gitignore               # Segurança e versionamento limpo
├── README.md                # Documentação técnica do projeto
│
├── .streamlit/              # Configurações Streamlit
│   ├── config.toml          # Theming (Cores, Fontes)
│   └── secrets.toml.example # Exemplo de injeção de credenciais
│
├── firebase/
│   └── firebase_config.py   # Inicializador do Firebase via st.secrets
│
├── modules/                 # Funcionalidades e Telas
│   ├── atendimento.py       # Cadastro rápido com reset automático
│   ├── pesquisa.py          # Histórico com busca parcial
│   ├── dashboard.py         # KPIs Financeiros do dia
│   └── fechamento.py        # Consolidação de caixa
│
├── services/                # Lógica de Negócio e Backend
│   ├── firestore_service.py # Interação e Query no Banco
│   └── validation_service.py# Validação e tratamento de dados (ex: Placa)
│
└── reports/                 # [Futuro] Relatórios salvos e PDFs gerados
```

---

## 💻 1. Rodando Localmente (Localhost)

1. No seu terminal, entre na pasta do projeto:
   ```bash
   cd "veritas-flow-python"
   ```
2. (Recomendado) Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instale as dependências rigorosas:
   ```bash
   pip install -r requirements.txt
   ```
4. **Segurança (Crucial)**:
   - Duplique o arquivo `.streamlit/secrets.toml.example` e renomeie a cópia para `secrets.toml`.
   - Abra o `secrets.toml` e cole os valores do seu **serviceAccountKey.json** (Firebase).
5. Inicie o sistema localmente:
   ```bash
   streamlit run app.py
   ```
   > A aplicação abrirá automaticamente no seu navegador.

---

## 🔥 2. Configurando o Firebase (Firestore)

1. Acesse o [Console do Firebase](https://console.firebase.google.com/) e crie/abra seu projeto.
2. Em **Cloud Firestore**, crie o banco de dados em modo de produção.
3. No painel à esquerda, vá em **Configurações do Projeto > Contas de Serviço**.
4. Clique em **Gerar nova chave privada** e baixe o arquivo `.json`.
5. Extraia os dados desse `.json` e coloque-os no `.streamlit/secrets.toml` para conectar seu app ao banco.

### Schema Automático Utilizado
O sistema cria e lê dados da coleção `atendimentos` com a seguinte estrutura:
`placa` (string), `solicitante` (string), `outorgante` (string), `obito` ("Sim"|"Não"), `valor` (float), `pagamento` (string), `data_hora` (timestamp servidor) e `created_at` (datetime local).

---

## 🚀 3. Deploy (Streamlit Community Cloud)

O repositório já está preparado com `runtime.txt` (Python 3.12) e `requirements.txt` atualizados.

1. **Suba o código para seu GitHub** (veja passo 4 abaixo).
2. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com seu GitHub.
3. Clique em **New app**.
4. Selecione seu repositório, branch (`main` ou `master`), e digite `app.py` no "Main file path".
5. **PASSO MAIS IMPORTANTE (SECRETS)**:
   - Antes de clicar em Deploy, clique em **Advanced Settings**.
   - No campo **Secrets**, cole TODO O CONTEÚDO que está no seu `.streamlit/secrets.toml` local.
   - Isso manterá suas chaves do Firebase seguras na nuvem e fora do repositório público.
6. Clique em **Deploy**! A URL pública HTTPS será gerada em segundos.

---

## ⚙️ 4. Subindo para o GitHub (Git Workflow)

Se você não tiver feito o push ainda, execute na raiz (`veritas-flow-python`):

```bash
git init
git add .
git commit -m "feat: setup veritas flow production-ready"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

---

## 🚨 Troubleshooting (Resolução de Erros)

- **Erro de Importação do Pillow/PIL**: Se ocorrer erro no deploy relacionado a imagens ou Pillow, verifique se o `requirements.txt` contém a linha `Pillow>=10.0.0`. Nosso arquivo já vem corrigido.
- **Firebase não inicializa**: Confira com precisão as chaves do seu `secrets.toml`. O Streamlit Cloud requer que a identação e as aspas triplas para a `private_key` estejam exatamente conforme o `.example`.
- **Erro de versão do Python**: Nosso arquivo `runtime.txt` está configurado para `python-3.12` garantindo compatibilidade entre `pandas` novo e Streamlit.

---
*Arquitetura 100% pronta e refatorada.*
