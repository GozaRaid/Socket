from socket import *
import threading

# Tentukan port dan alamat server
port = 5555
ip = gethostbyname(gethostname())
addr = (ip,port)


#objek socket dengan IPv4 dan TCP
server = socket(AF_INET,SOCK_STREAM)
server.bind(addr)

#parse http dan ambil isinya
def receive(msg):
    #ambile headernya
    header = msg.split('\n')
    #ambil baris pertama dan kalimat ke 2 (nama file)
    file = header[0].split()[1]
    
    try:
        # Coba buka file yang diminta dan baca isinya
        file = open(f".{file}", "r")
        content = file.read()
        file.close()
        # Jika file ditemukan, siapkan respons HTTP yang berhasil
        response = "HTTP/1.1 200 OK\n\n" + content
    except FileNotFoundError:
        # Jika file tidak ditemukan, siapkan respons 404 Not Found
        response = "HTTP/1.1 404 Not Found\n\nFile Not Found!"
    except Exception as e:
        # Tangani kesalahan lainnya dan kirim pesan kesalahan kembali ke klien
        response = f"HTTP/1.1 500 Internal Server Error\n\nError: {str(e)}"

    return response

#fungsi untuk terima pesan dan koneksi klien
def handle_client(socket,adr):
    print("koneksi dari: ",adr)
    while True:
        msg = socket.recv(1024).decode()
        #Jika dapat pesan maka lakukan receive dan hasilnya kembalikan ke klien dan encode
        if msg:
            content = receive(msg)
            socket.sendall(content.encode())
            break
    socket.close()

#fungsi untuk mulai server dan menunggu koneksi masuk
def start():
    server.listen()
    print(f"(Listening), Buka http://{ip}:{port}")
    #loop untuk menerima koneksi
    while  True:
        socket,adr = server.accept()
        #thread baru untuk setiap klien
        thread = threading.Thread(target=handle_client,args=(socket,adr))
        thread.start()
        print("Success")

print("start")
start()



            
