import socket

#  Configuración de parámetros del cliente 
HOST = 'localhost'
PORT = 5000

def main():
    try:
        # Configuración del socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Conectado al servidor {HOST}:{PORT}")

            while True:
                mensaje = input("Escribí un mensaje (o 'éxito' para salir): ")
                if mensaje.lower() == 'éxito':
                    print("Cerrando conexión...")
                    s.close
                    break
                s.sendall(mensaje.encode('utf-8'))
                data = s.recv(1024)
                print(f"Respuesta del servidor: {data.decode('utf-8')}")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. ¿Está corriendo?")
    except Exception as e:
        print(f"Error en el cliente: {e}")

if __name__ == "__main__":
    main()
