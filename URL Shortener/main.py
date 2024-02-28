from tkinter import Tk, Label, Entry, Button, PhotoImage, messagebox
import pyshorteners

dark_green = '#61892F'
light_green = '#86C232'
black = '#000000'
ocean_blue = '#23313f'
font = 'Garamond'


class URLShortener:
    def __init__(self):
        self.short_url = None

        self.main_win = Tk()
        self.main_win.geometry('500x380+420+130')
        self.main_win.title('URL Shortener App')
        self.main_win.resizable(False, False)
        self.main_win.config(bg=ocean_blue)
        img = PhotoImage(file='link icon.png')
        self.main_win.iconphoto(False, img)

    def labels(self):
        self.paste_url_lab = Label(self.main_win, text='Enter URL', font=(font, 20, 'bold'), fg=light_green,
                                   bg=ocean_blue)
        self.paste_url_lab.place(x=182, y=110)

        url_img = PhotoImage(file='header image.png')
        self.url_icon= Label(self.main_win, image=url_img, bg=ocean_blue)
        self.url_icon.image = url_img
        self.url_icon.place(x=10 ,y=10)

    def entries(self):
        self.url_entry = Entry(self.main_win, font=(font, 15, 'bold'), fg=black, bg=dark_green, width=40)
        self.url_entry.place(x=70, y=160)

        self.url = Entry(self.main_win, font=(font, 20, 'bold'), fg=light_green, bg=ocean_blue, width=30, bd=0,
                         justify='center')
        self.url.pack(side='bottom', pady=50)

    def buttons(self):
        self.shorten_btn = Button(self.main_win, text='Shorten URL', font=(font, 12, 'bold'), fg=light_green,
                                  bg=ocean_blue, activeforeground=light_green, activebackground=ocean_blue,
                                  relief= 'raised', width=13,bd=6, command=self.process)
        self.shorten_btn.place(x=175, y=205)

    def process(self):
        long_url = self.url_entry.get()
        new_url = self.url.get()

        if long_url == '':
            messagebox.showerror('No Link', 'No link was found!')
            self.url.delete(0, 'end')

        else:
            try:
                if new_url != '':
                    self.url.delete(0, 'end')

                url_object = pyshorteners.Shortener()
                self.short_url = url_object.isgd.short(long_url)
                self.url.insert('end', self.short_url)

            except pyshorteners.exceptions.ShorteningErrorException:
                messagebox.showerror('Invalid Link', 'The link entered does not exist!')
                self.url_entry.delete(0, 'end')
                self.url.delete(0, 'end')


u = URLShortener()
u.labels()
u.entries()
u.buttons()
u.main_win.mainloop()
