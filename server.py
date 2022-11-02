import socket
import traceback
import threading
from queue import Queue
import time
from cache import Constant

class Server():

    # 初始化连接
    def __init__(self, ip, port) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip,port))
        self.s.listen(5)
    
    # 关闭
    def close(self):
        self.s.close()

    # 发送
    def send(self,client,message):
        # 使用套接字发送数据
        # 发送内容必须是 bytes 类型
        client.send(bytes(message.encode('utf-8')))
        # queue_map["recvQ"].put(message)

    # 接收
    def clientRecv(self,addr):
        # 接收数据 (单次接收最大字节数)
        while True:
            try:
                reData = Constant.queue_map[addr]["client"].recv(10240)
                # 尝试解码方式
                try:
                    content = reData.decode("utf-8")
                except:
                    content = reData.decode("GBK")
            except:
                print(traceback.format_exc())
                print("baocuo")
                try:
                    print(f"try close {addr} client")
                    Constant.queue_map[addr]["client"].close()
                    Constant.queue_map.pop(addr)
                except:
                    print(traceback.format_exc())
                    break
                time.sleep(0.3)
            else:
                if content and len(content):
                    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    Constant.recvQ.put(f"{now}\n{addr}: {content}")
                #     return content
                # return None
    
    # 广播
    def broadcasting(self):
        while True:
            try:
                if Constant.recvQ.qsize():
                    message = Constant.recvQ.get()
                    for key in Constant.queue_map:
                        self.send(Constant.queue_map[key]["client"], message=message)
                else:
                    time.sleep(0.3)
            except:
                print(traceback.format_exc())
                time.sleep(0.3)

    # 创建链接
    def create_client(self):
        # 接收数据 (单次接收最大字节数)
        while True:
            try:
                client,addr = self.s.accept()
                if not Constant.queue_map.get(addr[0]):
                    recvQ = Queue()
                    sendQ = Queue()
                    Constant.queue_map[addr[0]] = {"recvQ":recvQ,"sendQ":sendQ,"client":client}
                server_thread = threading.Thread(target=self.clientRecv,args=(addr[0],))
                server_thread.daemon = True
                server_thread.start()
            except:
                print(traceback.format_exc())
            time.sleep(0.3)

server = Server("0.0.0.0",9999)

create_client_thread = threading.Thread(target=server.create_client)
create_client_thread.daemon = True

broadcasting_thread = threading.Thread(target=server.broadcasting)
# broadcasting_thread.daemon = True

create_client_thread.start()
broadcasting_thread.start()

print()