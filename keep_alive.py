from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>T-800 is Online and Monitoring!</h1><p>Esta pagina eh uma gambiarra para a Render nao desligar o servidor.</p></body></html>")
        
    def log_message(self, format, *args):
        pass # Esconde os logs de acesso para não poluir o terminal

def run_server():
    # A Render exige que o Web Service escute na porta definida pela variável $PORT (padrão 10000)
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"[Keep-Alive] Servidor web falso rodando na porta {port} para enganar a Render...")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
