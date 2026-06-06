FROM python:3.11-slim

# Instala dependências do sistema necessárias para o Hermes
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Baixa a última versão oficial do Hermes Agent
RUN git clone https://github.com/NousResearch/hermes-agent.git /opt/hermes
WORKDIR /opt/hermes

# Instala o Hermes e as extensões de mensageria (Telegram, Email, etc)
RUN pip install --no-cache-dir uv
RUN uv pip install --system --no-cache-dir -e ".[all,messaging]"

# Prepara a pasta de dados do Hermes
ENV HERMES_HOME=/root/.hermes
RUN mkdir -p /root/.hermes

# Copia as regras e a memória do robô para dentro do container
COPY config.yaml /root/.hermes/config.yaml
COPY skills /root/.hermes/skills
COPY keep_alive.py /opt/keep_alive.py
COPY start.sh /opt/start.sh

# Dá permissão de execução
RUN chmod +x /opt/start.sh

# Inicializa o robô
CMD ["/opt/start.sh"]
