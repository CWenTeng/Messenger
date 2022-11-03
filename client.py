import threading
import traceback
import ctypes
from cache import Constant
import tkinter
from communication import comm
from communication import Communication
import time


class Down_win:
    def create(self):
        self.root = tkinter.Toplevel()
        self.root.title('下载子窗')  # 标题
        self.root.geometry('400x200')
        self.source_path_entry = tkinter.Entry(self.root, width=50)
        self.source_path_entry.place(x=10,y=10)
        self.targ_path_entry = tkinter.Entry(self.root, width=50)
        self.targ_path_entry.place(x=10,y=50)

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
                                    height=2
                                    )
        send_button.place(x=600, y=355)
        down_button = tkinter.Button(text='Down', 
                                    font=('微软雅黑', 16), 
                                    command=lambda:self.down_win(),
                                    width=10,
                                    height=1
                                    )
        down_button.place(x=600, y=300)
        
    
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
    root.title('通讯')  # 标题
    root.geometry('800x500+400+200')  # 窗体位置
    
    # root.after(1000,root2)

    def down(self,win):
        tar = win.targ_path_entry.get()
        source = win.source_path_entry.get()
        win.targ_path_entry.place_forget()
        win.source_path_entry.place_forget()
        targ_path_entry = tkinter.Entry(win.root, width=50)
        targ_path_entry.place(x=10,y=50)
        targ_path_entry.config(state=tkinter.DISABLED)
        comm = Communication(Constant.IP,Constant.PORT)
        comm.send(source,Constant.FILE_TYPE)
        comm_file = comm.clientRecv_file(tar)
            # persent = next(comm_file)
        i = 0.1;
        while True:
            try:
                persent = next(comm_file)
                if persent[2]/persent[1] >= i:
                    i += 0.1
                    print(persent)
                # TODO 进度条待改造
                # targ_path_entry.config(state=tkinter.NORMAL)
                # targ_path_entry.insert("1.0",persent)
                # targ_path_entry.delete(0,tkinter.END)
                # targ_path_entry.insert(0,f"{persent[0]} / {persent[1]}")
                # targ_path_entry.config(state=tkinter.DISABLED)
            except Exception as e:
                print(traceback.format_exc())
                print(e)
                break


    def down_win(self):
        win = Down_win()
        win.create()
        down_button = tkinter.Button(win.root,text='Down', 
                            font=('微软雅黑', 16), 
                            command=lambda:self.down(win),
                            width=4
                            )
        down_button.place(x=300,y=80)


if __name__ == "__main__":
    
    def recv(c):
        while True:
            message = comm.clientRecv()
            if message:
                if message[0] == Constant.TEXT_TYPE:
                    c.recv_message(message[1])
                elif message[0] == Constant.FILE_TYPE:
                    pass
            else:
                time.sleep(0.1)  
    
    c = Client()
    recv_thread = threading.Thread(target=recv,args=(c,))
    recv_thread.daemon = True
    recv_thread.start()
    c.start()
    
    print("close")
    