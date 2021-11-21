from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import socketserver
import socket
import sys
import fcntl
import struct
import os


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed_path = urlparse(self.path)
        message_parts = [
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                                        self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
            'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        print(message)

        polku = parsed_path.path

        if polku == "/":
            f = open('index.html', 'r')
            message = f.read()

        if polku == "/aloita":
            os.system('sudo python3 majakka.py s 10 sat')

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(message, 'utf-8'))
        return


class IpHandler:
    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])


if __name__ == '__main__':

    try:
        # Set the port number
        if sys.argv[1:]:
            port = int(sys.argv[1])
        else:
            port = 80

        httpd = socketserver.TCPServer(("", port), GetHandler)

        local_ip = IpHandler().get_ip_address('wlan0')
        osoite = "http://"+local_ip

        if port != 80:
            osoite = osoite + ":" + str(port)

        print("Majakka-palvelin osoitteessa " + osoite)
        httpd.serve_forever()

    # Stopped the server
    except KeyboardInterrupt:
        httpd.server_close()
        print("Majakka-palvelin sammutettu.")
