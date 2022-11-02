import threading
import traceback
import tkinter
from communication import comm
import time

class Client:
    
    def __init__(self) -> None:
        self.Text = tkinter.Text(self.root, width=100, height=20)
        self.Text.place(x=30, y=30)
        self.Text.bind("<MouseWheel>",self.Wheel)
        self.Text.config(state=tkinter.DISABLED)
        # 发送消息
        self.send_text = tkinter.Text(self.root, width=80, height=10)
        self.send_text.place(x=30, y=300)
        # 发送按钮
        send_button = tkinter.Button(text='Send', 
                                    font=('微软雅黑', 16), 
                                    command=lambda:self.send_event(),
                                    width=10,
                                    height=4
                                    )
        send_button.place(x=600, y=300)
        
    
    def send_event(self):
        comm.send(self.send_text.get("1.0",tkinter.END))
        self.send_text.delete("1.0",tkinter.END)
    
    def recv_message(self,message):
        self.Text.config(state=tkinter.NORMAL)     
        print(message)
        self.Text.insert(tkinter.END,message)
        self.Text.yview_moveto(1)
        self.Text.config(state=tkinter.DISABLED)
        
    def Wheel(self,event):#鼠标滚轮动作
        print(str(-1*(event.delta/120)))#windows系统需要除以120
        self.Text.yview_scroll(int(-1*(event.delta/120)), "units")
        # Text.yview_scroll(int(-1*(event.delta/120)), "units")

    def start(self):
        self.root.mainloop()

    root = tkinter.Tk()
    root.title = '通讯'  # 标题
    root.geometry('800x500+400+200')  # 窗体位置
    



if __name__ == "__main__":
    
    def recv(c):
        while True:
            message = comm.clientRecv()
            if message:
                c.recv_message(message)
            else:
                time.sleep(0.1)  
    
    c = Client()
    recv_thread = threading.Thread(target=recv,args=(c,))
    recv_thread.daemon = True
    recv_thread.start()
    c.start()
    
    print("close")
    