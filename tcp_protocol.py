import queue, threading,socket, sys

class TCP_Logic:
    def tcp_protocol_serverSide():
        HOST = "127.0.0.1"
        PORT = 40252
        msgs = queue.Queue()
        clients = []
        clients_lock = threading.Lock()
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created successfully..")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket
        s.bind((HOST, PORT))
        # Start listerning
        s.listen(6)
        print("Server is listerning...")
        
        def  handle_conn (conn, addr, clients, clients_lock, msgs):
                with clients_lock:
                    clients.append(conn)
                print(f"conneted to {addr}")
                try:
                    while True:
                        # Read Msg form client
                        message = conn.recv(1024)
                        if not message:
                            break
                        msgs.put((conn, message))
                finally:
                    with clients_lock:
                        clients.remove(conn)
                    conn.close()
                    print(f"Connection closed: {addr}")

        #  Broadcast msgs
        def broadcaster(msgs, clients, clients_lock):
                while True:
                    sender, msg = msgs.get()
                    with clients_lock:
                        for c in clients:
                            if c != sender:
                                print(f"Broadcasting message: {msg.decode(errors='ignore')}")
                                c.sendall(msg)

        # start broadcasting
        threading.Thread(
            target=broadcaster, 
            args=(msgs, clients, clients_lock),
            daemon=True
            ).start()

        #  Accept Connection request from client (loop)
        try:
            while True:
                conn, addr = s.accept()
                # Start handling connections
                threading.Thread(
                    target=handle_conn,
                    args=(conn, addr, clients, clients_lock, msgs),
                    daemon=True
                    ).start()
        except KeyboardInterrupt as ki:
            print("\n Shutting down Server...")
            with clients_lock:
                for c in clients:
                    c.close()
                s.close()
                sys.exit(0)  #clean exit

    def tcp_Protocol_clientSide():
        HOST = "127.0.0.1"
        PORT = 40252
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establish connection to server
        s.connect((HOST, PORT))
        # Recieve user_input
        username = input("Enter a username: ")
        msg = input("\nMessage: ")
        msgPrepend = f"<<{username}>> {msg}"
        send_msg = bytearray(msgPrepend, "UTF-8")

        # Continue communication
        while True:
            # Send Msg to server
            s.send(send_msg)
            # Recieve Reply from server
            s.recv(2040)
    

TCP_Logic.tcp_protocol_serverSide()

