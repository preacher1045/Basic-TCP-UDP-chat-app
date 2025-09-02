import queue, threading,socket, sys

class TCP_Logic:
    def tcp_protocol_serverSide():
        HOST = "127.0.0.1"
        PORT = 40252
        msgs = queue.Queue()
        clients = []
        clients_lock = threading.Lock()
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, backlog=None, reuse_port=False)
        print("Socket created successfully..")
        # Bind the socket
        s.bind((HOST, PORT))
        # Start listerning
        s.listen(6)
        print("Server is listerning...")

        # Accept Connection request from client
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_conn, args=(conn, addr, clients), daemon=True)
        
            def  handle_conn (conn, addr, clients):
                with clients_lock:
                    clients.append(conn)
                print(f"conneted to {addr}")
                try:
                    while True:
                        
                        # Read Msg form client
                        message = conn.recv(2040)
                        if not message:
                            with clients_lock:
                                clients.remove(conn)
                            break
                        msgs.put((conn, message))
                finally:
                    with clients_lock:
                        clients.remove(conn)
                        conn.close()
            
            handle_conn(conn, addr, clients)

            #  Broacast msgs
            def broadcaster(msgs, clients):
                while True:
                    threading.Thread(target=broadcaster, args=(msgs, clients), daemon=True)
                    sender, msg = msgs.get()
                    with clients_lock:
                        for c in clients:
                            if c != sender:
                                c.sendall(msg)

            broadcaster(msgs, clients)

    
    def tcp_Protocol_clientSide():
        HOST = "127.0.0.1"
        PORT = 40252
        msg = "Hello server, this is client"
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establish connection to server
        s.connect((HOST, PORT))
        # Send Msg to server
        s.send(2024)
        # Recieve Reply from server
        s.recv(2040)
    

TCP_Logic.tcp_protocol_serverSide()

