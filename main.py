from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from sqlite3 import *
import os

def KeyPress(k):
    if k.keysym=='Escape':
        exit()
    elif k.keysym=="F1":
        nemod()
    elif k.keysym=='F2':
        add()
    elif k.keysym=='F3':
        delete()
    elif k.keysym=='F4':
        chng()

def exit():
    if messagebox.askyesno("Выход","Хотите выйти?"):
        cur.connection.close()
        for i in range(0,l.size(),1):
            os.remove(str(i)+'.png')
        root.destroy()

def imgtoblob(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def blobtoimg(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data[0])

allimg = str()
alldata = str()
def reloaddata():
    global allimg
    global alldata
    allimg = cur.execute("SELECT image FROM Explorers").fetchall()
    alldata = cur.execute("SELECT data FROM Explorers").fetchall()
    alldata = [i[0] for i in alldata]
    n = 0
    for i in allimg:
        blobtoimg(allimg[n],str(n)+'.png')
        n+=1
    global name
    global imgblob
    global imgf
    global data
    name = ''
    imgblob = ''
    data = ''
    imgf = ''



def AboutProg():
    messagebox.showinfo(message="База данных 'Знаменитые полярники России' \n(c) Pervushin E.K., Russia, 2023")

def nemod():
    def click():
        top.destroy()
    top = Toplevel(root)
    top.title("О программе")
    top.geometry("450x210")
    top.title("Справка")
    canvas1 = Canvas(top)
    canvas1.place(x=15,y=10,width=420,height=190)
    canvas1.create_text(10,5, text="База данных 'Знаменитые полярники России'\nПозволят: добавлять / изменять / удалять информацию.\nКлавиши программы:\nF1 - вызов справки по программе,\nF2 - добавить в базу данных,\nF3 - удалить из базы данных,\nF4 - изменить запись в базе данных,\nF10 - меню программы", font=26, anchor='nw')
    canvas1.create_window(210, 170, anchor="center", window=Button(canvas1, text="Закрыть", command=click))
    top.resizable(width=False, height=False)


def add():
    def click(*args):
        text = namet.get('1.0','end')
        if text == 'Введите название новой статьи...\n':
            namet.delete('1.0','end')
    def leave(*args):
        text = namet.get('1.0','end')
        if text == '\n':
            namet.insert('1.0',"Введите название новой статьи...")
    def click1(*args):
        text = datat.get('1.0','end')
        if text == 'Введите текст новой статьи...\n':
            datat.delete('1.0','end')
    def leave1(*args):
        text = datat.get('1.0','end')
        if text == '\n':
            datat.insert('1.0',"Введите текст новой статьи...")


    def imgopen():
        filename = filedialog.askopenfilename()
        imgn['state'] = 'normal'
        imgn.insert('1.0', filename)
        global imgf
        imgf = filename
        imgn['state'] = 'disabled'
        newentry.lift()


    def send():
        global name
        name = namet.get('1.0','end')
        global imgblob
        imgblob = imgtoblob(imgf)
        global data
        data = datat.get('1.0','end')
        record()
        newentry.destroy()
        
        
        
    newentry = Toplevel(root, bg="white")
    newentry.title("добавить")
    newentry.geometry("500x350")
    ###name
    namel = Text(newentry, width=15,height=1,border=False)
    namel.insert('1.0', "Фамилия имя:")
    namel['state'] = 'disabled'
    namel.grid(row=0,sticky='NW')
    namet = Text(newentry, height=1,borderwidth=2)
    namet.insert('1.0',"Введите название новой статьи...")
    namet.bind("<Button-1>",click)
    namet.bind("<Leave>",leave)
    namet.grid(row=1,sticky='E W')
    ###img
    imgl = Text(newentry, width=5, height=1,border=False)
    imgl.insert('1.0', "Файл:")
    imgl['state'] = 'disabled'
    imgl.grid(row=2,sticky='NW')
    imgb = Button(newentry,text='File', command=imgopen)
    imgb.grid(row=3,sticky='NW')
    imgn = Text(newentry,height=1,border=False)
    imgn.insert('1.0', "")
    imgn['state'] = 'disabled'
    imgn.grid(row=4,sticky='NW NE')
    ###data
    datal = Text(newentry, width=13,height=1,border=False)
    datal.insert('1.0', "Текст статьи:")
    datal['state'] = 'disabled'
    datal.grid(row=5,sticky='NW')
    datat = Text(newentry, height=1,borderwidth=2)
    datat.insert('1.0',"Введите текст новой статьи...")
    datat.bind("<Button-1>",click1)
    datat.bind("<Leave>",leave1)
    datat.grid(row=6,sticky='NE NW SE SW')
    ###button
    done = Button(newentry,text='Создать',command=send)
    done.grid(row=7,sticky='NW')
    newentry.columnconfigure(0,weight=1)
    newentry.rowconfigure(6,weight=1)
    
def record():
    record = "INSERT INTO Explorers(id,name,image,data) VALUES(?,?,?,?)"
    cur.execute(record,(l.size(),str(name)[0:-1],imgblob,str(data)[0:-1]))
    conn.commit()
    l.insert(l.size(),name)
    reloaddata()


def delete():
    delete = "DELETE FROM Explorers WHERE id=?"
    cur.execute(delete,(id,))
    conn.commit()
    if id < l.size():
        updateid = "UPDATE Explorers SET id=? WHERE id=?"
        for i in range(id,l.size()-id,1):
                cur.execute(updateid,(i,i+1))
    conn.commit()
    l.delete(id)
    reloaddata()

def chng():
    def imgopen():
        filename = filedialog.askopenfilename()
        imgn['state'] = 'normal'
        imgn.insert('1.0', filename)
        global imgf
        imgf = filename
        imgn['state'] = 'disabled'
        newentry.lift()


    def send():
        global name
        global imgblob
        global alldata
        if l.get(id) != namet.get('1.0','end'):
            name = namet.get('1.0','end')
        else: name = alldata[id]
        l.delete(id)
        l.insert(id,name)
        if imgf != '':
            imgblob = imgtoblob(imgf)
        else: imgblob = imgtoblob(str(id)+'.png')
        global data
        data = datat.get('1.0','end')
        update = "UPDATE Explorers SET name=?, image=?, data=? WHERE id=?"
        cur.execute(update,(str(name)[0:-1],imgblob,str(data)[0:-1],id))
        conn.commit()
        reloaddata()
        newentry.destroy()
        
        
        
    newentry = Toplevel(root, bg="white")
    newentry.title("Изменить")
    newentry.geometry("400x300")
    ###name
    namel = Text(newentry, width=9,height=1,border=False)
    namel.insert('1.0', "Название:")
    namel['state'] = 'disabled'
    namel.grid(row=0,sticky='NW')
    namet = Text(newentry, height=1,borderwidth=2)
    namet.insert('1.0',l.get(id))
    namet.grid(row=1,sticky='E W')
    ###img
    imgl = Text(newentry, width=5, height=1,border=False)
    imgl.insert('1.0', "Файл:")
    imgl['state'] = 'disabled'
    imgl.grid(row=2,sticky='NW')
    imgb = Button(newentry,text='File', command=imgopen)
    imgb.grid(row=3,sticky='NW')
    imgn = Text(newentry,height=1,border=False)
    imgn.insert('1.0', "")
    imgn['state'] = 'disabled'
    imgn.grid(row=4,sticky='NW NE')
    ###data
    datal = Text(newentry, width=13,height=1,border=False)
    datal.insert('1.0', "Текст статьи:")
    datal['state'] = 'disabled'
    datal.grid(row=5,sticky='NW')
    datat = Text(newentry, height=1,borderwidth=2)
    datat.insert('1.0',alldata[id])
    datat.grid(row=6,sticky='NE NW SE SW')
    ###button
    done = Button(newentry,text='Создать',command=send)
    done.grid(row=7,sticky='NW')
    newentry.columnconfigure(0,weight=1)
    newentry.rowconfigure(6,weight=1)



id = 0
def selected(event):
    global id
    idnew = l.curselection()
    idnew = idnew[0]
    if id != idnew:
        id = idnew
        img1 = ImageTk.PhotoImage(Image.open(str(id)+'.png'))
        image.configure(image=img1)
        image.image = img1
        ldata['state'] = 'normal'
        ldata.delete('1.0','end')
        ldata.insert('1.0', alldata[id])
        ldata['state'] = 'disabled'




root = Tk()


mainmenu = Menu(root) 
root.config(menu=mainmenu) 
#file menu
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Добавить F2", command=add)
filemenu.add_command(label="Удалить F3", command=delete)
filemenu.add_command(label="Изменить F4", command=chng)
filemenu.add_separator()
filemenu.add_command(label="Выход Esc", command=exit)
#help menu
helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Содержание", command=nemod)
helpmenu.add_separator()
helpmenu.add_command(label="О программе", command=AboutProg)

mainmenu.add_cascade(label="Фонд", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)


#statusbar
statusbar = Label(root,relief=SUNKEN,bg="#113F7C",fg="white",anchor="w",text="F1-справка F2-добавить F3-удалить F4-изменить F10-меню",border=False)
statusbar.grid(column=0,row=1,columnspan=3,sticky="S SW SE")



conn = connect("fond.db")
cur = conn.cursor()

reloaddata()
entrys = cur.execute("SELECT name FROM Explorers").fetchall()
entrys = [i[0] for i in entrys]
choicesvar = StringVar(value=entrys)
l = Listbox(root,listvariable=choicesvar, border=2, width=16)
l.grid(column=0,row=0,sticky="S N W E")

root.geometry("800x600")


###img
img = ImageTk.PhotoImage(Image.open(str(id)+'.png'))
image = Label(root,image=img,anchor='center')
image.grid(column=1,row=0)
###text
ldata = Text(root,bg="white", width=45, wrap=WORD)
ldata.insert('1.0', alldata[id])
ldata['state'] = 'disabled'
ldata.grid(column=2,row=0,sticky='N S E')



root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.columnconfigure(2,weight=1)
root.rowconfigure(0,weight=1)


root.title("Известные полярники России")
l.bind("<<ListboxSelect>>",selected)
root.bind("<KeyPress>",KeyPress)



root.protocol("WM_DELETE_WINDOW", exit)
root.state('zoomed')
root.mainloop()