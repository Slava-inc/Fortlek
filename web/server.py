# web/server.py
import http.server
import socketserver
import threading
import os
import webbrowser

class AudioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
        super().__init__(*args, directory=web_dir, **kwargs)

    
    def do_GET(self):
        if self.path == "/":
            self.path = "/audio_guide.html"
        return super().do_GET()

class WebServer:
    def __init__(self, port=8000):
        self.port = port
        self.httpd = None
        self.thread = None
        self.web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
        # Создаём папку web если её нет
        os.makedirs(self.web_dir, exist_ok=True)
            
    def start(self):
        if self.thread and self.thread.is_alive():
            return
            
        socketserver.TCPServer.allow_reuse_address = True
        self.httpd = socketserver.TCPServer(("", self.port), AudioHandler)
        
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
        print(f"Веб-сервер запущен на http://localhost:{self.port}")
    
    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
    
    def is_running(self):
        return self.thread and self.thread.is_alive()