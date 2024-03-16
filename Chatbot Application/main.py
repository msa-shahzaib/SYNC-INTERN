from tkinter import Tk, PhotoImage, Frame, Text, Label, Entry, Button, Scrollbar
from chatbot import get_response

FONT = 'Consolas'
BLACK = '#000000'
DULL_BLACK = '#272727'
GREY = '#747474'
ORANGE = '#FF652F'
YELLOW = '#FFE400'
SEA_GREEN = '#14A76C'
BOT_NAME = 'CraveMate'


class FoodOrderingInterface:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('400x460+480+100')
        self.root.title('ChatBot')
        self.root.resizable(False, False)
        self.root.config(bg=DULL_BLACK)
        img = PhotoImage(file='chatbot.png')
        self.root.iconphoto(False, img)

    def framework(self):
        self.frame = Frame(self.root, height=280, width=340, bg=GREY)
        self.frame.pack(side='top', pady=90)

    def chatbox(self):
        self.scroller = Scrollbar(self.frame, orient='vertical')
        self.scroller.pack(side='right', fill='both')

        self.textbox = Text(self.frame, height=25, width=60, bg=GREY, bd=3, relief='sunken', selectbackground=GREY,
                            selectforeground=BLACK, highlightbackground=DULL_BLACK, font=(FONT, 8), fg=BLACK)
        self.textbox.pack()

        self.textbox.config(yscrollcommand=self.scroller.set, state='disabled')
        self.scroller.config(command=self.textbox.yview)

    def label(self):
        self.empty_lab = Label(self.root, padx=400, pady=25, bg=ORANGE)
        self.empty_lab.place(x=0, y=0)

        self.header = Label(self.root, text='Welcome to FlavorsVille!'.upper(), font=(FONT, 18, 'bold'), fg=BLACK,
                            bg=ORANGE)
        self.header.place(x=50, y=20)

    def entry(self):
        self.prompt = Entry(self.root, font=(FONT, 18, 'bold'), fg=BLACK, bg=GREY, width=23)
        self.prompt.place(x=8,y=396)

    def buttons(self):
        self.sendButton = Button(self.root, text='send', font=(FONT, 14, 'bold'), fg=BLACK, bg=SEA_GREEN, bd=5,
                                 activebackground=SEA_GREEN, activeforeground=BLACK, relief='raised', width=5,
                                 command=self.sendPrompt)
        self.sendButton.place(x=325, y=390)

    def sendPrompt(self):
        prompt = self.prompt.get()

        if not prompt:
            return

        self.prompt.delete(0, 'end')
        msg1 = 'You: ' + prompt + '\n\n'
        msg2 = f'{BOT_NAME}: {get_response(prompt)}\n\n'

        self.textbox.config(state='normal')
        self.textbox.insert('end', msg1)
        self.textbox.insert('end', msg2)
        self.textbox.config(state='disabled')

        self.textbox.see('end')


bot = FoodOrderingInterface()
bot.framework()
bot.chatbox()
bot.label()
bot.entry()
bot.buttons()
bot.root.mainloop()

