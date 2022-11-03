from queue import Queue

queue_map = {}

# sendQ = Queue()
recvQ = Queue()

TEXT_TYPE = b'0'
FILE_TYPE = b'1'
IP = '192.168.0.108'
PORT = 7788