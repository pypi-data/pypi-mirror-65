from tkinter import ttk,Toplevel,Frame,Label,Button,Entry,StringVar
from tkinter import messagebox
import sys



class ParamsError(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self)
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo


class SettingsDialog(Toplevel):
    # 定义构造方法
    def __init__(self, parent, title = None, modal=True):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.resizable(width=0,height=0)  
        # 设置标题
        if title: self.title(title)
        self.parent = parent
        self.result = None
        self.m_Data = None
        self.m_Rows = StringVar(value=6)
        self.m_Columns =StringVar(value=6)
        self.m_X = StringVar(value=1)
        self.m_Y = StringVar(value=1)
        self.m_Beepers = StringVar(value= sys.maxsize)
        # 创建对话框的主体内容
        frame = Frame(self)
        # 调用init_widgets方法来初始化对话框界面
        self.initial_focus = self.init_widgets(frame)
        frame.pack(padx=5, pady=5)
        # 调用init_buttons方法初始化对话框下方的按钮
        self.init_buttons()
        # 根据modal选项设置是否为模式对话框
        if modal: self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        # 为"WM_DELETE_WINDOW"协议使用self.cancel_click事件处理方法
        self.protocol("WM_DELETE_WINDOW", self.cancel_click)
        # 根据父窗口来设置对话框的位置
        self.geometry("+%d+%d" % (parent.winfo_rootx()+parent.winfo_width()/2 -150,parent.winfo_rooty()+parent.winfo_height()/2 -120))
        # 让对话框获取焦点
        self.initial_focus.focus_set()
        self.wait_window(self)
    # 通过该方法来创建自定义对话框的内容
    def init_widgets(self, master):
        # 行
        Label(master, text='Rows:', font=('Times',10)).grid(row=1, column=0,sticky='e')
        Entry(master, font=('Times',10),textvariable=self.m_Rows).grid(row=1, column=1)
        # 列
        Label(master, text='Columns:', font=('Times',10)).grid(row=2, column=0,sticky='e')
        Entry(master, font=('Times',10),textvariable=self.m_Columns).grid(row=2, column=1)
        #karel初始位置X
        Label(master, text='Karel initial location x:', font=('Times',10)).grid(row=3, column=0,sticky='e')
        Entry(master, font=('Times',10),textvariable=self.m_X).grid(row=3, column=1)
        #karel初始位置Y
        Label(master, text='Karel initial location y:', font=('Times',10)).grid(row=4, column=0,sticky='e')
        Entry(master, font=('Times',10),textvariable=self.m_Y).grid(row=4, column=1)
        #beepers
        Label(master, text='Beepers in bag :', font=('Times',10)).grid(row=5, column=0,sticky='e')
        Entry(master, font=('Times',10),textvariable=self.m_Beepers).grid(row=5, column=1)
    # 通过该方法来创建对话框下方的按钮框
    def init_buttons(self):
        f = Frame(self)
        # 创建"确定"按钮,位置绑定self.ok_click处理方法
        w = Button(f, text="OK", width=10, command=self.ok_click, default='active')
        w.pack(side='left', padx=5, pady=5)
        # 创建"确定"按钮,位置绑定self.cancel_click处理方法
        w = Button(f, text="Cancel", width=10, command=self.cancel_click)
        w.pack(side='left', padx=5, pady=5)
        self.bind("<Return>", self.ok_click)
        self.bind("<Escape>", self.cancel_click)
        f.pack()
    # 该方法可对用户输入的数据进行校验
    def validate(self):
        # 可重写该方法
        try:
            rows = int(self.m_Rows.get() )
            columns = int (self.m_Columns.get() )
            x = int (self.m_X.get())
            y = int (self.m_Y.get())
            beepers =int(self.m_Beepers.get())
            if rows<1 or columns<1:
                raise ParamsError('行数和列数不能小于1')
            if x<1 or y<1 or x>columns or y>rows:
                raise ParamsError('起始位置必须在范围内')
            if beepers<0:
                raise ParamsError('beeper数目必须大于0')
        except Exception as e:
            messagebox.showerror("error",e)
            return False
        else:
            self.m_Data = {'rows':rows,'columns':columns,'x':x,'y':y,'beepers':beepers }
            return True
    def ok_click(self, event=None):
        # 如果不能通过校验，让用户重新输入
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        # 将焦点返回给父窗口
        self.parent.focus_set()
        # 销毁自己
        self.destroy()
        self.result = 'ID_OK'
        
    def cancel_click(self, event=None):
        # 将焦点返回给父窗口
        self.parent.focus_set()
        # 销毁自己
        self.destroy()
        self.result = 'ID_CANCEL'





