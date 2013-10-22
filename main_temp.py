from Tkinter import *
from subprocess import call
import os
from tkFileDialog import askopenfilename
import shlex
from PyPDF2 import PdfFileReader
import RecordClass
from tkFileDialog import asksaveasfilename


def new_set():
    filename=askopenfilename
    try:
        r_file=open(filename,"rb")
    except:
        print("Could not open the file")
    charge_open(filename)
    pass

def erase():
    objects=canvas.find_all()
    for item in objects:
        canvas.delete(item)

def updateCache(flag,inter,filename):
    """Cette fonction permet de charger dans la liste 'images'
    le nombre d'images dans l'interval 'inter' qui correspondent 
    aux pages du pdf"""
    global mywd,images
    if flag>0:
        images_name=[]
        images=[]
        for i in range(inter[0],inter[1]+1):
            newfilename=filename.split(".")
            newfilename=newfilename[0]
            newfilename=newfilename.rpartition("/")
            newfilename=newfilename[-1]
            images_name.append(mywd+newfilename+"_"+str(i)+".gif")
            images.append(0)
            instruction="convert -resize 400x400 {0}[{1}] {2}{3}_{4}.gif".format(filename,i,mywd,newfilename,i)
            args=shlex.split(instruction)
            call(args)
        for i in range(0,len(images)):
            images[i]=PhotoImage(file=images_name[i])
    else:
        pass

def save_page(num_page):
    """Sauvegarde de la page indiquee num_page dans la liste de donnees saving"""
    global saving
    list_objects=canvas.find_all()
    tags=[]
    saving[num_page]=[]
    if list_objects:
        tags.append(canvas.gettags(list_objects[0]))
        for item in list_objects:
            tag=canvas.gettags(item)
            if tag[0][0:4]=="line" or tag[0][0:4]=="rect":
                saving[num_page].append(RecordClass.RecordClass(tag[0][0:4],canvas.coords(item),tag,"",canvas.itemcget(tag[0],"width"),canvas.itemcget(tag[0],"fill")))
            if tag[0][0:4]=="text":
                saving[num_page].append(RecordClass.RecordClass(tag[0][0:4],canvas.coords(item),tag,canvas.itemcget(tag[0],"text"),canvas.itemcget(tag[0],"width"),canvas.itemcget(tag[0],"fill")))
    
def load_page(num_page):
    """Chargement de la page indiquee en num_page dans la liste saving"""
    global saving,cur_size
    for instance in saving[num_page]:
        coords_obj=instance.getCoords()
        tag_obj=instance.getTag()
        if instance.getType()=="line":
            canvas.create_line(coords_obj[0],coords_obj[1],coords_obj[2],coords_obj[3],width=instance.getSize(),tags=tag_obj,fill=instance.getColor())
        elif instance.getType()=="text":
            canvas.create_text(coords_obj[0],coords_obj[1],text=instance.getText(),tags=tag_obj,width=instance.getSize(),fill=instance.getColor())
        elif instance.getType()=="rect":
            canvas.create_rectangle(coords_obj[0],coords_obj[1],coords_obj[2],coords_obj[3],width=instance.getSize(),tags=tag_obj,fill=instance.getColor())
            
        
def part1_set(event):
    global text
    part1="""HELP : PROJET TABLEAU NUMERIQUE INTERACTIF
    GALLARDO KEVIN
    
    CE PROJET A POUR BUT D'IMPLANTER UNE INTERFACE DE 
    CONTROLE D'UN RETROPROJECTEUR PAR LE BIAIS D'UNE 
    WIIMOTE CONNECTEE EN USB A L'ORDINATEUR QUI EST RELIE
    AU RETROPROJECTEUR.
    IL S'ACCOMPAGNE AUSSI D'UN LOGICIEL DE GESTION DE 
    PRESENTATIONS PDF QUI PERMET L'AFFICHAGE D'UN DOCUMENT
    AU FORMAT PDF AINSI QUE SA MODIFICATION
    
    """
    text.delete(1.0,END)
    text.insert(1.0,part1)
    text.insert(END,"Aller a la partie 'Commandes'",'href')
    

def part2_set(event):
    global text
    part2="""HELP(2) : GUIDE DES COMMANDES
        POUR OUVRIR UN PDF : FICHIER->OUVRIR UN PDF
        ENSUITE LA MODIFICATION PEUT S'EFFECTUER A
        L'AIDE DES DIFFERENTS OUTILS DE DESSIN 
        PRESENTS DANS L'APPLI.
        LE DEROULEMENT DE LA PRESENTATION SE GERE 
        GRACE AU 'MININAVIGATOR' PRESENT DANS LA 
        BARRE DES OUTILS AINSI QUE DANS LA FENETRE 
        D'AFFICHAGE DE LA PRESENTATION.
    """
    text.delete(1.0,END)
    text.insert(1.0,part2)
    text.insert(END,"Aller a la partie 'Presentation'",'href2')
    text.tag_config('href2',foreground="blue",underline=True)
    text.tag_bind('href2',"<Button-1>",part1_set)


def help_set():
    help_window=Toplevel()
    part1="""PROJET TABLEAU NUMERIQUE INTERACTIF
    GALLARDO KEVIN
    
    CE PROJET A POUR BUT D'IMPLANTER UNE INTERFACE DE 
    CONTROLE D'UN RETROPROJECTEUR PAR LE BIAIS D'UNE 
    WIIMOTE CONNECTEE EN USB A L'ORDINATEUR QUI EST RELIE
    AU RETROPROJECTEUR.
    IL S'ACCOMPAGNE AUSSI D'UN LOGICIEL DE GESTION DE 
    PRESENTATIONS PDF QUI PERMET L'AFFICHAGE D'UN DOCUMENT
    AU FORMAT PDF AINSI QUE SA MODIFICATION
    
    """
    global text
    text=Text(help_window)
    text.pack()
    text.insert(END,part1)
    text.insert(END,"Aller a la partie 'Commandes'",'href')
    text.tag_config('href',foreground="blue",underline=True)
    text.tag_bind('href',"<Button-1>",part2_set)


def charge_open(filename):
    """Charge un pdf et charge les donnees dans saving"""
    global mywd,num_page,nb_pages,mini_navigator,saving
    erase()
    pwd=os.getcwd()
    mywd=pwd+"/data/images/"
    try:
        r_file=open(filename,"rb")
    except:
        print("Could not open the file")
    
    if not mini_navigator:
        canvas.configure(width=400,height=400)
        mini_navigator=Frame(playland)
        mini_navigator.pack()
        
        
        previous_can=Button(mini_navigator,image=previous_icon,command=previous_set)
        previous_can.grid(row=1,column=1,ipadx=10,padx=5,ipady=10,pady=5)
        
        
        next_can=Button(mini_navigator,image=next_icon,command=next_set)
        next_can.grid(row=1,column=3,ipadx=10,padx=5,ipady=10,pady=5)
        
        
        play_can=Button(mini_navigator,image=play_icon)
        play_can.grid(row=1,column=2,ipadx=10,padx=5,ipady=10,pady=5)
        
    
    pdf_file=PdfFileReader(r_file)
    try:
        nb_pages=pdf_file.getNumPages()
    except PdfReadWarning:
        pass
    
    if nb_pages > 4:
        updateCache(1,(0,3),filename) #Charge les 4 premieres images du pdf
    else:
        updateCache(1,(0,nb_pages-1),filename) #Charge les images du pdf en cache
    canvas.create_image(0,0,anchor=NW,image=images[0],tags="image")
    num_page=0  
    saving=[[]]*nb_pages
    
    
    line=r_file.readline()  
    while line:
        args=line.split("_")
        
        line=r_file.readline()
        
        




def open_set():
    global mywd,num_page,nb_pages,filename,mini_navigator,saving
    erase()
    pwd=os.getcwd()
    mywd=pwd+"/data/images/"
    filename=askopenfilename()
    try:
        r_file=open(filename,"rb")
    except:
        print("Could not open the file")
    
    if not mini_navigator:
        canvas.configure(width=400,height=400)
        mini_navigator=Frame(playland)
        mini_navigator.pack()
        
        
        previous_can=Button(mini_navigator,image=previous_icon,command=previous_set)
        previous_can.grid(row=1,column=1,ipadx=10,padx=5,ipady=10,pady=5)
        
        
        next_can=Button(mini_navigator,image=next_icon,command=next_set)
        next_can.grid(row=1,column=3,ipadx=10,padx=5,ipady=10,pady=5)
        
        
        play_can=Button(mini_navigator,image=play_icon)
        play_can.grid(row=1,column=2,ipadx=10,padx=5,ipady=10,pady=5)
        
    
    pdf_file=PdfFileReader(r_file)
    try:
        nb_pages=pdf_file.getNumPages()
    except PdfReadWarning:
        pass
    
    if nb_pages > 4:
        updateCache(1,(0,3),filename) #Charge les 4 premieres images du pdf
    else:
        updateCache(1,(0,nb_pages-1),filename) #Charge les images du pdf en cache
    canvas.create_image(0,0,anchor=NW,image=images[0],tags="image")
    num_page=0  
    saving=[[]]*nb_pages  
    
def save_set():
    global saving,filename
    filenamesave=asksaveasfilename()
    try:    
        w_file=open(filenamesave+".me","w")
    except Exception:
        print("Could not open the file")
    w_file.write(filename+"\n")
    for page in saving:#pour toutes les pages de la liste saving
        for instance in page:
            coords=instance.getCoords()
            w_file.write(str(saving.index(page))+"_")
            w_file.write(instance.getType()+"_")
            for coord in coords:
                w_file.write(str(coord)+"*")
            w_file.write("_")
            w_file.write(str(instance.getTag()[0]))
            w_file.write(instance.getText())
            w_file.write("_")
            w_file.write(instance.getSize())
            w_file.write("_")
            w_file.write(instance.getColor())
            w_file.write("\n")

def quit_set():
    pass

def size1_set():
    global cur_size
    cur_size=2

def size2_set():
    global cur_size
    cur_size=4

def size3_set():
    global cur_size
    cur_size=6

def size4_set():
    global cur_size
    cur_size=8
    
def size5_set():
    global cur_size
    cur_size=10
    
def color1_set():
    global cur_color
    cur_color="red"

def color2_set():
    global cur_color
    cur_color="blue"

def color3_set():
    global cur_color
    cur_color="yellow"

def color4_set():
    global cur_color
    cur_color="green"
    
def color5_set():
    global cur_color
    cur_color="black"

def layout(size,color):#parametre booleens
    """ajoute les cadres de taille de pinceaux
    et de couleur"""
    if sizes_frame:
        sizes_frame.pack_forget()
    if color_frame:
        color_frame.pack_forget()
    if more_frame:
        more_frame.pack_forget()
    if size:
        addsizebuttons(toolbox)
    if color:
        addcolorbuttons(toolbox)
        addmorebutton(toolbox)


def addsizebuttons(toolbox):
    global sizes_frame
    if not sizes_frame:
        sizes_frame=Frame(toolbox)
        global size_images
        size_images=[]
        id=os.getcwd()+"/data/images/icones/"
        for i in range(0,5):
            size_images.append(PhotoImage(file=id+"size"+str(i)+".gif"))
            eval("Button(sizes_frame,image=size_images[i],command=size{0}_set).grid(row=1,column={0},pady=10)".format(i+1))
        sizes_frame.pack()
    try:
        sizes_frame.pack_info()
    except TclError:
        sizes_frame.pack()

def addcolorbuttons(toolbox):
    global color_frame
    if not color_frame:
        color_frame=Frame(toolbox)
        global color_images
        color_images=[]
        id=os.getcwd()+"/data/images/icones/"
        color_images.append(PhotoImage(file=id+"red.gif"))
        color_images.append(PhotoImage(file=id+"blue.gif"))
        color_images.append(PhotoImage(file=id+"yellow.gif"))
        color_images.append(PhotoImage(file=id+"green.gif"))
        color_images.append(PhotoImage(file=id+"black.gif"))
        for i in range(0,5):
            eval("Button(color_frame,image=color_images[i],command=color{0}_set).grid(row=1,column={0},pady=10)".format(i+1))
    try:
        color_frame.pack_info()
    except TclError:
        color_frame.pack()

def addmorebutton(toolbox):
    global more_frame
    if not more_frame:
        more_frame=Frame(toolbox)
        Button(more_frame,text="More colors...",command=color3_set).grid(row=0,column=1)
    try:
        more_frame.pack_info()
    except TclError:
        more_frame.pack()
        
        
def pencil_set():
    tools_history.append("pen")
    layout(1,1)

def valid_text():
    global in_entry,text_number,cur_color
    canvas.create_text(30,30,text=in_entry.get(),tag="text{0}".format(text_number),fill=cur_color)
    text_number+=1

def text_set():
    global in_entry
    tools_history.append("text")
    """if color_frame:
        color_frame.pack_forget()
    addcolorbuttons(toolbox)"""
    layout(0,1)
    in_win=Toplevel(toolbox)
    Label(in_win,text="Veuillez saisir le texte").pack()
    in_entry=Entry(in_win,width=10)
    in_entry.pack()
    Button(in_win,text="Valider",command=valid_text).pack()
    Button(in_win,text="Annuler",command=in_win.destroy).pack()
    
    
    
def move_set():
    tools_history.append("move")
    #if sizes_frame:
        #sizes_frame.pack_forget()
    #if color_frame:
        #color_frame.pack_forget()
    layout(0,0)
    
def select_set():
    tools_history.append("sel")
    """if sizes_frame:
        sizes_frame.pack_forget()
    if color_frame:
        color_frame.pack_forget()"""
    layout(0,0)


def gum_set():
    tools_history.append("gum")
    #addsizebuttons(toolbox)
    layout(1,0)

def paintingpot_set():
    tools_history.append("pot")
    """if sizes_frame:
        sizes_frame.pack_forget()"""
    layout(1,0)
        
def rect_set():
    tools_history.append("rect")
    """if sizes_frame:
        sizes_frame.pack_forget()
    addcolorbuttons(toolbox)"""
    layout(0,1)

def line_set():
    tools_history.append("line")
    """if sizes_frame:
        sizes_frame.pack_forget()
    addcolorbuttons(toolbox)"""
    layout(0,1)

def circle_set():
    tools_history.append("cir")
    """if sizes_frame:
        sizes_frame.pack_forget()
    addcolorbuttons(toolbox)"""
    layout(0,1)

def next_set():
    global num_page,images,nb_pages,filename
    
    if num_page<nb_pages-1:
        save_page(num_page)
        num_page=num_page+1
    remaining=nb_pages-num_page
    if remaining>4:
        if num_page%4==0:
            updateCache(1,(num_page,num_page+3),filename)
        erase()
        canvas.create_image(0,0,anchor=NW,image=images[(num_page)%4],tags="image")
        load_page(num_page)
    elif remaining>0:
        if num_page%4==0:
            updateCache(1,(num_page,num_page+remaining-1),filename)
        erase()
        canvas.create_image(0,0,anchor=NW,image=images[num_page%4],tags="image")
        load_page(num_page)
    else:
        pass
  

def previous_set():
    global num_page,images,nb_pages
    if num_page>0:
        save_page(num_page)
        num_page=num_page-1
    if num_page%4==3:
        updateCache(1,(num_page-3,num_page),filename)
    erase()
    canvas.create_image(0,0,anchor=NW,image=images[num_page%4],tags="image")
    load_page(num_page)


def interface(toolbox):
    tools=Frame(toolbox, width=120)
    tools.pack()
    id=os.getcwd()+"/data/images/icones/"# Images Directory
    
    
    global pencil_icon
    pencil_icon=PhotoImage(file=id+"crayon.gif")
    pencil=Button(tools,image=pencil_icon,command=pencil_set)
    pencil.grid(row=1,column=1,ipadx=5,ipady=5,padx=5)
    
    
    global text_icon
    text_icon=PhotoImage(file=id+"text.gif")
    text=Button(tools,image=text_icon,command=text_set)
    text.grid(row=1,column=2,ipadx=5,ipady=5,padx=5)
    
    
    global select_icon
    select_icon=PhotoImage(file=id+"select.gif")
    select=Button(tools,image=select_icon,command=select_set)
    select.grid(row=1,column=3,ipadx=5,ipady=5,padx=5)
    
    
    global gum_icon
    gum_icon=PhotoImage(file=id+"gum.gif")
    gum=Button(tools,image=gum_icon,command=gum_set)
    gum.grid(row=2,column=1,ipadx=5,ipady=5)
    
    
    global paintingpot_icon
    paintingpot_icon=PhotoImage(file=id+"paintingpot.gif")
    paintingpot=Button(tools,image=paintingpot_icon,command=paintingpot_set)
    paintingpot.grid(row=2,column=2,ipadx=5,ipady=5)
    
    
    global move_icon
    move_icon=PhotoImage(file=id+"move.gif")
    move=Button(tools,image=move_icon,command=move_set)
    move.grid(row=2,column=3,ipadx=5,ipady=5)
    
    
    global rect_icon
    rect_icon=PhotoImage(file=id+"rect.gif")
    rect=Button(tools,image=rect_icon,command=rect_set)
    rect.grid(row=3,column=1,ipadx=5,ipady=5)
    
    global line_icon
    line_icon=PhotoImage(file=id+"line.gif")
    line=Button(tools,image=line_icon,command=line_set)
    line.grid(row=3,column=2,ipadx=5,ipady=5)
    
    
    global circle_icon
    circle_icon=PhotoImage(file=id+"circle.gif")
    circle=Button(tools,image=circle_icon,command=circle_set)
    circle.grid(row=3,column=3,ipadx=5,ipady=5)
    
    
    navigator=Frame(toolbox)
    navigator.pack()
    
    
    Label(navigator,text="-").grid(row=1,column=2,pady=10)
    
    
    global previous_icon
    previous_icon=PhotoImage(file=id+"previous.gif")
    previous=Button(navigator,image=previous_icon,command=previous_set)
    previous.grid(row=2,column=1,ipadx=5,padx=5,ipady=5,pady=5)
    
    
    global next_icon
    next_icon=PhotoImage(file=id+"next.gif")
    next=Button(navigator,image=next_icon,command=next_set)
    next.grid(row=2,column=3,ipadx=5,padx=5,ipady=5,pady=5)
    
    
    global play_icon
    play_icon=PhotoImage(file=id+"play.gif")
    play=Button(navigator,image=play_icon)
    play.grid(row=2,column=2,ipadx=5,padx=5,ipady=5,pady=5)
    Label(navigator,text="-").grid(row=3,column=2,pady=10)

    global cur_size
    cur_size=4
    global sizes_frame
    sizes_frame=""
    global cur_color
    cur_color="black"
    global color_frame
    color_frame=""
    global more_frame
    more_frame=""


def mouseDown(event):
    global first_x, first_y,tools_history
    first_x=event.x
    first_y=event.y
    if len(tools_history)>0:    
        if tools_history[-1]!="move":
            objs=canvas.find_withtag("selected")
            for item in objs:
                #canvas.itemconfigure(item,fill="black")
                canvas.dtag(item,"selected")
    #mb_file_menu.entryconfig(2,state="normal")

def mouseMove(event):
    global first_x,first_y,tools_history,end_x,end_y,line_number,cur_size,rect_number,cur_color
    if len(tools_history)>0:
        if tools_history[-1]=="pen":
            #global cur_size
            canvas.create_line(first_x,first_y,event.x,event.y,width=cur_size,tags="line{0}".format(line_number),fill=cur_color)
            first_x=event.x
            first_y=event.y
        if tools_history[-1]=="sel":
            rect=canvas.find_withtag("selection")
            if rect:
                canvas.delete(rect)
            end_x=event.x
            end_y=event.y
            canvas.create_rectangle(first_x,first_y,end_x,end_y,tags="selection")
        if tools_history[-1]=="move":
            if tools_history[-2]=="sel":
                depx=event.x-first_x
                depy=event.y-first_y
                canvas.move("selected",depx,depy)
                first_x=event.x
                first_y=event.y
        if tools_history[-1]=="gum":
            current_object=canvas.find_overlapping(event.x-cur_size,event.y-cur_size,event.x+cur_size,event.y+cur_size)
            if (len(current_object) > 1):
                for item in current_object:
                    if (canvas.gettags(item)[0]!="image"):
                        canvas.delete(item)
        if tools_history[-1]=="rect":
            rect=canvas.find_withtag("rectangle{0}".format(rect_number))
            if rect:
                canvas.delete(rect)
            end_x=event.x
            end_y=event.y
            canvas.create_rectangle(first_x,first_y,end_x,end_y,tags="rectangle{0}".format(rect_number),fill=cur_color)

def mouseUp(event):
    global first_x,first_y,end_x,end_y,line_number,tags,rect_number
    if len(tools_history)>0:
        if tools_history[-1]=="sel":
            rect=canvas.find_withtag("selection")
            if rect:
                canvas.delete(rect)
            objects_selected=canvas.find_enclosed(first_x, first_y, end_x, end_y)
            tags=[]
            if objects_selected:
                tags.append(canvas.gettags(objects_selected[0]))
                for item in objects_selected:
                    tag=canvas.gettags(item)
                    if tag!=tags[-1]:
                        tags.append(tag)    
                for tag in tags:
                    #canvas.itemconfigure(tag,fill="blue")
                    canvas.addtag_withtag("selected",tag)
        if tools_history[-1]=="pen":
            line_number+=1
        if tools_history[-1]=="rect":
            rect_number+=1
        pass


toolbox=Tk()
playland=Toplevel(toolbox)
global tools_history,line_number,text_number,mini_navigator
tools_history=[]
line_number=0
text_number=0
rect_number=0
mini_navigator=""
menu_bar=Frame(toolbox)
menu_bar.pack()


mb_file=Menubutton(menu_bar,text="File")
mb_edit=Menubutton(menu_bar,text="Edit")
mb_help=Menubutton(menu_bar,text="Help")


mb_file_menu=Menu(mb_file,tearoff=True)
mb_file_menu.add_command(label="Ouvrir",command=new_set)
mb_file_menu.add_command(label="Charger un pdf",command=open_set)
mb_file_menu.add_command(label="Sauver",command=save_set)
mb_file_menu.add_command(label="Quitter",command=quit_set)



mb_edit_menu=Menu(mb_edit,tearoff=True)


mb_help_menu=Menu(mb_help,tearoff=True)
mb_help_menu.add_command(label="Help...",command=help_set)

mb_file.configure(menu=mb_file_menu)
mb_edit.configure(menu=mb_edit_menu)
mb_help.configure(menu=mb_help_menu)


mb_file.pack(side=LEFT)
mb_edit.pack(side=LEFT)
mb_help.pack(side=LEFT)


interface(toolbox)


canvas=Canvas(playland,background="lightgray")
canvas.pack()
canvas.bind("<ButtonPress-1>",mouseDown)
canvas.bind("<ButtonRelease-1>",mouseUp)
canvas.bind("<B1-Motion>",mouseMove)


toolbox.mainloop()