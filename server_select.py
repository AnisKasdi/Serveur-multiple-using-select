#!/usr/bin/python3
import socket
import sys
import select

def server_select():
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    port = 7777
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(5)  # Le serveur peut accepter 5 connexions en attente
    print("Serveur TCP en écoute...")

    # Liste des sockets clients
    clients = [server_socket]

    while True:
        # On attend que les sockets soient prêtes pour la lecture
        ready_to_read, _, _ = select.select(clients, [], [])

        for sock in ready_to_read:
            if sock == server_socket:
                # Un nouveau client tente de se connecter
                client_socket, client_address = server_socket.accept()
                clients.append(client_socket)
                print(f"Client connecté depuis {client_address}")
            else:
                # Un client existant envoie des données
                try:
                    data = sock.recv(1500)
                    if not data:
                        # Si aucune donnée n'est reçue, cela signifie que le client a fermé la connexion
                        print(f"Client {sock.getpeername()} déconnecté")
                        clients.remove(sock)
                        sock.close()
                    else:
                        # Envoyer les données au client (echo)
                        print(f"Données reçues de {sock.getpeername()}: {data.decode()}")
                        sock.sendall(data)
                except:
                    print("Erreur avec un client")
                    clients.remove(sock)
                    sock.close()

server_select()
