import tkinter
from tkinter import *
from tkinter import filedialog
import pandas
from tkinter import ttk
import Operator_grammar
import Operator_parsing
import Predict_parsing
import predict_grammar
import LR_1

class Grammar_tree:
    def __init__(self,type):
        self.type=type
        self.dataFrame = pandas.DataFrame(columns=['Left', 'Right'], dtype='str')
        self.index = 0
        self.tree_main()

    def open(self, *args):
        self.filename = filedialog.askopenfilename(initialdir='Grammar/'+self.type, title='Choose file')
        if len(self.filename) != 0:
            self.menubar.destroy()
            self.create_menu()
            self.dataFrame=pandas.read_csv(self.filename)
            obj = self.treeview.get_children()  # 获取所有对象
            for o in obj:
                self.treeview.delete(o)  # 删除对象
            self.index=len(self.dataFrame)
            for i in range(self.index):
                x=self.dataFrame.loc[i]
                self.treeview.insert('', END, values=[x[0],x[1]])

    def des(self, *args):
        try:
            self.labx.destroy()
            self.laby.destroy()
            self.entry_usrx.destroy()
            self.entry_usry.destroy()
        except:
            pass
    def create_newfile(self,*args):
        x=self.entry_usrx.get()
        y=self.entry_usry.get()
        self.dataFrame.loc[self.index]=[x,y]
        self.index+=1
        print(self.dataFrame)
        self.treeview.insert('', END, values=[x,y])
        self.des()
    def create(self,*args):
        self.labx = tkinter.Label(self.root, text='左部', bg='gray', fg='white',relief=GROOVE)
        self.labx.place(x=150, y=150, width=30, height=30)
        self.laby = Label(self.root,  text='右部',bg='gray', fg='white',relief=GROOVE)
        self.laby.place(x=150, y=180, width=30, height=30)
        self.entry_usrx = tkinter.Entry(self.root, relief=RIDGE, xscrollcommand=False,bd =5)
        self.entry_usrx.place(x=180, y=150, width=300, height=30)
        self.entry_usry = tkinter.Entry(self.root, relief=RIDGE, xscrollcommand=False,bd =5)
        self.entry_usry.place(x=180, y=180, width=300, height=30)
        self.entry_usry.bind('<Return>', self.create_newfile)
    def search_tag(self,text_widget, keyword, tag):
        pos = '1.0'
        while True:
            idx = text_widget.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            text_widget.tag_add(tag, idx, pos)
    def see_sort(self,*args):
        try:
            self.Ts.destroy()
        except:
            pass
        self.Ts = Toplevel()
        screenwidth = self.Ts.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.Ts.winfo_screenheight()  # 屏幕高度
        width = 600
        height = 420
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.Ts.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        self.Ts.wm_resizable(False, False)
        self.Ts.title(self.type+'文法分析')
        self.error_text = Text(self.Ts, width=120, height=40)
        if (self.type == '预测'):
            co1 = 'First'
            co2='Follow'
        else:
            co1 = 'First_VT'
            co2 = 'Last_VT'
        content='\n'
        for x in self.First.keys():
            content+=co1+'('+x+')==>'+str(self.First[x])+'\n'
        content+='\n'
        for x in self.Last.keys():
            content+=co2+'('+x+')==>'+str(self.Last[x])+'\n'
        self.error_text.insert(1.0, content)
        self.error_text.tag_config('tag', foreground='red')
        self.error_text.tag_config('tag1', foreground='blue')
        self.search_tag(self.error_text, 'First', 'tag')
        self.search_tag(self.error_text, 'Follow', 'tag1')
        self.search_tag(self.error_text, 'First_VT', 'tag')
        self.search_tag(self.error_text, 'Last_VT', 'tag1')

        self.error_text.pack(side="left", fill="both",expand=True)
        self.vsb = tkinter.Scrollbar(self.Ts, orient="vertical", command=self.error_text.yview)
        self.vsb.pack(side="right", fill="y")
        self.error_text.config(state=DISABLED)
    def analy_string(self,*args):
        string=self.entry_usrz.get()
        string=string.split(' ')
        if(self.type=='算符' or self.type=='LR'):
            if (self.type == '算符'):
                self.process=Operator_parsing.Operator_parsing().analyse_main(string,self.result)
            else:
                self.LR_parsing.SLR(string)
                self.process = self.LR_parsing.process
            columns=self.process[0]
            self.trees = ttk.Treeview(self.Ts, show="headings",height=16)  # 表格
            self.trees["columns"] = columns
            self.trees.column(columns[0], width=150, anchor='w')  # #设置列
            self.trees.heading(columns[0], text=columns[0])  # #设置显示的表头名
            self.trees.column(columns[1], width=150, anchor='e')  # #设置列
            self.trees.heading(columns[1], text=columns[1])  # #设置显示的表头名
            for x in columns[2:]:
                self.trees.column(x, width=150,anchor='center')  # #设置列
                self.trees.heading(x, text=x)  # #设置显示的表头名
            self.s = ttk.Style(self.trees)
            self.s.theme_use('alt')
            for i in range(1,len(self.process)):
                self.trees.insert("", i, text=i, values=(self.process[i]))
            self.trees.place(x=0,y=70)
        else:
            self.process = Predict_parsing.pre_parsing().analyse(string, self.result)
            columns = self.process[0]
            self.trees = ttk.Treeview(self.Ts, show="headings", height=16)  # 表格
            self.s = ttk.Style(self.trees)
            self.s.theme_use('alt')
            self.trees["columns"] = columns
            self.trees.column(columns[0], width=200, anchor='w')  # #设置列
            self.trees.heading(columns[0], text=columns[0])  # #设置显示的表头名
            self.trees.column(columns[1], width=200, anchor='e')  # #设置列
            self.trees.heading(columns[1], text=columns[1])  # #设置显示的表头名
            for x in columns[2:]:
                self.trees.column(x, width=200, anchor='center')  # #设置列
                self.trees.heading(x, text=x)  # #设置显示的表头名
            for i in range(1, len(self.process)):
                self.trees.insert("", i, text=i, values=(self.process[i]))
            self.trees.place(x=0, y=70)

    def enter_see(self,*args):
        try:
            self.Ts.destroy()
        except:
            pass
        self.Ts = Toplevel()
        screenwidth = self.Ts.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.Ts.winfo_screenheight()  # 屏幕高度
        width = 600
        height = 420
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.Ts.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        self.Ts.wm_resizable(False, False)
        self.Ts.title(self.type+'文法分析测试')
        lab=tkinter.Label(self.Ts,text='【测试串的终结符请以一个空格隔开】',bg='gray',fg='white',relief=GROOVE)
        lab.place(x=0,y=0,width=600,height=20)
        if(self.type!='LR'):
            temm=self.result['Terminator']
        else:
            temm=self.LR_parsing.terminalset
        end=''
        for x in temm:
            if(x!='@'):
                end=end+x+' '
        Label=tkinter.Label(self.Ts,text=end,bg='white',fg='green',relief=GROOVE)
        Label.place(x=0,y=20,width=600,height=20)
        Label1 = tkinter.Label(self.Ts, text='测试串', bg='white', fg='red',relief=GROOVE)
        Label1.place(x=0, y=40, width=40, height=30)
        self.entry_usrz = tkinter.Entry(self.Ts, relief=RIDGE, xscrollcommand=False, bd=5)
        self.entry_usrz.place(x=40, y=40, width=560, height=30)
        self.entry_usrz.bind('<Return>', self.analy_string)
    def see_table(self,*args):
        try:
            self.Ts.destroy()
        except:
            pass
        self.Ts = Toplevel()
        screenwidth = self.Ts.winfo_screenwidth()
        screenheight = self.Ts.winfo_screenheight()
        if(self.type=='算符'):
            content = self.result['Table']
            x=len(content)*30
            y=len(content)*20
            self.Ts.title('算符优先分析表')
        elif(self.type=='预测'):
            content = self.result['Table']
            self.Ts.title('预测分析表')
            x=len(content[0])*50
            y=len(content)*20
        else:
            content=self.LR_parsing.cotent
            self.Ts.title('LR-Action-GO分析表')
            x = len(content[0]) * 50
            y = len(content) * 20
        alignstr = '%dx%d+%d+%d' % (x, y, (screenwidth - x) / 2, (screenheight - y) / 2)
        self.Ts.geometry(alignstr)
        self.tree = ttk.Treeview(self.Ts, show="headings")  # #创建表格对象
        col = content[0]
        self.s = ttk.Style(self.tree)
        self.s.theme_use('alt')
        self.tree["columns"] =content[0]
        for x in col:
            self.tree.column(x, width=20)  # #设置列
            self.tree.heading(x, text=x)  # #设置显示的表头名
        for i in range(1,len(content)):
            self.tree.insert("", i, text=i, values=(content[i]))
        self.tree.pack(fill='both', expand=True)
    def see_DNF(self,*args):
        try:
            self.Ts.destroy()
        except:
            pass
        self.Ts = Toplevel()
        screenwidth = self.Ts.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.Ts.winfo_screenheight()  # 屏幕高度
        width = 600
        height = 420
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.Ts.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        self.Ts.wm_resizable(False, False)
        self.Ts.title(self.type+'文法分析')
        self.error_text = Text(self.Ts, width=120, height=40)
        content=''
        for result in self.LR_parsing.pointset:
            content+='状态'+str(result.id)+'\n'
            for onepro in result.status:
                content+=str(onepro.left)+'->'+str(onepro.right)+'\n'
        self.error_text.insert(1.0, content)
        self.error_text.tag_config('tag', foreground='red')
        self.search_tag(self.error_text, '状态', 'tag')
        self.error_text.pack(side="left", fill="both", expand=True)
        self.vsb = tkinter.Scrollbar(self.Ts, orient="vertical", command=self.error_text.yview)
        self.vsb.pack(side="right", fill="y")
        self.error_text.config(state=DISABLED)

    def run(self,*args):
        if(self.index>0):
            self.menubar.destroy()
            self.create_menu()
            if(self.type=='算符'):
                self.result=Operator_grammar.Operator_grammar(self.dataFrame).return_result()
                self.fmenu=Menu(self.menubar, tearoff=0)
                self.fmenu.add_command(label="查看First_VT,Last_VT", command=self.see_sort)
                self.fmenu.add_command(label="查看分析表", command=self.see_table)
                self.fmenu.add_command(label="输入串测试", command=self.enter_see)
                self.s=self.menubar.add_cascade(label="功能查看",menu=self.fmenu)
                self.First=self.result['First_VT']
                self.Last=self.result['Last_VT']
            elif(self.type=='预测'):
                self.result =predict_grammar.PREE(self.dataFrame).return_result()
                self.fmenu = Menu(self.menubar, tearoff=0)
                self.fmenu.add_command(label="查看First,Follow", command=self.see_sort)
                self.fmenu.add_command(label="查看分析表", command=self.see_table)
                self.fmenu.add_command(label="输入串测试", command=self.enter_see)
                self.s = self.menubar.add_cascade(label="功能查看", menu=self.fmenu)
                self.First = self.result['First']
                self.Last = self.result['Follow']
            elif(self.type=='LR'):
                self.LR_parsing=LR_1.LR_parsing(self.dataFrame)
                self.fmenu = Menu(self.menubar, tearoff=0)
                self.fmenu.add_command(label="查看项目集规范族", command=self.see_DNF)
                self.fmenu.add_command(label="查看分析表", command=self.see_table)
                self.fmenu.add_command(label="输入串测试", command=self.enter_see)
                self.s = self.menubar.add_cascade(label="功能查看", menu=self.fmenu)

    def create_menu(self):
        self.menubar = Menu(self.root, tearoff=False)
        self.menubar.add_command(label="打开文法文件", command=self.open)
        self.menubar.add_command(label="运行文法", command=self.run)
        self.root.config(menu=self.menubar)
    def delet(self,*args):
        self.dataFrame=pandas.DataFrame(columns=['Left', 'Right'], dtype='str')
        self.index = 0
        obj = self.treeview.get_children()
        for o in obj:
            self.treeview.delete(o)  # 删除对象
        self.menubar.destroy()
        self.create_menu()
    def tree_main(self):
        self.root = Tk()  # 初始框的声明
        self.root.title(self.type+'分析法测试')
        self.root.wm_resizable(False, False)
        screenwidth = self.root.winfo_screenwidth() # 屏幕宽度
        screenheight = self.root.winfo_screenheight()  # 屏幕高度
        width = 600
        height = 420
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        tabel_frame = tkinter.Frame(self.root)
        tabel_frame.pack()
        self.create_menu()
        right_menubar = tkinter.Menu(self.root,tearoff=False)
        right_menubar.add_command(label="添加产生式",command=self.create)
        right_menubar.add_command(label="清空产生式", command=self.delet)
        def xShowMenu(event):
            right_menubar.post(event.x_root, event.y_root)  # #将菜单条绑定上事件，坐标为x和y的root位置

        self.root.bind("<Button-3>", xShowMenu)
        self.root.bind('<Double-Button-1>', self.des)

        columns = ("产生式左部", "产生式右部")
        self.treeview = ttk.Treeview(self.root, height=18, show="headings", columns=columns)  # 表格
        self.s = ttk.Style(self.treeview)
        self.s.theme_use('alt')
        self.treeview.tag_configure('tag', foreground='green',background='blue')
        self.treeview.column("产生式左部", width=150)  # 表示列,不显示
        self.treeview.column("产生式右部", width=350)
        self.treeview.heading("产生式左部", text="产生式左部")  # 显示表头
        self.treeview.heading("产生式右部", text="产生式右部")
        self.treeview.pack()
        self.root.mainloop()