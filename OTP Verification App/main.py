from tkinter import Tk, PhotoImage, Label, Canvas, Entry, Button, messagebox
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

dark_blue = '#25274D'
dark_grey = '#464866'
silver = '#AAABB8'
font = 'Consolas'


class OTPVerificationApp:
    def __init__(self, sender_email, app_password, recipients_email):
        self.sender_email = sender_email
        self.app_password = app_password
        self.recipients_email = recipients_email

        self.code = None
        self.counter = 60

        self.main_win = Tk()
        self.main_win.geometry('500x500+420+100')
        self.main_win.title('OTP Verification App')
        self.main_win.resizable(False, False)
        self.main_win.config(bg=dark_grey)
        image = PhotoImage(file='otp icon.png')
        self.main_win.iconphoto(False, image)

    @staticmethod
    def generateOTP():
        return str(random.randint(100000, 999999))

    def generateEmail(self):
        subject = 'OTP Verification Code'
        body = 'Your OTP verification code is ' + self.code

        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.recipients_email
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(self.sender_email, self.app_password)
        server.sendmail(self.sender_email, self.recipients_email, message.as_string())

        server.quit()

    def canvas(self):
        self.c = Canvas(self.main_win, width=300, height=200, bg=silver, highlightbackground=dark_grey)
        self.c.place(x=98, y=190)

    def labels(self):
        self.header_lab = Label(self.main_win, text='<OTP VERIFICATION>', font=(font,25,'bold'), fg=silver,
                                bg=dark_grey)
        self.header_lab.pack(pady=22)

        self.email_req_lab = Label(self.c, text=f'Enter your email address',font=(font,15,'bold'), fg=dark_blue, bg=silver)
        self.email_req_lab.place(x=20, y=40)

        img = PhotoImage(file='header image.png')
        self.image_lab = Label(self.main_win, image=img, bg=dark_grey)
        self.image_lab.image = img
        self.image_lab.place(x=170 ,y=75)

        self.enter_otp_lab = Label(self.c, text=f'Enter OTP we send to\n{self.recipients_email}',font=(font,15,'bold'),
                                   fg=dark_blue, bg=silver)

        self.timer = Label(self.c, text='', font=(font, 14, 'bold'), fg=dark_blue, bg=silver)

    def entries(self):
        self.email_entry = Entry(self.c, font=(font,14,'bold'), fg=dark_blue, bg=silver, width=25)
        self.email_entry.place(x=30, y=100)

        self.otp_entry = Entry(self.c, font=(font,14,'bold'), fg=dark_blue, bg=silver, width=8)

    def buttons(self):
        self.submit_btn = Button(self.c, text='submit',font=(font,10,'bold'), fg=silver, bg=dark_grey, width=8,
                                    activeforeground=silver, activebackground=dark_grey, relief='raised', bd=6,
                                    command=self.process)
        self.submit_btn.place(x=113, y=140)

        self.submit_button = Button(self.c, text='submit',font=(font,10,'bold'), fg=silver, bg=dark_grey, width=8,
                                    activeforeground=silver, activebackground=dark_grey, relief='raised', bd=6,
                                    command=self.verification)

        self.resend_btn = Button(self.main_win, text='resend OTP',font=(font,10,'bold'), fg=dark_blue, bg=silver,
                                 width=12, activeforeground=dark_blue, activebackground=silver, relief='raised',
                                 bd=6, command=self.resendCode)

    def countdown(self):
        if self.counter > 0:
            self.counter -= 1
            self.timer.config(text=f'{self.counter:02d}')
            self.timer.after(1000, self.countdown)

        else:
            messagebox.showerror('Timeout', 'Your OTP has expired!\nClick on Resend OTP to get a new one')
            self.code = None

    def process(self):
        inputEmail = self.email_entry.get()

        if inputEmail == self.recipients_email:
            self.code = self.generateOTP()
            self.generateEmail()

            self.email_req_lab.destroy()
            self.email_entry.destroy()
            self.submit_btn.destroy()

            self.enter_otp_lab.place(x=35, y=20)
            self.timer.place(x=135, y=75)
            self.otp_entry.place(x=110, y=110)
            self.submit_button.place(x=113, y=150)
            self.resend_btn.pack(side='bottom', pady=30)

            self.countdown()

        else:
            messagebox.showerror('Invalid Email', 'Email address does not match!')
            self.email_entry.delete(0, 'end')

    def verification(self):
        code = self.otp_entry.get()

        if code == self.code:
            self.timer.config(fg=silver)
            self.enter_otp_lab.destroy()
            self.otp_entry.destroy()
            self.submit_button.destroy()
            self.resend_btn.destroy()
            self.counter = 10000

            self.msg = Label(self.c, text='Login Successful!', font=(font, 20, 'bold'), fg=dark_blue, bg=silver)
            self.msg.place(x=25, y=80)

            self.exit_btn = Button(self.main_win, text='EXIT', font=(font, 10, 'bold'), fg=silver, bg=dark_grey,width=6,
                                   activeforeground=silver, activebackground=dark_grey, relief='raised', bd=6,
                                   command=quit)
            self.exit_btn.pack(side='bottom', pady=30)

        elif not(code.isdigit()):
            messagebox.showwarning('Type Error', 'Enter valid code!')
            self.otp_entry.delete(0, 'end')

        else:
            messagebox.showwarning('Invalid OTP', 'OTP does not match!')
            self.otp_entry.delete(0, 'end')

    def resendCode(self):
        self.code = self.generateOTP()
        self.generateEmail()
        messagebox.showinfo('OTP Sent', f'An OTP has been send to {self.recipients_email} successfully!')
        self.counter = 60
        self.countdown()


# Make sure to add sender, receiver and app password of your gmail id#

otp = OTPVerificationApp('','','')
otp.canvas()
otp.labels()
otp.entries()
otp.buttons()
otp.main_win.mainloop()

