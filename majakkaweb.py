# Import server module
import http.server

# Import SocketServer module
import socketserver

# Import sys module
import sys

try:
    # Set the port number
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 5000

    # Set the IP address
    server_address = ('127.0.0.1', port)

    # Create object for handling HTTP requests
    Handler = http.server.SimpleHTTPRequestHandler

    # Run the web server forever to handle the HTTP requests
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("Web Server is running at http://localhost:%s" %port)
        httpd.serve_forever()

# Stopped the server
except KeyboardInterrupt:
    httpd.server_close()
    print("The server is stopped.")