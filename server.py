import os
import socket
import traceback
import threading
from queue import Queue
import time
from cache import Constant

class Server():

    # 初始化连接
    def __init__(self, ip, port) -> None:
        # 创建socket
        # # （协议ipv4，tcp）
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip,port))
        self.s.listen(128)
    
    # 关闭
    def close(self):
        self.s.close()

    # 发送
    def send(self,client,message):
        # 使用套接字发送数据
        # 发送内容必须是 bytes 类型
        message_len = hex(len(bytes(message.encode('utf-8'))))
        message_len = message_len.replace("0x","").zfill(8)
        send_message = f"{message_len}{message}"
        client.send(Constant.TEXT_TYPE+bytes(send_message.encode('utf-8')))
        # queue_map["recvQ"].put(message)
        
        
        # 发送
    def send_file(self,client,file_path):
        # 使用套接字发送数据
        # 发送内容必须是 bytes 类型
        file_len = os.path.getsize(file_path)
        if file_len>=4294967295:
            print("文件过大：{file_len}")
            return
        file_len = hex(file_len)
        file_len = file_len.replace("0x","").zfill(8)
        send_message = f"{file_len}"
        client.send(Constant.FILE_TYPE+bytes(send_message.encode('utf-8')))
        with open(file_path,'rb') as f:
            for f_data in f:
                # data = f.read(1024)
                # if data:
                if f_data:
                    client.send(f_data)
                else:
                    print('传输完成')
                    break
        # send_message = f"{Constant.TEXT_TYPE}{file_len}{file_path}"
        # client.send(bytes(send_message.encode('utf-8')))

    # 接收
    def clientRecv(self,addr):
        # 接收数据 (单次接收最大字节数)
        while True:
            try:
                message_type = Constant.queue_map[addr]["client"].recv(1)
                message_len = int(Constant.queue_map[addr]["client"].recv(8), 16)                    
                reData = Constant.queue_map[addr]["client"].recv(message_len)
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
                    if message_type == Constant.TEXT_TYPE:
                        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        Constant.recvQ.put(f"{addr}\t{now}: \n{content}")
                    if message_type == Constant.FILE_TYPE:
                        Constant.queue_map[addr]['type']=Constant.FILE_TYPE
                        # now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        Constant.queue_map[addr]['fileQ'].put(f"{content}")
                #     return content
                # return None
    
    # 广播
    def broadcasting(self):
        while True:
            try:
                if Constant.recvQ.qsize():
                    message = Constant.recvQ.get()
                    for key in Constant.queue_map:
                        if Constant.queue_map[key].get('type') != Constant.FILE_TYPE:
                            self.send(Constant.queue_map[key]["client"], message=message)
                else:
                    time.sleep(0.3)
            except:
                print(traceback.format_exc())
                time.sleep(0.3)

    # 文件单播
    def up_file(self):
        while True:
            try:
                for key in Constant.queue_map:
                    if Constant.queue_map[key]["fileQ"].qsize():
                        filepath = Constant.queue_map[key]["fileQ"].get()
                        self.send_file(Constant.queue_map[key]["client"], filepath)
                    else:
                        time.sleep(0.3)
            except:
                print(traceback.format_exc())
                time.sleep(0.3)
            time.sleep(0.3)
    # 创建链接
    def create_client(self):
        # 接收数据 (单次接收最大字节数)
        while True:
            try:
                client,addr = self.s.accept()
                # if addr[0] not in ['192.168.5.130',
                #                    '172.22.15.2']:
                #     client.close()
                #     continue
                print(addr)
                if not Constant.queue_map.get(addr):
                    recvQ = Queue()
                    sendQ = Queue()
                    fileQ = Queue()
                    Constant.queue_map[addr] = {"recvQ":recvQ,
                                                "sendQ":sendQ,
                                                "fileQ":fileQ,
                                                "client":client}
                server_thread = threading.Thread(target=self.clientRecv,args=(addr,))
                server_thread.daemon = True
                server_thread.start()
                print(f"clinet:{addr}")
            except:
                print(traceback.format_exc())
            time.sleep(0.3)

server = Server("",7788)

create_client_thread = threading.Thread(target=server.create_client)
# create_client_thread.daemon = True

broadcasting_thread = threading.Thread(target=server.broadcasting)
up_file_thread = threading.Thread(target=server.up_file)
# broadcasting_thread.daemon = True

create_client_thread.start()
time.sleep(1)
broadcasting_thread.start()
time.sleep(1)
up_file_thread.start()
print("start ok")
