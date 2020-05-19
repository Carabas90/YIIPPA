from tkinter import (Tk, Label, Grid, W, E, Button, Scale, Radiobutton, Entry, Toplevel, messagebox, 
                    Frame, DoubleVar)
from CsvHandling import create_new, archive_patient, import_data, write_line
from YaleInsulinInfusionProtocol import insulin_adaptation, mmol_to_mg, mg_to_mmol
from functools import partial
from datetime import datetime, timedelta
from Setup import setup

class YiippaGUI:
    def __init__(self, master):
        """
        Opens the main window, from which inidvidual Patients can be selected and new Patients
        can be added.
        """
        self.master = master
        
        self.master.title('YIIPPA')
        
        self.mf = Frame(master)
        self.mf.grid()

        self.spacer0 = Label(self.mf, text='              ', font='Arial 20')
        self.spacer0.grid(row=0, column=0)

        self.h1 = Label(self.mf, text='Yale Insulin Infusion Protocol', font='Arial16')
        self.h1.grid(row=2, column=2, sticky=W)

        self.spacer1 = Label(self.mf, text='              ', font='Arial 16')
        self.spacer1.grid(row=3, column=4)

        self.i = self.create_pat_buttons(self.mf)
        self.i += 1

        self.spacer2 = Label(self.mf, text='              ', font='Arial 16')
        self.spacer2.grid(row=self.i, column=4)
        self.i += 1

        self.new_pat_b = Button(self.mf, text='Neuer Patient', command=self.new_pat)
        self.new_pat_b.grid(row=self.i, column=1)
        
        self.refresh_b = Button(self.mf, text='Aktualisieren', command=self.refresh)
        self.refresh_b.grid(row=self.i, column=3)
        self.i += 1
        
        self.spacer3 = Label(self.mf, text='              ', font='Arial 16')
        self.spacer3.grid(row=self.i, column=4)
        
    def open_pat(self, patlist):
        """
        Opens the Patient Window.
        """
        self.pat_window = PatWindow(self.master, patlist)
        self.master.wait_window(self.pat_window.pat_window)
        self.refresh()

    def create_pat_buttons(self, master):
        """
        Reads the Patient Data from legend.csv and creates a button corresponding to each Patient, 
        with which the Patient Window can be accessed.
        """
        pats = import_data('legend.csv')
        pats.pop(0) # Removes CSV-Header from the list
        i = 4 # Row to start showing the Buttons
        for p in pats:
            pat_name = p[1].title() + ' , ' + p[0].title() + '   ' + p[2]
            com = partial(self.open_pat, p) # Commands in Buttons can't have arguments, 
            #thats why partial is used to pass a function with arguments to the button
            pat_button = Button(master, text=pat_name, command=com)
            pat_button.grid(row=i , column=2)
            i += 1
        return i # Returns the last value for i, as a reference point for the rest of the GUI

    def refresh(self):
        """
        Destroys and rebuilds the GUI with the updated Data.
        """
        self.mf.destroy()
        self.__init__(self.master)

    def new_pat(self):
        """
        Opens an instance of NpWindow. refreshes the main Window, when NpWindow is closed.
        """
        self.np_window = NpWindow(self.master)
        self.master.wait_window(self.np_window.np_window)
        self.refresh()


class NpWindow():
    def __init__(self, master):
        """
        Opens an Input-Mask, where a new Patient can be added.
        """
        self.np_window = Toplevel(master)
        self.np_window.title('Neuer Patient')

        self.np_spacer0 = Label(self.np_window,text='        ', font='Arial 16')
        self.np_spacer0.grid(row=0, column=0, sticky=W)

        self.np_spacer1 = Label(self.np_window,text='        ', font='Arial 16')
        self.np_spacer1.grid(row=2, column=3, sticky=W)

        self.np_h1 = Label(self.np_window, text='Neuen Patienten aufnehmen:', font='Arial16')
        self.np_h1.grid(row=1, column=1, sticky=W)

        self.np_name_label = Label(self.np_window, text='Nachname', font='Arial 14')
        self.np_name_label.grid(row=3, column=1, sticky=W)
        self.np_name_entry = Entry(self.np_window)
        self.np_name_entry.grid(row=3, column=2, sticky=W)

        self.np_fname_label = Label(self.np_window, text='Vorname', font='Arial 14')
        self.np_fname_label.grid(row=4, column=1, sticky=W)
        self.np_fname_entry = Entry(self.np_window)
        self.np_fname_entry.grid(row=4, column=2, sticky=W)

        self.np_birthdate_label = Label(self.np_window, text='Geburtsdatum', font='Arial 14')
        self.np_birthdate_label.grid(row=5, column=1, sticky=W)
        self.np_birthdate_entry = Entry(self.np_window)
        self.np_birthdate_entry.grid(row=5, column=2, sticky=W)

        self.np_spacer2 = Label(self.np_window,text='        ', font='Arial 16')
        self.np_spacer2.grid(row=6, column=3, sticky=W)

        self.np_add_pat_button = Button(self.np_window, text='Patient aufnehmen', command= self.add_pat)
        self.np_add_pat_button.grid(row=7,column=2)

        self.np_spacer3 = Label(self.np_window,text='        ', font='Arial 16')
        self.np_spacer3.grid(row=8, column=3, sticky=W)

    def add_pat(self):
        """
        Uses the User Input to create e new Patient file and an entry in legend.csv
        """ 
        name = self.np_name_entry.get().title()
        fname = self.np_fname_entry.get().title()
        birthdate = self.np_birthdate_entry.get()

        if '' in (name, fname, birthdate):
            message = ('Fehlende Eingabe in einem oder mehreren Felder! Zur Aufnahme eines ' + 
                        'Patienten, achten sie bitte darauf, dass alle Felder ausgefüllt sind.')
            messagebox.showerror(title='Fehlende Eingabe', message=message)
        else:
            create_new(fname, name, birthdate)
            self.np_window.destroy()

class PatWindow:
    def __init__(self, master, patlist):
        """
        Opens the Patient Window, which serves as an entry mask for Blood-Glucose data, and allows
        the User to calculate the new insulin-rate or to archive the Patient.
        """
        self.patlist = patlist
        self.bz_data = import_data(self.patlist[3]) # Reads the Data from the CSV-File in the patlist
        self.bz_data.pop(0) # Removes CSV-Header
        self.now = datetime.now()

        self.pat_window = Toplevel()
        self.pat_window.title(self.patlist[1] + ' , ' + self.patlist[0])

        self.f = Frame(self.pat_window)
        self.f.grid()

        self.pat_spacer0 = Label(self.f ,text='        ', font='Arial 16')
        self.pat_spacer0.grid(row=0, column=0, sticky=W)

        self.pat_h1 = Label(self.f, text=(self.patlist[1]+ ' , '+self.patlist[0]+ '    '+ self.patlist[2]), font='Arial16')
        self.pat_h1.grid(row=1, column=1, sticky=W)

        self.pat_spacer1 = Label(self.f ,text='        ', font='Arial 16')
        self.pat_spacer1.grid(row=2, column=4, sticky=W)

        self.insulin_label = Label(self.f, text='Aktuelle Insulindosis:', font='Arial 14')
        self.insulin_label.grid(row=3, column=1, sticky=W)
        self.insulin_rate = DoubleVar()
        self.insulin_scale = Scale(self.f, from_=0.0, to=18.0, orient='horizontal', variable=self.insulin_rate,
                                   resolution=0.1, length=200)
        self.insulin_scale.grid(row=3, column=2, sticky=W, columnspan=2)
        if self.bz_data:
            self.insulin_scale.set(self.bz_data[-1][2])

        self.bz_old_label = Label(self.f, text= 'Voheriger Blutzucker:', font='Arial 14')
        self.bz_old_label.grid(row=4, column=1, sticky=W)
        self.bz_old_entry = Entry(self.f, width=10)
        self.bz_old_entry.grid(row=4, column=2, sticky=W)
        if self.bz_data:
            self.bz_old_entry.insert(0, str(self.bz_data[-1][3]))

        self.bz_old_dt_label = Label(self.f, text='Zeitpunkt des voherigen Blutzuckers:               '
                                    ,font='Arial 14')
        self.bz_old_dt_label.grid(row=5, column=1, sticky=W)
        self.bz_old_d_entry = Entry(self.f, width=12)
        self.bz_old_d_entry.grid(row=5, column=2, sticky=W)
        self.bz_old_t_entry = Entry(self.f, width=8)
        self.bz_old_t_entry.grid(row=5, column=3, sticky=W)
        if self.bz_data:
            self.bz_old_d_entry.insert(0,self.bz_data[-1][0])
            self.bz_old_t_entry.insert(0, self.bz_data[-1][1])
        else:
            self.bz_old_d_entry.insert(0, self.now.strftime('%d.%m.%Y'))

        self.pat_spacer2 = Label(self.f ,text='        ', font='Arial 16')
        self.pat_spacer2.grid(row=6, column=4, sticky=W)

        self.bz_new_label = Label(self.f, text= 'Aktueller Blutzucker:', font='Arial 14')
        self.bz_new_label.grid(row=7, column=1, sticky=W)
        self.bz_new_entry = Entry(self.f, width=10)
        self.bz_new_entry.grid(row=7, column=2, sticky=W) 
        
        self.bz_new_dt_label = Label(self.f, text='Zeitpunkt des aktuellen Blutzuckers:               '
                                    ,font='Arial 14')
        self.bz_new_dt_label.grid(row=8, column=1, sticky=W)
        self.bz_new_d_entry = Entry(self.f, width=12)
        self.bz_new_d_entry.grid(row=8, column=2, sticky=W)
        self.bz_new_t_entry = Entry(self.f, width=8)
        self.bz_new_t_entry.grid(row=8, column=3, sticky=W)
        self.bz_new_d_entry.insert(0, self.now.strftime('%d.%m.%Y'))
        self.bz_new_t_entry.insert(0, self.now.strftime('%H:%M'))

        self.pat_spacer3 = Label(self.f ,text='        ', font='Arial 16')
        self.pat_spacer3.grid(row=9, column=4, sticky=W)

        self.insulin_adjustment = Label(self.f ,text='        ', font='Arial 16')
        self.insulin_adjustment.grid(row=10, column=1, columnspan=2, sticky=W)

        self.pat_spacer4 = Label(self.f ,text='        ', font='Arial 16')
        self.pat_spacer4.grid(row=11, column=4, sticky=W)

        self.ca = partial(self.conf_archive, patlist)
        self.archive_button = Button(self.f, text='Patient archivieren', command=self.ca)
        self.archive_button.grid(row=12, column=1, sticky=W)

        self.calc_button = Button(self.f, text='Berechnen', command=self.calc)
        self.calc_button.grid(row=12, column=3, sticky=W)

        self.pat_spacer6 = Label(self.f ,text='        ', font='Arial 16')
        self.pat_spacer6.grid(row=13, column=4, sticky=W)


    def conf_archive(self, patlist):
        self.conf_window = Toplevel()
        self.conf_window.title('Bitte bestätigen!')

        self.conf_spacer0 = Label(self.conf_window, text='        ', font='Arial 16')
        self.conf_spacer0.grid(row=0, column=0, sticky=W)
        
        self.conf_label = Label(self.conf_window, text=('Sind Sie sicher, dass Sie '+ patlist[1] + ' , ' + patlist[0]
                                    + ' archivieren wollen. \n Die Patientendaten können nachträglich nicht'+ 
                                    'wiederhergestellt werden.'), font= 'Arial 14')
        self.conf_label.grid(row=1, column=1, rowspan=2, columnspan=3, sticky=W)

        self.conf_spacer1 = Label(self.conf_window, text='        ', font='Arial 16')
        self.conf_spacer1.grid(row=3, column=4, sticky=W)

        self.cancel_button = Button(self.conf_window, text='Abbrechen', command=self.conf_window.destroy)
        self.cancel_button.grid(row=4, column=1, sticky=W)

        self.a = partial(self.archive, patlist)
        self.confirm_button = Button(self.conf_window, text='Archivieren', command=self.a)
        self.confirm_button.grid(row=4, column=3, sticky=E)

        self.conf_spacer1 = Label(self.conf_window, text='        ', font='Arial 16')
        self.conf_spacer1.grid(row=5, column=4, sticky=W)


    def archive(self, patlist):
        """
        Archives Patient and closes all corresponding Windows.
        """
        archive_patient(self.patlist[0], self.patlist[1], self.patlist[2])
        self.conf_window.destroy()
        self.pat_window.destroy()

    def calc(self):
        """
        Calculates the new Insulin Rate unsin the Yale Insulin Infusion Protocol, and writes the Data
        to the Patients CSV-File.
        """
        try:    
            bg = int(self.bz_new_entry.get())
            dt_old = datetime.strptime((self.bz_old_d_entry.get()+self.bz_old_t_entry.get()), '%d.%m.%Y%H:%M')
            dt_new = datetime.strptime((self.bz_new_d_entry.get()+self.bz_new_t_entry.get()), '%d.%m.%Y%H:%M')
            dt_delta = dt_new - dt_old
            dt_change = (dt_delta.days * 24) + (dt_delta.seconds / 3600)
       
            if dt_change <= 0:
                messagebox.showerror(message='Zeitpunkt des voherigen Blutzuckers liegt nach dem' +
                                 'Zeitpunkt des aktuellen Blutzuckers')
                return
        
            bg_change = (bg - int(self.bz_old_entry.get())) / dt_change
            insulin_rate = self.insulin_rate.get()
        
        except:
            messagebox.showerror(message='Ungültige Eingabe in mindestens einem Feld!')
            return

        insulin_adapted = insulin_adaptation(bg, bg_change, insulin_rate)

        self.insulin_adjustment['text'] = 'Die neue Insulin-Laufrate ist ' + str(insulin_adapted) + ' IE/h!'
        
        self.data_old = [self.bz_old_d_entry.get(), self.bz_old_t_entry.get(), self.insulin_rate.get(), self.bz_old_entry.get()]
        if (not self.bz_data) or (self.bz_data[-1] != self.data_old):
            write_line(self.patlist[3], self.data_old)

        self.data_new = [self.bz_new_d_entry.get(), self.bz_new_t_entry.get(), self.insulin_rate.get(), self.bz_new_entry.get()]
        write_line(self.patlist[3], self.data_new)


if __name__ == '__main__':
    setup()
    root = Tk()
    sofa_gui = YiippaGUI(root)
    root.mainloop()