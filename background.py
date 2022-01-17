import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import os
import tkinter.messagebox
import Lexical_Analysis
from tkinter import ttk
import pandas
import Parsing
import Mid_code
import Target_code
import Explanation

class TextLineNumbers(tk.Canvas):#行标类
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):#文本类
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs,)
        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)
        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

class Example(tk.Frame):#创建一个可编辑的文本
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self,*args, **kwargs)
        self.text = CustomText(self,width=110, height=32)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=25)
        self.linenumbers.attach(self.text)
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def update_size(self, event):
        widget_width = 0
        widget_height = float(event.widget.index(tk.END))
        for line in event.widget.get("1.0", tk.END).split("\n"):
            if len(line) > widget_width:
                widget_width = len(line) + 1
        event.widget.config(width=widget_width, height=widget_height)
    def _on_change(self, event):
        self.linenumbers.redraw()
    def insert_text(self,content):
        if content is not -1:
            self.text.delete(1.0, END)
            self.text.insert(1.0, content)

class Note():
    def __init__(self):
        self.file = []
        self.bts=[]
        self.file_path=[]
        self.contents=[]
        self.error_describe=pandas.read_pickle('CSV\Errors.pickle')
        self.index=0
        locat=str(__file__).split('/')
        self.locat=''
        for i in range(len(locat)-1):
            self.locat+=locat[i]+'/'
        self.koo=[] #存储所以控件
        self.msd = Tk()
        self.createUI()
        self.msd.mainloop()
    def createUI(self):#创建主界面
        # create menu
        #加载图片
        self.image_new= Image.open(r'picture/new.jpg')
        self.image_new=self.image_new.resize((20, 20))
        self.image_new = ImageTk.PhotoImage(self.image_new)
        self.image_open= Image.open(r'picture/open.jpg')
        self.image_open=self.image_open.resize((18, 18))
        self.image_open = ImageTk.PhotoImage(self.image_open)
        self.image_save= Image.open(r'picture/save.jpg')
        self.image_save=self.image_save.resize((18, 18))
        self.image_save = ImageTk.PhotoImage(self.image_save)
        self.image_save_as= Image.open(r'picture/save_as.jpg')
        self.image_save_as=self.image_save_as.resize((20, 20))
        self.image_save_as = ImageTk.PhotoImage(self.image_save_as)
        self.image_exit= Image.open(r'picture/exit.jpg')
        self.image_exit=self.image_exit.resize((20, 20))
        self.image_exit = ImageTk.PhotoImage(self.image_exit)
        self.image_file = Image.open(r'picture/file.gif')
        self.image_file = self.image_file.resize((15, 15))
        self.image_file = ImageTk.PhotoImage(self.image_file)
        self.image_close = Image.open(r'picture/close_s.jpg')
        self.image_close = self.image_close.resize((10, 10))
        self.image_close = ImageTk.PhotoImage(self.image_close)

        screenwidth = self.msd.winfo_screenwidth()
        screenheight = self.msd.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (800, 450, (screenwidth - 800) / 2-100, (screenheight - 450) / 2)
        self.msd.geometry(alignstr)
        self.msd.title('Compile')
        self.msd.wm_resizable(False, False)
        #主菜单
        menubar = Menu(self.msd,tearoff=False)
        fmenu = Menu(menubar, tearoff=0)
        fmenu.add_command(label='New', command=self.new, accelerator="(Ctrl+n)", compound="left",
                          image=self.image_new, hidemargin=True)
        fmenu.add_separator()
        fmenu.add_command(label='Open', command =self.open,accelerator="(Ctrl+o)",compound="left",image=self.image_open,hidemargin=True)
        fmenu.add_separator()
        fmenu.add_command(label='Save', command=self.save,accelerator="(Ctrl+s)",compound="left",image=self.image_save,hidemargin=True)
        fmenu.add_separator()
        fmenu.add_command(label='Save as', command=self.save_as,accelerator="(Ctrl+p)",compound="left",image=self.image_save_as,hidemargin=True)
        menubar.add_cascade(label="File", menu=fmenu)
        menubar.add_command(label="Run",command=self.run_compile)
        menubar.add_command(label='Exit', command=self.exit,accelerator="(Ctrl+f)")
        self.msd.config(menu=menubar)
        self.msd.bind('<Control-n>', self.new)
        self.msd.bind('<Control-o>',self.open)
        self.msd.bind('<Control-s>', self.save)
        self.msd.bind('<Control-p>', self.save_as)
        self.msd.bind('<Control-f>', self.exit)
        self.msd.bind('<Button-3>',self.des)
        self.msd.bind('<Control-r>',self.run_compile)
        self.msd.protocol('WM_DELETE_WINDOW', self.exit)


    def see_img(self,*args):
        os.system('"C:/Program Files/Google/Chrome/Application/chrome.exe" ' + self.locat+'img/DAG-without-act-var.png')

    def see_result(self,i,*args):
        try:
            self.ls.destroy()
        except:
            pass
        self.ls=Label(self.Ts, anchor="center", image=self.re_image[i])
        self.ls.place(x=0,y=100)

    def search_tag(self,text_widget, keyword, tag):
        pos = '1.0'
        while True:
            idx = text_widget.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            text_widget.tag_add(tag, idx, pos)
    def clear_koo(self):
        try:
            for x in self.koo:
                x.destroy()
            self.koo.clear()
        except:
            pass
    def see_word(self,*args):
        self.clear_koo()
        self.Ts.title(self.file[self.index] + '-错误分析')
        self.error_text=Text(self.Ts,width=90, height=15)
        content='词法错误分析-》【'+str(len(self.Lexical_errors))+'-errors】\n\n'
        for i in range(len(self.Lexical_errors)):
            x=self.Lexical_errors[i]
            content=content+'Error-'+str(i+1)+' : '+str(x[1])+'行\t'+str(x[2])+'列\t【'+x[3][:5]+"】\t附近 "+x[0]+':'+self.error_describe[x[0]][0]+'\n          修正提示=>'+self.error_describe[x[0]][1]+'\n'
        if (self.L_flag):
            content += '语法错误分析-》【' + str(len(self.Parsing_errors)) + '-errors】\n\n'
            for i in range(len(self.Parsing_errors)):
                x = self.Parsing_errors[i]
                content = content + 'Error-' + str(i + 1) + ' : ' + str(x[1][2]) + '行\t' + str(x[1][3]) + '列\t【' + x[1][
                    0] + "】\t附近 " + x[0] + ':' + self.error_describe[x[0]][0] + '\n          修正提示=>' + \
                          self.error_describe[x[0]][1] + '\n'
        if(self.P_flag):
            content += '语义错误分析-》【' + str(len(self.mean_result[2])) + '-errors】\n\n'
            for i in range(len(self.mean_result[2])):
                x = self.mean_result[2][i]
                content = content + 'Error-' + str(i + 1) + ' : ' + str(x[2]) + '行\t' + str(x[3]) + '列\t【' + x[1] + "】\t附近 " + x[0] + ':' + self.error_describe[x[0]][0] + '\n          修正提示=>' + \
                          self.error_describe[x[0]][1] + '\n'
        self.error_text.insert(1.0, content[0:-1])
        self.error_text.tag_config('tag', foreground='red')
        self.error_text.tag_config('tag1', foreground='blue')
        self.search_tag(self.error_text, 'Error', 'tag')
        self.search_tag(self.error_text, '修正提示', 'tag1')
        self.koo.append(self.error_text)
        self.error_text.pack(side="left", fill="both")
        self.vsb = tk.Scrollbar(self.Ts, orient="vertical", command=self.error_text.yview)
        self.koo.append(self.vsb)
        self.vsb.pack(side="right", fill="y")
        self.error_text.config(state=DISABLED)

    def see_alg(self,*args):
        self.clear_koo()
        self.Ts.title(self.file[self.index] + '-token文件')
        self.tree = ttk.Treeview(self.Ts, show="headings")  # #创建表格对象
        self.s = ttk.Style(self.tree)
        self.s.theme_use('alt')
        col = self.armmessage.columns.values.tolist()
        self.tree["columns"] = col
        for x in col:
            self.tree.column(x, width=148)  # #设置列
            self.tree.heading(x, text=x)  # #设置显示的表头名
        for i in range(len(self.armmessage)):
            self.tree.insert("", i, text=i, values=(self.armmessage.loc[i].values.tolist()))
        self.koo.append(self.tree)
        self.tree.pack(fill='both',expand=True)

    def see_grammar(self, *args):
        ur = '"C:/Program Files/Google/Chrome/Application/chrome.exe" ' + self.locat+'work/' + self.xname+'/语法树.html'
        os.system(ur)
    def see_symbol_table(self,*args):
        self.clear_koo()
        self.Ts.title(self.file[self.index] + '-符号表')
        self.symnol_text = Text(self.Ts, width=90, height=15)
        content='\n'
        for x in self.mean_result[1].keys():
            y=self.mean_result[1][x]
            if(len(y)!=0):
                content+='作用域:'+x+'\n  '
                for name in y.keys():
                    content +=name+'--'+str(y[name])+'\n  '
                content+='\n'
        self.symnol_text.insert(1.0, content[0:-1])
        self.symnol_text.tag_config('tag', foreground='red')
        self.symnol_text.tag_config('tag1', foreground='blue')
        self.search_tag(self.symnol_text, 'Error', 'tag')
        self.search_tag(self.symnol_text, '作用域', 'tag1')
        self.koo.append(self.symnol_text)
        self.symnol_text.pack(side="left", fill="both")
        self.vsb = tk.Scrollbar(self.Ts, orient="vertical", command=self.symnol_text.yview)
        self.koo.append(self.vsb)
        self.vsb.pack(side="right", fill="y")
        self.symnol_text.config(state=DISABLED)

    def see_midcode(self, *args):
        self.clear_koo()
        self.Ts.title(self.file[self.index] + '-中间代码')
        self.tree = ttk.Treeview(self.Ts, show="headings")  # #创建表格对象
        self.s = ttk.Style(self.tree)
        self.s.theme_use('alt')
        col = ['编号','算符','对象1','对象2','结果','作用域']
        self.tree["columns"] = col
        for x in col:
            self.tree.column(x, width=100,anchor = "center")  # #设置列
            self.tree.heading(x, text=x)  # #设置显示的表头名
        for i in range(len(self.mean_result[0])):
            self.tree.insert("", i, text=i, values=(['('+str(i)+')']+self.mean_result[0][i]),)
        self.koo.append(self.tree)
        self.tree.pack(fill='both', expand=True)
    def see_targrt_code(self,*args):
        self.clear_koo()
        self.Ts.title(self.file[self.index] + '-目标代码')
        self.symnol_text = Text(self.Ts, width=90, height=15)
        self.symnol_text.insert(1.0, self.Target_mid)
        self.koo.append(self.symnol_text)
        self.symnol_text.pack(side="left", fill="both")
        self.vsb = tk.Scrollbar(self.Ts, orient="vertical", command=self.symnol_text.yview)
        self.koo.append(self.vsb)
        self.vsb.pack(side="right", fill="y")
        self.symnol_text.config(state=DISABLED)
    def explation(self,*args):
        self.clear_koo()
        self.process_result=Explanation.explanation(self.mean_result[0],self.mean_result[1],'work/' + self.xname).run_main()
        self.Ts.title(self.file[self.index] + '程序解释')
        self.symnol_text = Text(self.Ts, width=90, height=15)
        self.symnol_text.insert(1.0, self.process_result)
        self.koo.append(self.symnol_text)
        self.symnol_text.config(state=DISABLED)
        self.symnol_text.pack(side="left", fill="both")
        self.vsb = tk.Scrollbar(self.Ts, orient="vertical", command=self.symnol_text.yview)
        self.vsb.pack(side="right", fill="y")
        self.koo.append(self.vsb)
        self.symnol_text.config(state=DISABLED)

    def New_window(self):
        try:
            self.Ts.destroy()
        except:
            pass
        self.Ts = Toplevel()
        screenwidth = self.msd.winfo_screenwidth()
        screenheight = self.msd.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (600, 450, (screenwidth - 600) / 2+300, (screenheight - 450) / 2)
        self.Ts.geometry(alignstr)
        self.Ts.wm_resizable(False, False)
        self.menubar = Menu(self.Ts, tearoff=False)
        self.menubar.add_command(label="错误分析",command=self.see_word)
        if(self.L_flag):
            self.menubar.add_command(label="token文件",command=self.see_alg)
            if(self.P_flag):
                self.menubar.add_command(label="语法树",command=self.see_grammar)
                if(self.M_flag):
                    self.menubar.add_command(label="中间代码",command=self.see_midcode)
                    self.menubar.add_command(label="符号表", command=self.see_symbol_table)
                    self.menubar.add_command(label="目标代码", command=self.see_targrt_code)
                    self.menubar.add_command(label="程序解释", command=self.explation)
        self.see_word()
        self.Ts.config(menu=self.menubar)
    def run_compile(self,*args):
        self.P_flag=False
        self.L_flag=False
        self.M_flag = False
        try:
            txtContent = self.ct.text.get(1.0, END)[:-1]
            self.xname=self.file[self.index]
            if (os.path.exists('work/' + self.xname) == False):
                os.mkdir('work/' + self.xname)
            self.Lex = Lexical_Analysis.Lexical_Analysis(txtContent, 'work/' + self.xname)
            self.Lex.main_Analysis()
            self.armmessage = self.Lex.get_ans()
            self.Lexical_errors = self.Lex.get_errors()
            if(len(self.Lexical_errors)==0):
                x=Parsing.Parsing(self.armmessage,'work/' + self.xname)
                self.Parsing_errors =x.return_errors()
                self.tree=x.return_parsing_tree()
                self.L_flag=True
                if(len(self.Parsing_errors)==0):
                    self.P_flag=True
                    mid=Mid_code.Midcode(self.armmessage,self.tree,'work/' + self.xname)
                    self.mean_result=mid.return_results()
                    if(len(self.mean_result[2])==0):
                        self.M_flag=True
                        self.Target_mid=Target_code.Targrt_code(self.mean_result[0],self.mean_result[0],'work/' + self.xname).target_code()
            try:
                self.Ts.destroy()
            except:
                pass
            self.New_window()

        except:
            pass
    def des(self,*args):
        try:
            self.lab.destroy()
            self.labelt.destroy()
            self.entry_usr.destroy()
        except:
            pass
    def new(self,*args):
        self.lab=tk.Label(self.msd,text='New file',bg='gray',fg='white',relief=GROOVE)
        self.lab.place(x=320, y=180, width=160,height=30)
        self.labelt = Label(self.msd, compound="left", image=self.image_file,relief=GROOVE)
        self.labelt.place(x=320, y=210, width=20, height=20)
        var_usr_name = tk.StringVar()
        self.entry_usr = tk.Entry(self.msd, textvariable=var_usr_name,relief=RIDGE,xscrollcommand=False)
        self.entry_usr.place(x=340, y=210, width=140,height=20)
        self.entry_usr.bind('<Return>', self.create_newfile)

    def create_newfile(self,*args):
        self.new_name='files/'+self.entry_usr.get()
        if(len(self.new_name)!=0):
            if(os.path.exists(self.new_name)==True):
                tk.messagebox.showerror(message='文件重名,请重新命名！')
            else:
                file = open(self.new_name, 'w', encoding='utf-8')
                file.flush()
                file.close()
                self.lab.destroy()
                self.labelt.destroy()
                self.entry_usr.destroy()
                self.filename=self.new_name
                content = self.openFile(fname=self.filename)
                self.contents.append(content)
                if (len(self.file) > 0):
                    txtContent = self.ct.text.get(1.0, END)
                    self.contents[self.index] = txtContent
                    self.index = len(self.file)
                    self.create_text(False)
                self.file.append(self.filename.split('/')[-1])
                self.file_path.append(self.filename)
                self.create_text(True, content)


    def create_text(self,c_c,*args):
        if(c_c==True):
            self.ct = Example(self.msd)
            self.ct.insert_text(args[0])
            self.crete_button()
            self.ct.place(x=0, y=18)
        else:
            for x in self.bts:
                x.destroy()
            self.bts.clear()
            self.ct.text.destroy()
            self.ct.linenumbers.destroy()
            self.ct.vsb.destroy()
            self.ct.destroy()
    def see_this(self,event,ix):#查看文件
        txtContent = self.ct.text.get(1.0, END)
        self.contents[self.index]=txtContent
        content=self.contents[ix][:-1]
        self.index=ix
        self.create_text(False)
        self.create_text(True,content)

    def close_this(self,event,ix):#关闭文件
        self.create_text(False)
        if(self.index==ix):
            self.file.pop(self.index)
            self.contents.pop(self.index)
            self.file_path.pop(self.index)
            if(self.index>0):
                self.index -=1
                content=self.contents[self.index]
                self.create_text(True, content)
            elif(self.index==0 and (len(self.file)-1>=0)):
                content=self.contents[self.index]
                self.create_text(True, content)
        elif(self.index>ix):
            content=self.contents[self.index]
            self.file.pop(ix)
            self.contents.pop(ix)
            self.file_path.pop(ix)
            self.index -= 1
            self.create_text(True, content)
        else:
            content=self.contents[self.index]
            self.file.pop(ix)
            self.contents.pop(ix)
            self.file_path.pop(ix)
            self.create_text(True, content)


    def save(self,*args):
        txtContent = self.ct.text.get(1.0, END)
        self.saveFile(content=txtContent)

    def save_as(self,*args):
        txtContent = self.ct.text.get(1.0, END)
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return
        f.write(txtContent,encoding='utf-8')
        f.close()

    def crete_button(self):
        begin=0
        for i in range(len(self.file)):
            name=self.file[i]
            if(i==self.index):
                label = Label(self.msd, text=name, compound="left", image=self.image_file,fg='blue')
            else:
                label=Label(self.msd,text=name,compound="left",image=self.image_file)
            la1 = Label(self.msd, compound="center", image=self.image_close)
            label.bind("<Button-1>", lambda event, ix=i: self.see_this(event,ix))
            label.place(x=begin,y=0,width=len(name)*8+10,height=18)
            la1.bind("<Button-1>", lambda event, ix=i: self.close_this(event, ix))
            la1.place(x=begin+len(name)*7+10, y=0, width=10, height=18)
            self.bts.append(label)
            self.bts.append(la1)
            begin=begin+len(name)*7+10+10

    def open(self,*args):
        self.filename = filedialog.askopenfilename(initialdir='files',title='Choose file')
        if len(self.filename)!=0:
            file_name=self.filename.split('/')[-1]
            if(file_name in self.file or self.filename in self.file_path):
                return
            content = self.openFile(fname=self.filename)
            self.contents.append(content)
            if(len(self.file)>0):
                txtContent = self.ct.text.get(1.0, END)
                self.contents[self.index] = txtContent
                self.index = len(self.file)
                self.create_text(False)
            self.file.append(self.filename.split('/')[-1])
            self.file_path.append(self.filename)
            self.create_text(True, content)

    def openFile(self, fname=None):
        if fname is None:
            return -1
        self.fname = fname
        file = open(fname, 'r',encoding='utf-8')
        content = file.read()
        file.close()
        return content

    def saveFile(self, content=None):
        if content is None:
            return -1
        self.fname=self.file_path[self.index]
        file = open(self.fname, 'w',encoding='utf-8')
        file.write(content)
        file.flush()
        file.close()
        return 0

    def exit(self,*args):
        if(len(self.file)>0):
            txtContent = self.ct.text.get(1.0, END)
            self.contents[self.index]=txtContent
            for x in range(len(self.file_path)):
                self.index=x
                txtContent=self.contents[x][:-1]
                self.saveFile(content=txtContent)
                print(self.fname+'保存完毕')
        sys.exit(0)

if __name__ == '__main__':
    Note()
