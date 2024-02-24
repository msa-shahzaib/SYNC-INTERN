from tkinter import Tk, Label, Entry, Button, PhotoImage, Spinbox
from datetime import datetime, timedelta
import pygame

BLUE = '#05386B'
WHITE = '#EDF5E1'
DULL_GREEN = '#8EE4AF'
DARK_GREEN = '#379683'
GREEN = '#5CDB95'


class Alarm:
    def __init__(self):
        self.h = None
        self.m = None
        self.s = None
        self.alarmStatus = False

        self.main_win = Tk()
        self.main_win.title("alarm clock app")
        self.main_win.geometry("520x380+400+130")
        self.main_win.config(bg=BLUE)
        self.main_win.resizable(False, False)
        img = PhotoImage(file='alarm.png')
        self.main_win.iconphoto(False, img)

        self.title_label = Label(self.main_win, text='Digital Alarm Clock', font=('digital-7', 30, 'bold'), fg=GREEN,
                                 bg=BLUE)
        self.title_label.pack(pady=10)

        self.time_title_label = Label(self.main_win, text='Local Time :', font=('digital-7', 25), fg=WHITE,
                                      bg=BLUE)
        self.time_title_label.place(x=100, y=100)

        self.CurrentTime()
        self.alarmSetting()

    def CurrentTime(self):
        current_time = datetime.now().strftime("%H : %M : %S")
        time_label = Label(self.main_win, text=current_time, font=('digital-7', 25, 'bold'), fg=BLUE, bg=GREEN, padx=12)
        time_label.place(x=265, y=100)
        time_label.after(1000, self.CurrentTime)

    def alarmSetting(self):
        self.set_alarm_lab = Label(self.main_win, text='Set an alarm', font=('digital-7', 20, 'bold'), fg=WHITE,
                                   bg=BLUE)
        self.set_alarm_lab.place(x=185, y=170)

        hr_val = [f'0{i}' if i < 10 else i for i in range(24)]
        self.h_spin = Spinbox(self.main_win, values=hr_val, font=('digital-7', 22, 'bold'), fg=BLUE, bg=DULL_GREEN,
                              wrap=True, width=2)
        self.h_spin.place(x=170, y=210)

        other_val = [f'0{i}' if i < 10 else i for i in range(60)]

        self.m_spin = Spinbox(self.main_win, values=other_val, font=('digital-7', 22, 'bold'), fg=BLUE,
                              bg=DULL_GREEN, wrap=True, width=2)
        self.m_spin.place(x=240, y=210)

        self.s_spin = Spinbox(self.main_win, values=other_val, font=('digital-7', 22, 'bold'), fg=BLUE,
                              bg=DULL_GREEN, wrap=True, width=2)
        self.s_spin.place(x=310, y=210)

        self.set_title_lab = Label(self.main_win, text='Alarm Title :', font=('digital-7', 18, 'bold'), fg=WHITE,
                                   bg=BLUE)
        self.set_title_lab.place(x=70, y=270)

        self.title_entry = Entry(self.main_win, width=19, font=('digital-7', 18, 'bold'), fg=BLUE, bg=DULL_GREEN)
        self.title_entry.place(x=220, y=270)

        self.set_button = Button(self.main_win, text='set', font=('digital-7', 12, 'bold'), fg=BLUE, bg=GREEN,
                                 activeforeground=BLUE, activebackground=GREEN, relief='raised', bd=6, width=5,
                                 command=self.setAlarm)
        self.set_button.pack(side='bottom', pady=25)

    def setAlarm(self):
        self.h = self.h_spin.get()
        self.m = self.m_spin.get()
        self.s = self.s_spin.get()
        self.title = self.title_entry.get()

        self.set_alarm_lab.destroy()
        self.h_spin.destroy()
        self.m_spin.destroy()
        self.s_spin.destroy()
        self.set_button.destroy()
        self.set_title_lab.destroy()
        self.title_entry.destroy()

        if self.title == '':
            self.title = '[untitled]'

        self.reminder_lab = Label(self.main_win, text=f'Alarm will ring at :', font=('digital-7', 20, 'bold'),
                                  fg=WHITE, bg= BLUE)
        self.reminder_lab.place(x=80, y=240)

        self.alarm_time = Label(self.main_win, text=f'{self.h} : {self.m} : {self.s}', font=('digital-7', 20, 'bold'),
                                fg=GREEN, bg=BLUE)
        self.alarm_time.place(x=320, y=240)

        self.checkAlarm()

    def checkAlarm(self):
        now = datetime.now()
        if int(self.h) == now.hour and int(self.m) == now.minute and int(self.s) == now.second:
            self.reminder_lab.destroy()
            self.alarm_time.destroy()

            self.alarm_title_lab = Label(self.main_win, text=self.title, font=('digital-7', 20, 'bold'), fg=WHITE,
                                         bg=BLUE)
            self.alarm_title_lab.pack(side='top', pady=140)

            self.snooze_button = Button(self.main_win, text='snooze', font=('digital-7', 14, 'bold'), fg=BLUE,
                                       bg=GREEN, activeforeground=BLUE, activebackground=GREEN,
                                       relief='raised', width=8, bd=6, command=self.snoozeAlarm)
            self.snooze_button.place(x=140, y=300)

            self.stop_button = Button(self.main_win, text='stop', font=('digital-7', 14, 'bold'), fg=BLUE,
                                     bg=GREEN, activeforeground=BLUE, activebackground=GREEN,
                                      relief='raised', bd=6, width=8, command=self.stopAlarm)
            self.stop_button.place(x=290, y=300)

            self.alarmStatus = True
            self.alarmTone()

        else:
            self.main_win.after(1000, self.checkAlarm)

    @staticmethod
    def alarmTone():
        pygame.mixer.init()
        pygame.mixer.music.load('metamorphosis (sigma song).mp3')
        pygame.mixer.music.play()

    def snoozeAlarm(self):
        if self.alarmStatus:
            self.alarm_title_lab.destroy()
            self.snooze_button.destroy()
            self.stop_button.destroy()

            self.snooze = Label(self.main_win, text='Snooze for (mins) :', font=('digital-7', 20, 'bold'), fg=WHITE,
                                bg=BLUE)
            self.snooze.place(x=130, y=230)

            self.s_time_entry = Entry(self.main_win, width=2, font=('digital-7', 20, 'bold'), fg=BLUE, bg=DULL_GREEN)
            self.s_time_entry.place(x=360, y=230)

            self.warning = Label(self.main_win, text='', font=('digital-7', 12, 'bold'), fg='red', bg=BLUE)
            self.warning.place(x=210, y=270)

            self.set_button = Button(self.main_win, text='set', font=('digital-7', 12, 'bold'), fg=BLUE,
                                     bg=GREEN, activeforeground=BLUE, activebackground=GREEN,
                                     relief='raised', bd=6, width=5, command=self.resetAlarm)
            self.set_button.pack(side='bottom', pady=40)

    def resetAlarm(self):
        snooze_duration = self.s_time_entry.get()

        if not (snooze_duration.isdigit()):
            self.s_time_entry.delete(0, 'end')
            self.warning.config(text='Invalid time!')

        else:
            self.warning.config(text='')
            self.snooze.destroy()
            self.s_time_entry.destroy()
            self.set_button.destroy()

            pygame.mixer.music.stop()
            delay_time = timedelta(minutes=int(snooze_duration))

            current_time = datetime.now()
            new_time = current_time + delay_time

            self.h = new_time.hour
            self.m = new_time.minute
            self.s = new_time.second

            self.reminder_lab = Label(self.main_win, text=f'Alarm will ring at :', font=('digital-7', 20, 'bold'),
                                      fg=WHITE, bg=BLUE)
            self.reminder_lab.place(x=80, y=240)

            self.alarm_time = Label(self.main_win, text=f'{self.h:02d} : {self.m:02d} : {self.s:02d}',
                                    font=('digital-7', 20, 'bold'), fg=GREEN, bg=BLUE)
            self.alarm_time.place(x=320, y=240)

            self.checkAlarm()

    def stopAlarm(self):
        if self.alarmStatus:
            pygame.mixer.music.stop()
            self.alarmStatus = False

            self.stop_button.destroy()
            self.snooze_button.destroy()
            self.alarm_title_lab.destroy()

            self.alarmSetting()


a = Alarm()
a.main_win.mainloop()

