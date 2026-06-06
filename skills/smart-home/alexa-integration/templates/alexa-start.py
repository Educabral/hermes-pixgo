#!/usr/bin/env python3
"""Iniciador da Alexa Bridge com Flask + ngrok tunnel.
Uso: python alexa_start.py
"""
import subprocess, sys, os, time, threading

HERMES_HOME = os.path.expanduser("~/AppData/Local/hermes")
BRIDGE_SCRIPT = os.path.join(HERMES_HOME, "alexa_bridge.py")

def start_flask():
    print("[+] Iniciando servidor webhook Alexa...")
    return subprocess.Popen([sys.executable, BRIDGE_SCRIPT], cwd=HERMES_HOME)

def start_ngrok(port=5000):
    print(f"[+] Abrindo tunnel ngrok para porta {port}...")
    try:
        from pyngrok import ngrok
        public_url = ngrok.connect(port, "http")
        print(f"\n{'='*60}")
        print(f"  ✅ ALEXA BRIDGE ONLINE!")
        print(f"  📡 URL Publica: {public_url}")
        print(f"  📍 Webhook:     {public_url}/alexa-webhook")
        print(f"  📍 IFTTT:       {public_url}/ifttt-trigger")
        print(f"{'='*60}\n")
        print(f"  No IFTTT, crie Applet:")
        print(f"     SE: Alexa ('disparar {{comando}}')")
        print(f"     ENTAO: Webhook -> POST ->")
        print(f"     URL: {public_url}/ifttt-trigger")
        print(f"     Body: {{\\\"command\\\":\\\"{{{{comando}}}}\\\"}}")
        print(f"\n  Pressione Ctrl+C para parar.\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[+] Parando...")
            ngrok.kill()
    except ImportError:
        print("[!] pyngrok nao instalado: pip install pyngrok")
        print("[!] Ou use ngrok manualmente: ngrok http {port}")

if __name__ == "__main__":
    print("🚀 INICIANDO ALEXA BRIDGE")
    flask_proc = start_flask()
    time.sleep(2)
    try:
        import requests
        r = requests.get("http://localhost:5000/", timeout=3)
        print(f"[+] Servidor local OK: {r.json()}")
    except:
        print("[!] Servidor local nao respondeu")
    start_ngrok()
    flask_proc.wait()
