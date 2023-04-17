import socket
import threading


def threaded(test_message):
    host = '10.171.227.118'
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    message = test_message

    while True:

        # sending the message and receiving the response
        s.send(message.encode('ascii'))
        data = s.recv(1024)
        print('Received from the server :', str(data.decode('ascii')))

        # prompt on the client side to continue the connection
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the connection once the while loop is broken
    s.close()


def Main():
    test_message = "poop from client"
    thread1 = threading.Thread(target=threaded, args=(test_message,))
    thread1.start()
    thread1.join()
    print("done!")


if __name__ == '__main__':
    Main()
