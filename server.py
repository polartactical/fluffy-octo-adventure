#!/usr/bin/env python3
import socket
import ssl
import MySQLdb

# Set the secret key
secret_key = 'supersecret'

# Create a listening socket on port 8888
host = '0.0.0.0'
port = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(5)
print(f'Listening on port {port}...')

# Connect to MySQL
host = 'localhost'
dbname = 'temp_fl'
username = 'sqluser'
password = 'sqlpassword'
db = MySQLdb.connect(host=host, user=username, passwd=password, db=dbname)
db.set_character_set('utf8mb4')
cursor = db.cursor()
print('Connected to MySQL...')

# Handle incoming connections
while True:
    conn, addr = sock.accept()
    print('Client connected')
    try:
#        data = conn.recv(1024).decode()
        data = conn.recv(1024).decode('latin-1')
        print(f'Incoming data {data}')
        if ',' not in data:
            continue # data does not contain expected values, so skip to next iteration
        sec_key, user_name, user_temp = data.split(",")
        if sec_key != secret_key.decode() or not user_name or not user_temp:
            print('Error: secret key missing or incorrect, or username and temp parameters are required')
            continue
        cursor.execute(f"INSERT INTO temp_fl (user_name, temp) VALUES ('{user_name}', '{user_temp}')")
        db.commit()
        print(f"Inserted row with ID {cursor.lastrowid}")
    except (ssl.SSLError, ConnectionResetError):
        pass
    conn.close()
