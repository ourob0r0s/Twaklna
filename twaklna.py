import csv
import sqlite3
from builtins import ValueError
from datetime import datetime

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class Project:


    def __init__(self):

        conn = sqlite3.connect('CCS227')
        cursor = conn.cursor()
        try:
            table = """CREATE TABLE PEOPLE(
                    FNAME VARCHAR(100),
                    LNAME VARCHAR(100),
                    SEX CHAR(6),
                    ID INT(10) NOT NULL,
                    YEAROFBIRTH INT(4),
                    TYPEOFVACCINCE VARCHAR(100),
                    DATEANDTIME DATETIME,
                    PNUMBER VARCHAR(10)
                    );"""

            cursor.execute(table)
        except Exception:
            print()

        self.app = tk.Tk()
        self.app.title('Vaccination')

        self.notebook = ttk.Notebook(self.app)
        self.notebook.pack()


        self.labelframe = tk.LabelFrame(self.app, text="check in")
        self.labelframe2 = tk.LabelFrame(self.app, text="immunty check")
        self.labelframe3 = tk.LabelFrame(self.app, text="import and export")
        self.frame = tk.Frame(self.labelframe)
        self.frame.pack()
        self.labelframe.pack()
        self.labelframe2.pack()
        self.labelframe3.pack()
        self.notebook.add(self.labelframe, text='check in ')
        self.notebook.add(self.labelframe2, text='immunty check ')
        self.notebook.add(self.labelframe3, text='import and export')

        self.x1 = tk.Label(self.labelframe, text="ID")
        self.x1.pack()
        self.y1 = tk.Entry(self.labelframe, width=40)
        self.y1.pack()
        self.y1.insert(0, 'must be 10 digits')

        self.x2 = tk.Label(self.labelframe, text="First name")
        self.x2.pack()
        self.y2 = tk.Entry(self.labelframe, width=40)
        self.y2.pack()

        self.x3 = tk.Label(self.labelframe, text="Last name")
        self.x3.pack()
        self.y3 = tk.Entry(self.labelframe, width=40)
        self.y3.pack()

        self.x4 = tk.Label(self.labelframe, text="Sex")
        self.x4.pack()
        s = ['Male', 'Female']
        selected_Gender = tk.StringVar()
        self.cb = ttk.Combobox(self.frame, textvariable=selected_Gender)
        self.cb['values'] = s
        self.cb.current(1)
        self.cmb = ttk.Combobox(self.labelframe, values=s, width=37)
        self.cmb.pack()

        self.x5 = tk.Label(self.labelframe, text="Year of birth")
        self.x5.pack()
        self.y5 = tk.Entry(self.labelframe, width=40)
        self.y5.pack()

        self.x5 = tk.Label(self.labelframe, text="Type of vaccine")
        self.x5.pack()
        v = ['Pfizer', 'AstraZeneca', 'Moderna', 'J&J']
        selected_VAC = tk.StringVar()
        self.cb = ttk.Combobox(self.frame, textvariable=selected_VAC)
        self.cb['values'] = v
        self.cb.current(1)
        self.cmb2 = ttk.Combobox(self.labelframe, values=v, width=37)
        self.cmb2.pack()

        '''self.x6 = tk.Label(self.labelframe, text="Date&Time")
        self.x6.pack()
        self.y6 = tk.Entry(self.labelframe, width=40)
        self.y6.pack()
        self.y6.insert(1, 'DD/MM/YYYY HH:MM AM/PM')'''


        self.x7 = tk.Label(self.labelframe, text="Phone no")
        self.x7.pack()
        self.y7 = tk.Entry(self.labelframe, width=40)
        self.y7.pack()
        self.y7.insert(0, "05XXXXXXXX")

        self.x8 = tk.Label(self.labelframe2, text="ID")
        self.x8.pack()
        self.y8 = tk.Entry(self.labelframe2, width=40)
        self.y8.pack()

        self.x9 = tk.Label(self.labelframe2, text="statues")
        self.x9.pack()
        self.y9 = tk.Entry(self.labelframe2, width=50)
        self.y9.pack()

        self.x10 = tk.Label(self.labelframe3, text="Directory")
        self.x10.pack()
        self.y10 = tk.Entry(self.labelframe3,width=50)
        self.y10.pack()

        self.b1 = tk.Button(self.labelframe, text="submit", command=self.insert)
        self.b1.pack()
        self.b2 = tk.Button(self.labelframe2, text="Check", command=self.checkVaccination)
        self.b2.pack()
        self.b5 =tk.Button(self.labelframe3,
                           text = "Browse Files",
                           command =self.browseFiles)
        self.b5.pack()
        self.b4 = tk.Button(self.labelframe3, text="Export", command=self.export)
        self.b4.pack()
        self.b3 = tk.Button(self.labelframe3, text="Import", command=self.import1)
        self.b3.pack()



        tk.mainloop()

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))

    def import1(self):
        conn = sqlite3.connect('CCS227')
        cursor = conn.cursor()
        der = self.y10.get()
        with open(der, 'r') as f:
            reader = csv.reader(f)
            data = next(reader)
            query = 'insert into PEOPLE values ({0})'

            query = query.format(','.join('?' * len(data)))
            cursor.execute(query, data)
            for data in reader:
                cursor.execute(query, data)
            conn.commit()


        conn.commit()
        tk.messagebox.showinfo('Response', 'imported done')

    def export(self):
        conn = sqlite3.connect('CCS227')
        cursor = conn.cursor()
        der = self.y10.get()
        cursor.execute("select * from PEOPLE")

        with open(der, "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerows(cursor)
        tk.messagebox.showinfo('Response', 'exported done')

    def showAll(self):
        conn = sqlite3.connect('CCS227')
        cursor = conn.cursor()
        print("Data Inserted in the table: ")
        data = cursor.execute('''SELECT * FROM PEOPLE''')
        for row in data:
            print(str(row))

    def searchId(self):
        conn = sqlite3.connect('CCS227')
        cursor = conn.cursor()
        id = self.y1.get()
        if not id.isdigit():
            return -1
        if str(id).count("") - 1 != 10:
            return -2
        data = cursor.execute('SELECT id FROM PEOPLE WHERE ID =' + id)
        count = 0;
        for row in data:
            count += 1
        return count

    def searchIdC(self):
        conn = sqlite3.connect('CCS227')
        cursor = conn.cursor()
        id = self.y8.get()
        if not id.isdigit():
            return -1
        if str(id).count("") - 1 != 10:
            return -2
        data = cursor.execute('SELECT id FROM PEOPLE WHERE ID =' + id)
        count = 0;
        for row in data:
            count += 1
        return count

    def checkVaccination(self):
        conn = sqlite3.connect('CCS227')
        cursor = conn.cursor()
        id = self.y8.get()
        c = self.searchIdC()
        if c == -1:
            self.y9.config(bg="gray")
            tk.messagebox.showinfo("result",'number should be int')
            return
        if c == -2:
            self.y9.config(bg="gray")
            tk.messagebox.showinfo("result", 'id should be 10 digits')
            return
        if c == 0:
            self.y9.config(bg="Red")
            tk.messagebox.showinfo("result", 'Not Vaccinated')
            return
        if c == 1:
            self.y9.config(bg="Yellow")
            tk.messagebox.showinfo("result", 'Vaccinated')
            return
        if c == 2:
            self.y9.config(bg="Green")
            tk.messagebox.showinfo("result", 'Fully Vaccinated')
            return


    def insert(self):
        conn = sqlite3.connect('CCS227')
        cursor = conn.cursor()

        id = self.y1.get()
        fname = self.y2.get()
        lname = self.y3.get()
        sex = self.cmb.get()
        byear = self.y5.get()
        type = self.cmb2.get()
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M %p")
        date = now
        pnum = self.y7.get()


        if sex not in ['Male', 'Female']:
            tk.messagebox.showinfo("result", 'sex should be either Male, Female (Case senstitve)')
            return

        if not id.isdigit():
            tk.messagebox.showinfo("result", 'number should be int')
            return

        if str(id).count("") - 1 != 10:
            tk.messagebox.showinfo("result", 'id should be 10 digits')
            return


        if type not in ['Pfizer', 'AstraZeneca', 'Moderna', 'J&J']:
            tk.messagebox.showinfo("result", 'type should be either Pfizer, AstraZeneca, Moderna, J&J (Case senstitve)')
            return


        try:
            byear = int(byear)
            print(byear)
            if byear <= 1900 or byear >= 2003:
                tk.messagebox.showinfo("result", 'year of birth between 1900 and 2003')
                return
        except ValueError:
            tk.messagebox.showinfo("result", 'year of birth should be int')
            return


        if str(pnum).count("") - 1 != 10:
            tk.messagebox.showinfo("result", 'number should be 10 digits')
            return

        if not pnum.startswith('05'):
            tk.messagebox.showinfo("result", 'number should start with 05')
            return

        if not pnum.isdigit():
            tk.messagebox.showinfo("result", 'number should be int')
            return

        try:
            datetime.strptime(date, "%d/%m/%Y %H:%M %p")
        except ValueError:
            tk.messagebox.showinfo("result", 'date time format should be DD/MM/YYYY HH:MM AM/PM')
            return

        if self.searchId() > 1:
            tk.messagebox.showinfo("result", 'person is fully vaccinated')
            return



        insert_query = 'INSERT INTO PEOPLE VALUES (\'' + fname + '\', \'' + lname + '\', \'' + sex + '\', ' + str(
            id) + ' ,' + str(byear) + ', \'' + type + '\', \'' + date + '\', \'' + str(pnum) +'\')'
        cursor.execute(insert_query)
        tk.messagebox.showinfo("result", "Record inserted")
        conn.commit()
        self.showAll()
        conn.close()





gui = Project()
