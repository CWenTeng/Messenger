import socket
import traceback

from cache import Constant
class Communication(object):

    # 初始化连接
    def __init__(self, ip, port) -> None:
        # 创建socket
        # # （协议ipv4，tcp）
        # super().__init__(*args, **kwargs)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.s)
        # ip = "192.168.1.105"
        # port = 7788
        # 连接
        self.s.connect((ip,port))
    
    # 关闭
    def close(self):
        self.s.close()

    # 发送
    def send(self,message,type = Constant.TEXT_TYPE):
        # 使用套接字发送数据
        # 发送内容必须是 bytes 类型
        message_len = hex(len(bytes(message.encode('utf-8'))))
        message_len = message_len.replace("0x","").zfill(8)
        send_message = f"{message_len}{message}"
        if type == Constant.TEXT_TYPE:
            self.s.send(Constant.TEXT_TYPE+bytes(send_message.encode('utf-8')))
        if type == Constant.FILE_TYPE:
            self.s.send(Constant.FILE_TYPE+bytes(send_message.encode('utf-8')))
        # self.s.send(bytes(message.encode('utf-8')))

    # 接收
    def clientRecv(self):
        # 接收数据 (单次接收最大字节数)
        try:
            message_type = self.s.recv(1)
            message_len = int(self.s.recv(8), 16)
            print(f"输出长度{message_len}")
            if message_type == Constant.TEXT_TYPE:
                reData = self.s.recv(message_len)
                # 尝试解码方式
                try:
                    content = reData.decode("utf-8")
                except:
                    content = reData.decode("GBK")
            elif message_type == Constant.FILE_TYPE:
                content = None
                
        except:
            traceback.format_exc()  
        else:
            if content and len(content):
                return (Constant.TEXT_TYPE,content)
            return None
        
        
            # 接收
    def clientRecv_file(self,tar):
        # 接收数据 (单次接收最大字节数)
        try:
            message_type = self.s.recv(1)
            message_len = int(self.s.recv(8), 16)
            if message_type == Constant.FILE_TYPE:
                content = 0
                with open(tar,'wb') as f:
                    while message_len > content:
                        data = self.s.recv(1024)
                        # if data:
                        f.write(data)
                        content += len(data)
                        yield (content,message_len)
                        # else:
                        #     break
                print("{content} / {message_len}")
                print("接收完毕")
                        
        except:
            print(traceback.format_exc())
        else:
            print("ttt")
            return "传输完毕"
        return "传输完毕?"

comm = Communication(Constant.IP,Constant.PORT)
print()

