import socket
import traceback

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
    def send(self,message):
        # 使用套接字发送数据
        # 发送内容必须是 bytes 类型
        self.s.send(bytes(message.encode('utf-8')))

    # 接收
    def clientRecv(self):
        # 接收数据 (单次接收最大字节数)
        try:
            reData = self.s.recv(1024)
            # 尝试解码方式
            try:
                content = reData.decode("utf-8")
            except:
                content = reData.decode("GBK")
        except:
            traceback.format_exc()
        else:
            if content and len(content):
                return content
            return None

comm = Communication("127.0.0.1",77777)
