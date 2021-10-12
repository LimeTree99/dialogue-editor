import tkinter as tk
from tkinter import ttk

class Style:
    font_heading = ('Arial', 13)
    font_body = ('Arial', 13)
    button_highlight='Gray60'
    bordercolor='gray60'

    background = 'gray85'
    button_background = 'gray75'
    textbox_color = 'gray98'
    line_space = 6


class Primitives:    
    class Frame(tk.Frame):
        def __init__(self, parent, *args, **kwargs):

            kwargs = {"background":Style.background} | kwargs

            super().__init__(parent, *args, **kwargs)

    class Label(tk.Label):
        def __init__(self, parent, text, *args, **kwargs):

            kwargs = {"background":Style.background,
                      "font":Style.font_heading, 
                      "width":0} | kwargs      # adds the defalt arg to kwargs if the arg doesnt exist
            
            super().__init__(parent, text=text, *args, **kwargs)

    class Button(tk.Button):
        def __init__(self, parent, text, command, *args, **kwargs):

            kwargs= {'border':1,
                     'highlightcolor':'red',
                     'background':Style.button_background,
                     'font':Style.font_heading,
                     'width':0,
                     'cursor':"hand2"} | kwargs

            super().__init__(parent, text=text, command=command, *args, **kwargs)
            
            self.hover_color = Style.button_highlight
            self.background = kwargs['background']
            
            self.bind("<Enter>", self.mouse_over)
            self.bind("<Leave>", self.mouse_away)

        def mouse_over(self, e):
            self['background'] = self.hover_color
        
        def mouse_away(self, e):
            self['background'] = self.background
    
    class Entry(tk.Entry):
        def __init__(self, parent, *args, **kwargs):

            kwargs = {'width':40,
                      'highlightthickness':1,
                      'relief':tk.FLAT,
                      'highlightbackground':Style.bordercolor,
                      'background':Style.textbox_color,
                      'font':Style.font_heading} | kwargs

            super().__init__(parent, *args, **kwargs)


    class Combobox(ttk.Combobox):
        def __init__(self, parent, **kwargs):
            super().__init__(parent, **kwargs)
            self.bind("<<ComboboxSelected>>", self.select) 
            self.bind("<FocusIn>", self.defocus)
            self.unselected_option = ""

        def defocus(self, event):
            event.widget.master.focus_set()

        def set_options(self, options, current=0):
            self['values'] = options
            if current == None:
                self.set(self.unselected_option)
            else:
                self.current(current)
        
        def select(self, event):
            pass
        

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
                                background = Style.textbox_color,
                                highlightbackground=Style.bordercolor,
                                font=Style.font_body,
                                spacing1=2,
                                spacing2=Style.line_space)

            self.scrollb = ttk.Scrollbar(self, command=self.text.yview)
            
            self.text['yscrollcommand'] = self.scrollb.set

            self.scrollb.pack(side=tk.RIGHT, fill=tk.Y)
            self.text.pack(side=tk.RIGHT, fill='both', expand=True)
        
        def set_text(self, text):
            self.text.delete(1.0, "end")
            self.text.insert(1.0, text) 

        def get_text(self):
            return self.text.get(1.0, "end")