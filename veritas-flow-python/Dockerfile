# Usa a imagem oficial do Python slim
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Atualiza pacotes e instala dependências de sistema (se necessário)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copia as dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta dinâmica (Render e Cloud Run usam a env PORT, Streamlit default é 8501)
ENV PORT=8501
EXPOSE $PORT

# Comando para rodar a aplicação
CMD streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0
