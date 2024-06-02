import socket
import sys

def client_req(ip, port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Buat try dan except, try jika berhasil, except untuk kondisi error
    try:
        client_socket.connect((ip, port))
        request = f"GET /{filename} HTTP/1.1\r\nHost: {ip}\r\n\r\n"
        client_socket.sendall(request.encode())
        response = client_socket.recv(4096).decode()
        print(response)
    except TimeoutError:
        print("Timeout Error")
    except ConnectionRefusedError:
        print("Koneksi ditolak")
    except ConnectionAbortedError:
        print("Connection Aborted")
    finally:
        client_socket.close()

if len(sys.argv) != 4:
    print("FORMAT INPUT: python client.py <server_ip> <server_port> <filename>")
else:
    ip = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
    client_req(ip, port, filename)
