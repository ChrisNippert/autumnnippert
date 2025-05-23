import http.server
import socketserver
import os
import socket
import sys

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="dist", **kwargs)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port):
    port = start_port
    while is_port_in_use(port):
        print(f"Port {port} is in use, trying {port + 1}...")
        port += 1
    return port

def main():
    try:
        # Find an available port
        port = find_available_port(PORT)
        
        # Create the server
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"\nServing at http://localhost:{port}")
            print("Press Ctrl+C to stop the server\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 