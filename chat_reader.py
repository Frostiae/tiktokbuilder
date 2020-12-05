import socket
from emoji import demojize

reading = True
laughs = 0
boring = 0

POSITIVE_FEEDBACK = ['lul', 'kekw', 'pog', 'lol', 'lmao']
NEGATIVE_FEEDBACK = ['residentsleeper', 'weirdchamp', 'pepepains', 'skip']


def main():
    sock = connect_chat()
    read_chat(sock)


def connect_chat() -> socket:
    sock = socket.socket()
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'frostiae'
    token = 'oauth:ff43z9nsw517llbuiqi03mbq7nxxpa'
    channel = '#xqcow'

    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))
    return sock


def read_chat(sock: socket):
    global laughs
    global boring
    while True:
        resp = sock.recv(2048).decode('utf-8')
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            if any(feedback in resp.lower() for feedback in POSITIVE_FEEDBACK):
                laughs += 1
            elif any(feedback in resp.lower() for feedback in NEGATIVE_FEEDBACK):
                boring += 1


def reset_chat():
    global laughs
    global boring
    laughs = 0
    boring = 0


if __name__ == '__main__':
    main()

