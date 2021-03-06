import tkinter as tk
from tkinter import ttk

class Style:
    font_heading = ('Cobert', 12)
    font_body = ('Cobert', 11)
    button_highlight='Gray60'
    bordercolor='gray60'

    bg = 'gray96'


class Primitives:    
    class Frame(tk.Frame):
        def __init__(self, parent, *args, **kwargs):

            kwargs = {"background":Style.bg} | kwargs

            super().__init__(parent, *args, **kwargs)

    class Label(tk.Label):
        def __init__(self, parent, text, *args, **kwargs):

            kwargs = {"background":'gray96',
                      "font":Style.font_heading, 
                      "width":0} | kwargs      # adds the defalt arg to kwargs if the arg doesnt exist
            
            super().__init__(parent, text=text, *args, **kwargs)

    class Button(tk.Button):
        def __init__(self, parent, text, command, *args, **kwargs):

            kwargs= {'border':0,
                     'background':"gray96",
                     'font':Style.font_heading,
                     'width':0,
                     'cursor':"hand2"} | kwargs

            super().__init__(parent, text=text, command=command, *args, **kwargs)
            
            self.hover = Style.button_highlight
            
            self.bind("<Enter>", self.mouse_over)
            self.bind("<Leave>", self.mouse_away)

        def mouse_over(self, e):
            self['background'] = self.hover
        
        def mouse_away(self, e):
            self['background'] = 'SystemButtonFace'
    
    class Entry(tk.Entry):
        def __init__(self, parent, *args, **kwargs):

            kwargs = {'width':40,
                      'highlightthickness':1,
                      'relief':tk.FLAT,
                      'highlightbackground':Style.bordercolor,
                      'font':Style.font_heading} | kwargs

            super().__init__(parent, *args, **kwargs)
            

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
                                highlightbackground=Style.bordercolor,
                                font=Style.font_body)

            self.scrollb = ttk.Scrollbar(self, command=self.text.yview)
            
            self.text['yscrollcommand'] = self.scrollb.set

            self.scrollb.pack(side=tk.RIGHT, fill=tk.Y)
            self.text.pack(side=tk.RIGHT, expand=True)
        
        def set_text(self, text):
            self.text.delete(1.0, "end")
            self.text.insert(1.0, text) 

        def get_text(self):
            return self.text.get(1.0, "end")