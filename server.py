from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logger.info(f'Запускаем сервер на порту {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Сервер остановлен')
        httpd.server_close()

if __name__ == '__main__':
    run_server()
