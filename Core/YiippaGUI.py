from tkinter import (Tk, Label, Grid, W, Button, Scale, Radiobutton, Entry, Toplevel, messagebox, 
                    Frame)
from CsvHandling import create_new, archive_patient, import_data
from functools import partial

class YiippaGUI:
    def __init__(self, master):
        """
        Opens the main window, from which inidviduall Patients can be selected and new Patients
        can be added.
        """
        self.master = master
        
        self.master.title('YIIPPA')
        
        self.mf = Frame(master)
        self.mf.grid()

        self.spacer0 = Label(self.mf, text='              ', font='Times 20')
        self.spacer0.grid(row=0, column=0)

        self.h1 = Label(self.mf, text='Yale Insulin Infusion Protocol', font='Times16')
        self.h1.grid(row=2, column=2, sticky=W)

        self.spacer1 = Label(self.mf, text='              ', font='Times 16')
        self.spacer1.grid(row=3, column=4)

        self.i = self.create_pat_buttons(self.mf)
        self.i += 1

        self.spacer2 = Label(self.mf, text='              ', font='Times 16')
        self.spacer2.grid(row=self.i, column=4)
        self.i += 1

        self.new_pat_b = Button(self.mf, text='Neuer Patient', command=self.new_pat)
        self.new_pat_b.grid(row=self.i, column=1)
        
        self.refresh_b = Button(self.mf, text='Aktualisieren', command=self.refresh)
        self.refresh_b.grid(row=self.i, column=3)
        self.i += 1
        
        self.spacer3 = Label(self.mf, text='              ', font='Times 16')
        self.spacer3.grid(row=self.i, column=4)
        
    def open_pat(self, patlist):
        """
        Opens the Patient Window.
        """
        self.pat_window = PatWindow(patlist)

    def create_pat_buttons(self, master):
        """
        Reads the Patient Data from legend.csv and creates a button corresponding to each Patient, 
        with which the Patient Window can be accessed.
        """
        pats = import_data('legend.csv')
        pats.pop(0)
        i = 4
        for p in pats:
            pat_name = p[1].title() + ' , ' + p[0].title() + '   ' + p[2]
            com = partial(self.open_pat, p)
            pat_button = Button(master, text=pat_name, command=com)
            pat_button.grid(row=i , column=2)
            i += 1
        return i

    def refresh(self):
        """
        Destroys and rebuilds the GUI with the updated Data.
        """
        self.mf.destroy()
        self.__init__(self.master)

    def new_pat(self):
        self.np_window = NpWindow()


class NpWindow():
    def __init__(self):
        """
        Opens an Input-Mask, where a new Patient can be added.
        """
        self.np_window = Toplevel()
        self.np_window.title('Neuer Patient')

        self.np_spacer0 = Label(self.np_window,text='        ', font='Times 16')
        self.np_spacer0.grid(row=0, column=0, sticky=W)

        self.np_spacer1 = Label(self.np_window,text='        ', font='Times 16')
        self.np_spacer1.grid(row=2, column=3, sticky=W)

        self.np_h1 = Label(self.np_window, text='Neuen Patienten aufnehmen:', font='Times16')
        self.np_h1.grid(row=1, column=1, sticky=W)

        self.np_name_label = Label(self.np_window, text='Nachname', font='Times14')
        self.np_name_label.grid(row=3, column=1, sticky=W)
        self.np_name_entry = Entry(self.np_window)
        self.np_name_entry.grid(row=3, column=2, sticky=W)

        self.np_fname_label = Label(self.np_window, text='Vorname', font='Times14')
        self.np_fname_label.grid(row=4, column=1, sticky=W)
        self.np_fname_entry = Entry(self.np_window)
        self.np_fname_entry.grid(row=4, column=2, sticky=W)

        self.np_birthdate_label = Label(self.np_window, text='Geburtsdatum', font='Times14')
        self.np_birthdate_label.grid(row=5, column=1, sticky=W)
        self.np_birthdate_entry = Entry(self.np_window)
        self.np_birthdate_entry.grid(row=5, column=2, sticky=W)

        self.np_spacer2 = Label(self.np_window,text='        ', font='Times 16')
        self.np_spacer2.grid(row=6, column=3, sticky=W)

        self.np_add_pat_button = Button(self.np_window, text='Patient aufnehmen', command= self.add_pat)
        self.np_add_pat_button.grid(row=7,column=2)

        self.np_spacer3 = Label(self.np_window,text='        ', font='Times 16')
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
    def __init__(self, patlist):
        self.pat_window = Toplevel()
        self.pat_window.title(patlist[1] + ' , ' + patlist[0])

        self.f = Frame(self.pat_window)
        self.f.grid()

        self.pat_spacer0 = Label(self.f ,text='        ', font='Times 16')
        self.pat_spacer0.grid(row=0, column=0, sticky=W)

        self.pat_h1 = Label(self.f, text=(patlist[1]+ ' , '+patlist[0]+ '    '+ patlist[2]), font='Times16')
        self.pat_h1.grid(row=1, column=1, sticky=W)

        










if __name__ == '__main__':
    root = Tk()
    sofa_gui = YiippaGUI(root)
    root.mainloop()