import socket
import sqlite3
import datetime
import threading

#  Configuración de parámetros del servidor 
HOST = 'localhost'
PORT = 5000
DB_NAME = 'mensajes.db'

#  Función para inicializar el socket 
def inicializar_socket():
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((HOST, PORT))  # Vinculamos el socket a la dirección y puerto
        servidor.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}...")
        return servidor
    except socket.error as e:
        print(f"Error al inicializar el socket: {e}")
        exit(1)

#  Función para inicializar la base de datos 
def inicializar_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Creamos la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
        exit(1)

#  Función para guardar un mensaje en la base de datos 
def guardar_mensaje(contenido, ip_cliente):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        fecha_envio = datetime.datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha_envio, ip_cliente))
        conn.commit()
        conn.close()
        return fecha_envio
    except sqlite3.Error as e:
        print(f"Error al guardar el mensaje: {e}")

#  Función para manejar una conexión de cliente 
def manejar_cliente(conn, addr):
    print(f"Conexión establecida con {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                mensaje = data.decode('utf-8')
                print(f"Mensaje recibido de {addr}: {mensaje}")
                timestamp = guardar_mensaje(mensaje, addr[0])
                if timestamp:
                    respuesta = f"Mensaje recibido: {timestamp}"
                    conn.sendall(respuesta.encode('utf-8'))
            except Exception as e:
                print(f"Error durante la comunicación con {addr}: {e}")
                break

#  Función principal para correr el servidor 
def correr_servidor():
    inicializar_db()
    servidor = inicializar_socket()
    while True:
        try:
            conn, addr = servidor.accept()  # Aceptamos una nueva conexión
            threading.Thread(target=manejar_cliente, args=(conn, addr)).start()
        except Exception as e:
            print(f"Error aceptando conexiones: {e}")

if __name__ == "__main__":
    correr_servidor()
