#!/usr/bin/env python3
"""Servidor Webhook Alexa - Ponte IFTTT + Alexa Routines + Hermes Agent
Criado por Hermes Agent para @Cabral_Cripto
"""

from flask import Flask, request, jsonify
import subprocess
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

LOG_FILE = os.path.expanduser("~/AppData/Local/hermes/alexa_commands.log")

def log_comando(comando, status, detalhe=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {comando} | {status} | {detalhe}\n")

def executar_hermes(comando):
    try:
        acoes = {
            "postar": "hermes run postar_thread",
            "noticias": "hermes run buscar_noticias",
            "resumo": "hermes run resumo_dia",
            "emails": "hermes run ler_emails",
            "med": "hermes run responder_meds",
            "teste": "echo Conexao Alexa-Hermes funcionando!",
        }

        cmd = acoes.get("teste")
        for chave, acao in acoes.items():
            if chave in comando.lower():
                cmd = acao
                break

        resultado = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return resultado.stdout[:500] if resultado.stdout else "Comando executado"
    except Exception as e:
        return f"Erro: {str(e)}"

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "servico": "Hermes Agent - Alexa Bridge",
        "versao": "1.0.0"
    })

@app.route("/alexa-webhook", methods=["POST"])
def alexa_webhook():
    dados = request.json or {}
    comando = dados.get("command", dados.get("text", ""))
    logging.info(f"Comando recebido da Alexa: {comando}")
    log_comando(comando, "recebido")
    resultado = executar_hermes(comando)
    log_comando(comando, "executado", resultado[:100])
    return jsonify({"status": "ok", "comando": comando, "resultado": resultado})

@app.route("/ifttt-trigger", methods=["POST"])
def ifttt_trigger():
    dados = request.json or {}
    comando = dados.get("command", "")
    if not comando:
        comando = f"{dados.get('value1', '')} {dados.get('value2', '')} {dados.get('value3', '')}".strip()
    if not comando:
        return jsonify({"error": "Comando nao informado"}), 400
    logging.info(f"IFTTT Trigger: {comando}")
    resultado = executar_hermes(comando)
    return jsonify({"status": "ok", "comando": comando, "resultado": resultado})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n{'='*50}")
    print(f"  HERMES AGENT - Alexa Bridge")
    print(f"  Rodando em: http://localhost:{port}")
    print(f"  Webhook URL: http://localhost:{port}/alexa-webhook")
    print(f"  IFTTT URL:   http://localhost:{port}/ifttt-trigger")
    print(f"{'='*50}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
