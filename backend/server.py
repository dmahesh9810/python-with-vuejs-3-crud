import json
import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer

# MySQL connection setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'vue_crud'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')  # Allowed HTTP methods
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Allowed headers
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        # Handle OPTIONS request (CORS preflight)
        self._send_response({}, status_code=200)

    def do_GET(self):
        if self.path == '/items':
            self.fetch_items()
        else:
            self._send_response({"message": "Not Found"}, status_code=404)

    def do_POST(self):
        if self.path == '/items':
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length).decode('utf-8')
            data = json.loads(post_data)
            self.create_item(data)
        else:
            self._send_response({"message": "Not Found"}, status_code=404)

    def do_PUT(self):
        if self.path.startswith('/items/'):
            item_id = int(self.path.split('/')[-1])
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length).decode('utf-8')
            data = json.loads(post_data)
            self.update_item(item_id, data)
        else:
            self._send_response({"message": "Not Found"}, status_code=404)

    def do_DELETE(self):
        if self.path.startswith('/items/'):
            item_id = int(self.path.split('/')[-1])
            self.delete_item(item_id)
        else:
            self._send_response({"message": "Not Found"}, status_code=404)

    def fetch_items(self):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        connection.close()
        self._send_response(items)

    def create_item(self, data):
        name = data.get('name', '')
        if name:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
            connection.commit()
            item_id = cursor.lastrowid
            cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            connection.close()
            self._send_response(item, status_code=201)
        else:
            self._send_response({"message": "Name is required"}, status_code=400)

    def update_item(self, item_id, data):
        name = data.get('name', '')
        if name:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("UPDATE items SET name = %s WHERE id = %s", (name, item_id))
            connection.commit()
            cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            connection.close()
            if item:
                self._send_response(item)
            else:
                self._send_response({"message": "Item not found"}, status_code=404)
        else:
            self._send_response({"message": "Name is required"}, status_code=400)

    def delete_item(self, item_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        connection.commit()
        connection.close()
        self._send_response({"message": "Item deleted"}, status_code=200)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
