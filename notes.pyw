import tkinter
import tkinter.filedialog
from tkinter import messagebox

class Note():
    def __init__(self):
        self.note_width = 256
        self.note_height = 256
        self.is_dragged = False #флаг перемещения заметки
        self.is_minimized = False #флаг, что заметка свёрнута
        self.clicked_x = 0
        self.clicked_y = 0
        self.window_x = 0
        self.window_y = 0

        self.create_window()
        self.create_top_panel()
        self.create_minimized_panel()
        self.bind_events()
        self.bind_buttons()
        self.create_note()

        self.window.mainloop()

    def create_window(self):
        self.window = tkinter.Tk()
        self.window.geometry('%sx%s' %(self.note_width, self.note_height))
        self.window.wm_attributes("-topmost", True) #поверх всех окон
        self.window.wm_attributes('-alpha', 0.75) #прозрачность
        self.window.wm_iconbitmap("img/icon.ico")
        self.window.overrideredirect(True) #отключаю верхнюю панель
        self.window.title('ScreenNotes by Dragmor')

    def create_note(self):
        #поле ввода заметки
        self.note_text = tkinter.Text(bg='yellow', font='system')
        self.note_text.pack()

    def create_top_panel(self):
        #развёрнутая панель
        self.top_panel = tkinter.Canvas(self.window, bg='yellow', width=self.note_width, height=20)
        self.top_panel.pack()
        #кнопка 'выход'
        self.image_button_exit = tkinter.PhotoImage(file='img/btn_exit.png')
        self.top_panel.create_image(self.note_width-self.image_button_exit.width()//2-2, self.image_button_exit.height()//2+2, image=self.image_button_exit, tag='exit_btn')
        #кнопка 'свернуть'
        self.image_button_iconify = tkinter.PhotoImage(file='img/btn_iconify.png')
        self.image_button_deiconify = tkinter.PhotoImage(file='img/btn_deiconify.png')
        self.top_panel.create_image(self.note_width-self.image_button_iconify.width()*2, self.image_button_iconify.height()//2+2, image=self.image_button_iconify, tag='iconify_btn')
        #кнопка 'сохранить'
        self.image_button_save = tkinter.PhotoImage(file='img/btn_save.png')
        self.top_panel.create_image(self.image_button_save.width()//2+2, self.image_button_save.height()//2+2, image=self.image_button_save, tag='save_btn')
        #кнопка 'загрузить'
        self.image_button_load = tkinter.PhotoImage(file='img/btn_load.png')
        self.top_panel.create_image(self.image_button_load.width()*2+2, self.image_button_load.height()//2+2, image=self.image_button_load, tag='load_btn')
        #кнопка 'поверх других окон'
        self.image_button_topmost_on = tkinter.PhotoImage(file='img/btn_topmost_on.png')
        self.image_button_topmost_off = tkinter.PhotoImage(file='img/btn_topmost_off.png')
        self.top_panel.create_image(self.image_button_topmost_on.width()*4+2, self.image_button_topmost_on.height()//2+2, image=self.image_button_topmost_on, tag='topmost_btn')
        #свёрнутая панель
        self.minimized_panel = tkinter.Canvas(self.window, bg='yellow', width=self.image_button_exit.width()*4, height=20)

    def bind_events(self):
        self.top_panel.bind("<Button-1>", self.mouse_event)
        self.top_panel.bind("<Motion>", self.drag_note)
        self.top_panel.bind("<ButtonRelease-1>", self.mouse_event)

    def bind_buttons(self):
        self.top_panel.tag_bind("exit_btn", "<Button-1>", self.pre_exit)
        self.top_panel.tag_bind("iconify_btn", "<Button-1>", self.minimize)
        self.top_panel.tag_bind("save_btn", "<Button-1>", self.save)
        self.top_panel.tag_bind("load_btn", "<Button-1>", self.load)
        self.top_panel.tag_bind("topmost_btn", "<Button-1>", self.topmost)

    def minimize(self, *args):
        '''метод минимизации окна'''
        if self.is_minimized == False:
            self.is_minimized = True
            self.top_panel.forget()
            self.note_text.forget()
            self.minimized_panel.pack()
            self.window.geometry('%sx%s+%s+%s' %(self.image_button_exit.width()*4, 24, self.window_x+(self.note_width-self.image_button_exit.width()*4), self.window_y))
            self.top_panel.itemconfigure('iconify_btn', image=self.image_button_deiconify)
        else:
            self.is_minimized = False
            self.minimized_panel.forget()
            self.top_panel.pack()
            self.note_text.pack()
            self.window.geometry('%sx%s+%s+%s' %(self.note_width, self.note_height, self.window_x, self.window_y))
            self.top_panel.itemconfigure('iconify_btn', image=self.image_button_iconify)

    def pre_exit(self, *args):
        if self.note_text.get(index1='current' ,index2='end') != '\n':
            user_choose = messagebox.askyesnocancel(title='', message='Сохранить текущий текст перед выходом?')
            if user_choose == True:
                self.save()
            elif user_choose == None:
                return
        exit()

    def create_minimized_panel(self):
        self.minimized_panel.create_image(self.image_button_exit.width()*4-self.image_button_exit.width()//2-2, self.image_button_exit.height()//2+2, image=self.image_button_exit, tag='btn_exit')
        self.minimized_panel.create_image(self.image_button_deiconify.width()*2, self.image_button_deiconify.height()//2+2, image=self.image_button_deiconify, tag='btn_deiconify')
        if self.window.wm_attributes("-topmost") == True:
            self.btn_topmost = self.image_button_topmost_on
        else:
            self.btn_topmost = self.image_button_topmost_off
        self.minimized_panel.create_image(self.image_button_topmost_on.width()-8, self.image_button_topmost_on.height()//2+2, image=self.btn_topmost, tag='topmost_btn')
        self.minimized_panel.tag_bind("btn_exit", "<Button-1>", self.pre_exit)
        self.minimized_panel.tag_bind("btn_deiconify", "<Button-1>", self.minimize)
        self.minimized_panel.tag_bind("topmost_btn", "<Button-1>", self.topmost)
        self.minimized_panel.bind("<Button-1>", self.mouse_event)
        self.minimized_panel.bind("<Motion>", self.drag_note)
        self.minimized_panel.bind("<ButtonRelease-1>", self.mouse_event)

    def topmost(self, *args):
        if self.window.wm_attributes("-topmost") == True:
            self.window.wm_attributes("-topmost", False)
            self.top_panel.itemconfigure('topmost_btn', image=self.image_button_topmost_off)
            self.minimized_panel.itemconfigure('topmost_btn', image=self.image_button_topmost_off)
        else:
            self.window.wm_attributes("-topmost", True)
            self.top_panel.itemconfigure('topmost_btn', image=self.image_button_topmost_on)
            self.minimized_panel.itemconfigure('topmost_btn', image=self.image_button_topmost_on)

    def save(self, *args):
        filename = tkinter.filedialog.asksaveasfilename(defaultextension='txt',
         initialfile='note.txt')
        if filename != '':
            file = open(filename, 'w')
            text = self.note_text.get(index1='current' ,index2='end')
            file.write(text)
            file.close()

    def load(self, *args):
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            file = open(filename, 'r')
            text = file.read()
            file.close()
            self.note_text.replace('current', 'end', text)

    def mouse_event(self, event):
        #если была нажата ЛКМ
        if event.state == 8:
            #включаю флаг режима перетаскивания окна
            self.is_dragged = True
            self.clicked_x = (self.window.winfo_pointerx()
                -self.window.winfo_rootx())
            self.clicked_y = (self.window.winfo_pointery()
                -self.window.winfo_rooty())
        else:
            self.is_dragged = False

    def drag_note(self, event, *args):
        '''метод для перетаскивания заметки'''
        if event.state != 264:
            self.is_dragged = False
        if self.is_dragged:
            self.window_x = self.window.winfo_pointerx()-self.clicked_x
            self.window_y = self.window.winfo_pointery()-self.clicked_y
            if self.is_minimized == True:
                height = 24
                width = self.image_button_exit.width()*4
            else:
                height = self.note_height
                width = self.note_width
            #двигаю
            self.window.geometry('%sx%s+%s+%s' %(
                width,
                height,
                self.window_x,
                self.window_y))


if __name__ == "__main__":
    screenNote = Note()
