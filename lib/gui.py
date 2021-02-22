import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

from lib.senario import Senario


class Primitives:
    font = ('Helvetica', 12)
    button_highlight='Gray60'
    bordercolor='gray60'
    
    class Frame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent, 
                             background='gray96')

    class Label(tk.Label):
        def __init__(self, parent, text, width=0):
            super().__init__(parent, 
                             text=text,
                             background='gray96',
                             font=Primitives.font,
                             width=width)

    class Button(tk.Button):
        def __init__(self, parent, text, command, width=0):
            super().__init__(parent, 
                             text=text, 
                             command=command,
                             border=0,
                             background="gray96",
                             font=Primitives.font,
                             width=width,
                             cursor="hand2")
            
            self.hover = Primitives.button_highlight
            
            self.bind("<Enter>", self.mouse_over)
            self.bind("<Leave>", self.mouse_away)

        def mouse_over(self, e):
            self['background'] = self.hover
        
        def mouse_away(self, e):
            self['background'] = 'SystemButtonFace'
    
    class Entry(tk.Entry):
        def __init__(self, parent, width=40):
            super().__init__(parent, 
                             width=width,
                             highlightthickness=1,
                             relief=tk.FLAT,
                             highlightbackground=Primitives.bordercolor,
                             font=Primitives.font)
            

    class Buttonlis(Frame):
        def __init__(self, parent, text_lis=[], command_lis=[], pack_side=tk.TOP):
            super().__init__(parent)
            self.pack_side = pack_side
            self.button_list = []
        
        def create(self, text_lis, command_lis):
            self.delete()
            for i in range(len(text_lis)):
                button = Primitives.Button(self, text_lis[i], command_lis[i])
                self.button_list.append(button)
                button.pack(side=self.pack_side, fill=tk.X, expand=True)

        def delete(self):
            for button in self.button_list:
                button.pack_forget()
            self.button_list = []   

    class Scrolltext(Frame):
        "large text space with scroll bar on right"
        def __init__(self, parent):
            super().__init__(parent)
            self.text = tk.Text(self, 
                                wrap=tk.WORD,
                                highlightthickness=1,
                                relief=tk.FLAT,
                                highlightbackground=Primitives.bordercolor)

            self.scrollb = ttk.Scrollbar(self, command=self.text.yview)
            
            self.text['yscrollcommand'] = self.scrollb.set

            self.scrollb.pack(side=tk.RIGHT, fill=tk.Y)
            self.text.pack(side=tk.RIGHT, expand=True)
        
        def set_text(self, text):
            self.text.delete(1.0, "end")
            self.text.insert(1.0, text) 

        def get_text(self):
            return self.text.get(1.0, "end")        

class Mine:
    class Text_peram_frame(Primitives.Frame):
        "label on left small entry on right"
        def __init__(self, parent, name, width=40):
            super().__init__(parent)

            self.text = Primitives.Entry(self, width=width)
            self.text.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            Primitives.Label(self, name).pack(side=tk.RIGHT, expand=True)

        def set_text(self, text):
            self.text.delete(0, "end")
            self.text.insert(0, text)

        def get_text(self):
            return self.text.get()

    class Text_button_frame(Primitives.Frame):
        "button on left small entry on right"
        def __init__(self, parent, button_text, command, width=30):
            super().__init__(parent)

            self.text = Primitives.Entry(self, width=width)
            self.text.pack(side=tk.RIGHT, fill=tk.X, expand=True)

            self.button = Primitives.Button(self, button_text, command, width=5)
            self.button.pack(side=tk.RIGHT, expand=True)

        def set_command(self, var):
            self.button.configure(command=var)

        def set_text(self, text):
            self.text.delete(0, "end")
            self.text.insert(0, text)

        def get_text(self):
            return self.text.get()

    class Choice_frame(Primitives.Frame):
        "entry and navigation of the choices"
        def __init__(self, parent, mainapp):
            super().__init__(parent)
            self.mainapp = mainapp
            self.widgit_lis = []
            names = ["A.", "B.", "C.", "D.", "E.", "F."]
            for i in range(len(names)):
                entry = Mine.Text_button_frame(self, names[i], lambda a=i: self.open_senario(a), width=70)
                self.widgit_lis.append(entry)
                entry.pack(fill=tk.X, expand=True)

        def open_senario(self, choice_index):
            self.save()
            self.mainapp.go_to_senario(self.mainapp.senario["choices"][choice_index][1])

        def set_choice_lis(self):
            choices = self.mainapp.senario.get_from_tag("choices")
            for i in range(len(self.widgit_lis)):
                if i < len(choices):
                    self.widgit_lis[i].set_text(choices[i][0])
                else:
                    #clear extra text
                    self.widgit_lis[i].set_text("")

        def save(self):
            for i in range(len(self.widgit_lis)):
                text = self.widgit_lis[i].get_text()
                text = text.strip()
                choices = self.mainapp.senario["choices"]
                if i < len(choices):
                    choices[i][0] = text
                elif text != '':
                    choices.append([text, self.mainapp.senario.new_senario()])



    class Editframe(Primitives.Frame):
        def __init__(self, parent, mainapp):
            super().__init__(parent)
            self.mainapp = mainapp

            self.name = Mine.Text_peram_frame(self, "Name")
            self.text = Primitives.Scrolltext(self)
            self.choice = Mine.Choice_frame(self, self.mainapp)
            

            self.name.pack(expand=True)
            self.text.pack(anchor="e", expand=True)
            self.choice.pack(expand=True)

        def load_senario(self, senario):
            if senario.tag_exists("name"):
                self.name.set_text(senario["name"])
            self.text.set_text(senario["text"])
            if senario.tag_exists("choices"):
                self.choice.set_choice_lis()

        def save(self):
            self.choice.save()
            self.mainapp.senario["text"] = self.text.get_text().strip()
            self.mainapp.senario["name"] = self.name.get_text().strip()

    class Infoframe(Primitives.Frame):
        def __init__(self, parent, mainapp):
            super().__init__(parent)
            self.mainapp = mainapp
            self.label = Primitives.Label(self, "Previous Senarios", width=20)
            self.buttons = Primitives.Buttonlis(self)

            self.label.pack(side=tk.TOP)
            self.buttons.pack(fill=tk.X, expand=True)

        def load(self):
            previous_senarios = self.mainapp.senario.find_prev_senarios_id()

            info_text = []
            commands = []
            for i in range(len(previous_senarios)):
                id_str = previous_senarios[i]
                
                info_str = self.mainapp.senario.get_info_str(id_str, 30)
                info_text.append(info_str)

                commands.append(lambda a=id_str: self.mainapp.go_to_senario(a))

            self.buttons.create(info_text, commands)



class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.title("Dialogue")
        self.root.configure(background='gray98')

        self.change_made = False

        self.edit_frame = None
        self.info_frame = None

        self.bind_keys(("<Control-s>", lambda event: self.save_file()),
                        ("<Control-Shift-S>", lambda event: self.save_as()))

        self.senario = Senario()

        self.create_menus()
        self.create_frame()

        self.load_senario()

    def create_frame(self):
        self.edit_frame = Mine.Editframe(self.root, self)
        self.info_frame = Mine.Infoframe(self.root, self)

        self.edit_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        self.info_frame.pack(side=tk.RIGHT, anchor="nw", expand=True)

    def go_to_senario(self, id_str):
        if self.senario.id_exists(id_str):
            self.save_senario()
            self.senario.goto_id(id_str)
            self.load_senario()
        else:
            print("senario does not exist")

    def go_to_new_senario(self, choice_name):
        "choice_name is used to add to the choice list"
        new_id = self.senario.new_senario()
        self.senario['choices'].append([choice_name, new_id])

    def load_senario(self):
        self.edit_frame.load_senario(self.senario)
        self.info_frame.load()
    
    def save_senario(self):
        self.edit_frame.save()

    def new_senario(self):
        self.senario.new_game()
        self.load_senario()
        self.root.title("Dialogue")

    def open_senario(self):
        data = [('json (*.json)', '*.json'),
                ('All tyes(*.*)', '*.*')]
        file = filedialog.askopenfile(filetypes = data, defaultextension = data)
        if file != None:
            self.senario.load_file(file.name)
            self.load_senario()
            self.root.title(f"Dialogue - {file.name}")

    def save_file(self):
        if self.senario.file_path == None:
            self.save_as()
        else:
            self.save_senario()
            self.edit_frame.save()
            self.senario.save_file()

    def save_as(self):
        data = [('json (*.json)', '*.json'), 
                ('All tyes(*.*)', '*.*')]
        file = filedialog.asksaveasfile(filetypes = data, defaultextension = data)
        if file != None:
            self.save_senario()
            self.senario.save_as_file(file.name)
            self.root.title(f"Dialogue - {file.name}")

    def exit(self):
        if self.senario.file_path == None:
            if messagebox.askokcancel("Unsaved Work", "You have unsaved work.\nAre you sure you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

    def bind_keys(self, *args):
        for arg, command in args:
            upper = arg[:-2] + arg[-2].upper() + arg[-1]
            lower = arg[:-2] + arg[-2].lower() + arg[-1]
            self.root.bind(upper, command)
            self.root.bind(lower, command)


    def create_menus(self):
        menubar = tk.Menu(self.root)

        fileMenu = MainApp.Menubars.File_menu(menubar, self)
        menubar.add_cascade(label="File", menu=fileMenu)

        self.root.config(menu=menubar)

    def mainloop(self):
        self.root.mainloop()

    class Menubars:
        class File_menu(tk.Menu):
            def __init__(self, menubar, mainapp):
                super().__init__(menubar, tearoff=0)
                self.add_command(label="New File", command=mainapp.new_senario)
                self.add_command(label="Open File", command=mainapp.open_senario)
                self.add_separator()
                self.add_command(label="Save", command=mainapp.save_file)
                self.add_command(label="Save As", command=mainapp.save_as)
                self.add_separator()
                self.add_command(label="Exit", command=mainapp.exit)