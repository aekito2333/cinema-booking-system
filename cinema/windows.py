import sqlite3
import csv
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import re
import datetime as dt
from customer import *
from employee import *
import math
import time


####key down function + log in function

# open database
conn1 = sqlite3.connect('customer_login.db')
c1 = conn1.cursor()
conn2 = sqlite3.connect('employee_login.db')
c2 = conn2.cursor()
conn3 = sqlite3.connect('cinema_films.db')
c3 = conn3.cursor()
conn4 = sqlite3.connect('film_posters.db')
c4 = conn4.cursor()
conn5 = sqlite3.connect('customer_profile.db')
c5 = conn5.cursor()

LARGE_FONT = ('Verdana', 12)
MEDIAN_FONT = ('Verdana', 10)
SMALL_FONT = ('Verdana', 8)


class LoginPage(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)
        self.geometry('{}x{}'.format(820, 400))
        self.wm_title('Welcome to Song cinema!!')
        self.configure(background='white')
        self.resizable(0, 0)
        self.photo1 = tk.PhotoImage(file='cinema.gif')
        tk.Label(self, image=self.photo1, bg='white').grid(row=0, column=2, padx=5, pady=5)

        ####creat entry for username and password:
        # customer set:
        tk.Label(self, text='UserName', bg='red', fg='white').grid(row=2, column=0, sticky='E', padx=5)
        tk.Label(self, text='Password', bg='red', fg='white').grid(row=3, column=0, sticky='E', padx=5)
        self.entry0 = tk.Entry(self)
        self.entry1 = tk.Entry(self)
        self.entry0.grid(row=2, column=1, sticky='W')
        self.entry1.grid(row=3, column=1, sticky='W')

        # employee set:
        tk.Label(self, text='UserName', bg='green', fg='white').grid(row=2, column=3, sticky='E', padx=5)
        tk.Label(self, text='Password', bg='green', fg='white').grid(row=3, column=3, sticky='E', padx=5)
        self.entry2 = tk.Entry(self)
        self.entry3 = tk.Entry(self)
        self.entry2.grid(row=2, column=4, sticky='W')
        self.entry3.grid(row=3, column=4, sticky='W')

        ####creat a log in button that checks for the username/password pair
        ttk.Button(self, text="Customer login", command = self.clickCustomer).grid(row=4, column=1, sticky='w')
        ttk.Button(self, text="New customer register", command=self.registerCustomer).grid(row=5, column=1, sticky='w')
        ttk.Button(self, text="Employee login", command = self.clickEmployee).grid(row=4, column=4, sticky='w')

    #a new customer could register
    def registerCustomer(self):
        self.destroy()
        app=RegisterPage()
        app.mainloop()

    def clickCustomer(self):
            enteredCustomerUserName = self.entry0.get()
            enteredCustomerPassword = self.entry1.get()

            try:
                c1.execute("SELECT * FROM customer_login WHERE userName=?", (enteredCustomerUserName,))
                dbPassword = c1.fetchall()[0][1]

                if enteredCustomerPassword == dbPassword:#login successful
                    c5.execute("SELECT * FROM customer_profile WHERE userName=?", (enteredCustomerUserName,))
                    profile=c5.fetchall()
                    global userC
                    userC = Customer(enteredCustomerUserName,enteredCustomerPassword)
                    userC.name = profile[0][1]
                    userC.emailAddress =profile[0][2]
                    self.destroy()
                    app = CustomerHomePage()
                    app.mainloop()
                    return userC

                else:
                    tk.messagebox.showerror('error', 'Incorrect password')
                    return False
            except ValueError:
                tk.messagebox.showerror('error', 'Incorrect entry')
                return False
            except IndexError:
                tk.messagebox.showerror('error', 'Incorrect entry')
                return False

    def clickEmployee(self):
            enteredEmployeeUserName = self.entry2.get()
            enteredEmployeePassword = self.entry3.get()
            try:
                c2.execute("SELECT * FROM Employee_login WHERE userName=?", (enteredEmployeeUserName,))
                dbPassword = c2.fetchall()[0][1]
                if enteredEmployeePassword == dbPassword:
                    global userE
                    userE = dictOfEmployees.get(enteredEmployeeUserName)
                    self.destroy()
                    app = EmployeeHomePage()
                    app.mainloop()
                    return userE
                else:
                    tk.messagebox.showerror('error', 'Incorrect password')
                    return False
            except ValueError:
                tk.messagebox.showerror('error', 'Incorrect entry')
                return False
            except IndexError:
                tk.messagebox.showerror('error', 'Incorrect entry')
                return False


class RegisterPage(tk.Tk):
    def __init__(self, **kwargs):
        # initialise tkinter
        tk.Tk.__init__(self, **kwargs)
        self.geometry('{}x{}'.format(820, 450))
        self.wm_title('Welcome to Song cinema!!')
        self.configure(background='white')
        self.resizable(0, 0)
        tk.Label(self, text='Please fill in the following to register:', font=MEDIAN_FONT).grid(row=0, column=0, sticky='E', padx=5, pady=10)

        ####creat entry for username, password, email address, name:
        # customer set:
        tk.Label(self, text='UserName:', font=MEDIAN_FONT).grid(row=1, column=0, sticky='E', padx=5, pady=10)
        tk.Label(self, text='Password:', font=MEDIAN_FONT).grid(row=2, column=0, sticky='E', padx=5, pady=10)
        tk.Label(self, text='Name:', font=MEDIAN_FONT).grid(row=3, column=0, sticky='E', padx=5, pady=10)
        tk.Label(self, text='E-mail Address:', font=MEDIAN_FONT).grid(row=4, column=0, sticky='E', padx=5, pady=10)
        self.entry0 = tk.Entry(self)
        self.entry1 = tk.Entry(self)
        self.entry2 = tk.Entry(self)
        self.entry3 = tk.Entry(self)
        self.entry0.grid(row=1, column=1, sticky='W')#UserName
        self.entry1.grid(row=2, column=1, sticky='W')#Password
        self.entry2.grid(row=3, column=1, sticky='W')#Name
        self.entry3.grid(row=4, column=1, sticky='W')#E-mail Address

        # submit button
        ttk.Button(self, text="Submit",command=self.register).grid(row=5, column=1)

        # back to login page
        ttk.Button(self, text="Back to login page", command=self.backToLogin).grid(row=6, column=1, pady=10)


    def register(self):
        try:
            userName=self.entry0.get()
            password=self.entry1.get()
            name=self.entry2.get()
            emailAddress=self.entry3.get()

            #check if entry is in the correct format
            #if username is in the correct format
            if re.fullmatch(r'[a-zA-Z0-9]+', userName):
                if len(userName)<1 or len(userName)>16:
                    tk.messagebox.showerror('error', 'Username should be 1-15 characters long!')
                    return
            else:
                tk.messagebox.showerror('error', 'Username should only contain \na-z,A-Z,0-9!')
                return

            #if password is in the correct length
            if len(password)<1 or len(password)>11:
                tk.messagebox.showerror('error', 'Password should be 1-10 characters long!')
                return

            #if name is in the correct format
            if re.fullmatch(r'[a-zA-Z]+[?\-|a-zA-z_ ]*', name):
                if len(name)<1 or len(name)>31:
                    tk.messagebox.showerror('error', 'Name should be 1-30 characters long!')
                    return
            else:
                tk.messagebox.showerror('error',
                                        'Name does not follow correct format:\nonly letters, "-" and "_" allowed')
                return

            #if e-mail address is in the correct format
            if re.fullmatch(r'[a-zA-Z_\-0-9]+(.[a-zA-Z_\-0-9]+)*[\@][a-zA-Z_\-0-9]+[.][a-zA-Z_\-0-9]+[.a-zA-Z_\-0-9]*', emailAddress):
                if len(emailAddress)>100:
                    tk.messagebox.showerror('error', 'E-mail address too long\n(no more than 99 characters)')
                    return
            else:
                tk.messagebox.showerror('error', 'E-mail address does not follow correct format')
                return


            #if all 4 entries are of the correct format, check if username already exsits in DB
            c1.execute("SELECT * FROM customer_login WHERE userName=?", (userName,))
            self.a = c1.fetchall()
            if bool(self.a) == False: #returns empty list -> username available
                #creat class instance
                newCustomer=Customer(userName,password)
                newCustomer.addToDB(name,emailAddress)
                tk.messagebox.showinfo('complete','Your register is successful')
                return
            else:
                tk.messagebox.showerror('unsuccessful', 'Your user name is taken\nplease try a different one!')
                return

        except:
            pass


    def backToLogin(self):
        self.destroy()
        app=LoginPage()
        app.mainloop()


class CustomerWindows(tk.Tk):

    def __init__(self, **kwargs):
        # initialise tkinter
        tk.Tk.__init__(self, **kwargs)
        self.geometry('{}x{}'.format(820, 450))
        welcomeText = 'Welcome back! ' + userC.name
        self.wm_title(welcomeText)
        self.configure(background='white')
        self.resizable(0, 0)
        self.dateToday = dt.datetime.now()
        ttk.Button(self, text='Home Page', command=self.returnToHome, width=20).grid(row=1, column=0,padx=10, pady=15)
        ttk.Button(self, text='View films', command=self.viewFilms, width=20).grid(row=2, column=0, padx=10, pady=15)
        ttk.Button(self, text='View my profile', command=self.viewMyProfile, width=20).grid(row=3, column=0,padx=10, pady=15)
        ttk.Button(self, text='Change my profile', command=self.changeMyProfile, width=20).grid(row=4, column=0,padx=10, pady=15)
        ttk.Button(self, text='View my history', command=self.viewMyHistory, width=20).grid(row=5, column=0,padx=10, pady=15)
        ttk.Button(self, text='Make booking', command=self.makeBooking, width=20).grid(row=6, column=0,padx=10, pady=15)
        ttk.Button(self, text='Log out', command=self.logoutCustomer, width=20).grid(row=7, column=0,padx=10, pady=15)

    def returnToHome(self):
        self.destroy()
        app = CustomerHomePage()
        return app.mainloop()

    def viewFilms(self):
        self.destroy()
        app = ViewFilms()
        return app.mainloop()

    def viewMyProfile(self):
        self.destroy()
        app = ViewMyProfilePage()
        return app.mainloop()

    def changeMyProfile(self):
        self.destroy()
        app = ChangeMyProfile()
        return app.mainloop()

    def viewMyHistory(self):
        self.destroy()
        app = ViewMyHistory()
        return app.mainloop()

    def makeBooking(self):
        self.destroy()
        app = MakeBooking()
        return app.mainloop()

    def logoutCustomer(self):
        self.destroy()
        app = LoginPage()
        return app.mainloop()


class CustomerHomePage(CustomerWindows):

    def __init__(self, **kwargs):
        CustomerWindows.__init__(self, **kwargs)

        headText = userC.name + ' Home Page'
        tk.Label(self, text = headText, font = LARGE_FONT).grid(row=0, column=0)
        tk.Label(self, text='Coming soon', font=LARGE_FONT).grid(row=0, column = 1, columnspan = 4)
        self.photo1 = tk.PhotoImage(file='avengers_inf.gif')
        tk.Label(self, image=self.photo1, bg='grey').grid(row = 1, column =2, rowspan = 10, columnspan = 2, sticky = 'E',padx=50, pady=10)
        self.photo2 = tk.PhotoImage(file='spiderman.gif')
        tk.Label(self, image=self.photo2, bg='grey').grid(row = 1, column =4, rowspan = 10, columnspan = 2, sticky = 'E',padx=10, pady=10)


class ViewFilms(CustomerWindows):

    def __init__(self, **kwargs):
        CustomerWindows.__init__(self, **kwargs)
        tk.Label(self, text='Current Films', font=LARGE_FONT).grid(row=0, column=0)
        self.date = None

        ##creat a filter for date / in the form of a dropdown list##
        c3.execute('SELECT DISTINCT date FROM cinema_films ')
        filmDateList = ['Select your date here']
        for i in c3.fetchall():
            # only select date that's in the future
            datetime_filmDate = dt.datetime.strptime(i[0] + ' 23:59', '%Y-%m-%d %H:%M')
            if datetime_filmDate >= self.dateToday:
                filmDateList.append(i[0]) #list of film dates from DB
        variable = tk.StringVar(self)
        variable.set(filmDateList[0])  # default value
        dateListDropDown=tk.OptionMenu(self, variable, *filmDateList, command=self.getFilmTitle)
        dateListDropDown.grid(row=1, column=1, sticky ='we', padx=10, pady=10)
        dateListDropDown.config(width=45)

    def getFilmTitle(self, value):
        self.date = value
        try:
            c3.execute("SELECT DISTINCT filmName FROM cinema_films WHERE date=?",(value,))
            filmTitleList = ['Select your film here']

            self.poster = tk.PhotoImage(file='blank.gif')
            tk.Label(self, image=self.poster, bg='white').grid(row=1, column=2, rowspan=10, columnspan=2, sticky='E',
                                                               padx=10, pady=10)

            for i in c3.fetchall(): #List of film titles
                filmTitleList.append(i[0])

            variable = tk.StringVar(self)
            variable.set(filmTitleList[0])  # default value
            filmDetailDropDown=tk.OptionMenu(self, variable, *filmTitleList, command=self.getFilmDetail)
            filmDetailDropDown.grid(row=2,column=1,sticky='we',padx=10,pady=10)
            filmDetailDropDown.config(width=45)

        except TypeError:
            pass
        except IndexError:
            pass

    def getFilmDetail(self, value):
        try:
            # label to show the description of the film
            c4.execute("SELECT description FROM film_posters WHERE filmName=?", (value,))
            description = c4.fetchone()[0]
            tk.Label(self, text='Description: ', font=MEDIAN_FONT).grid(row=3,column=1,sticky='w', padx=10,pady=10)
            tk.Label(self, text=description, height=4, width=40, wraplength=310, font=MEDIAN_FONT, justify='left').grid(row=4,column=1, rowspan=2, sticky='w', padx=10,pady=10)

            # bring out the poster for the chosen film
            c4.execute("SELECT poster FROM film_posters WHERE filmName=?", (value,))
            posterRef = c4.fetchone()
            if bool(posterRef) != False:
                self.poster = tk.PhotoImage(file=posterRef[0])
                tk.Label(self, image=self.poster, bg='white').grid(row=1, column=2, rowspan=10, columnspan=2,
                                                                   sticky='E', padx=10, pady=10)
            else:
                self.poster = tk.PhotoImage(file='blank.gif')
                tk.Label(self, image=self.poster, bg='white').grid(row=1, column=2, rowspan=10, columnspan=2,
                                                                   sticky='E', padx=10, pady=10)
            # bring out the duration of the film
            c4.execute("SELECT duration FROM film_posters WHERE filmName=?", (value,))
            duration = str(c4.fetchone()[0])
            duration ='Duration: '+ duration+' min'
            tk.Label(self, text=duration, font=MEDIAN_FONT, justify='left', width=40).grid(row=6, column=1, sticky='w',
                                                                                            padx=10, pady=10)


            # bring out the screen time for the chosen film
            c3.execute("SELECT DISTINCT time FROM cinema_films WHERE filmName=? AND date=?", (value,self.date))
            time=''
            for i in c3.fetchall():
                time = time + i[0]+' '
            tk.Label(self, text='Screen time: '+time, font=MEDIAN_FONT, justify='left', width=40).grid(row=7,
                                                                                column=1, sticky='w', padx=10, pady=10)

        except IndexError:
            pass

        except TypeError:
            pass


class ViewMyProfilePage(CustomerWindows):

    def __init__(self, **kwargs):
        CustomerWindows.__init__(self, **kwargs)
        headText = userC.name + ' Profile'
        tk.Label(self, text = headText, font = LARGE_FONT).grid(row=0, column=0)
        try:
            profile = userC.readMyProfile()
            tk.Label(self, text='User Name:', font=MEDIAN_FONT).grid(row=2, column=1, sticky='w', padx=10, pady=10)
            tk.Label(self, text=profile[0][0], font=MEDIAN_FONT).grid(row=2, column=2, sticky='w', padx=10, pady=10)
            tk.Label(self, text='Name:', font=MEDIAN_FONT).grid(row=3, column=1, sticky='w', padx=10, pady=10)
            tk.Label(self, text=profile[0][1], font=MEDIAN_FONT).grid(row=3, column=2, sticky='w', padx=10, pady=10)
            tk.Label(self, text='E-mail Address:', font=MEDIAN_FONT).grid(row=4, column=1, sticky='w', padx=10, pady=10)
            tk.Label(self, text=profile[0][2], font=MEDIAN_FONT).grid(row=4, column=2, sticky='w', padx=10, pady=10)
        except IndexError:
            pass


class ChangeMyProfile(CustomerWindows):

    def __init__(self, **kwargs):
        CustomerWindows.__init__(self, **kwargs)
        headText = userC.name + ' Edit'
        tk.Label(self, text=headText, font=LARGE_FONT).grid(row=0, column=0)
        tk.Label(self, text='update name: ', font=MEDIAN_FONT).grid(row=2, column=1, sticky='w')
        tk.Label(self, text='update e-mail address: ', font=MEDIAN_FONT).grid(row=3, column=1, sticky='w')
        self.entry0 = tk.Entry(self)#UPDATE name
        self.entry1 = tk.Entry(self)#UPDATE e-mail address
        self.entry0.grid(row=2, column=2, sticky='W')
        self.entry1.grid(row=3, column=2, sticky='W')

        ############creat a button to save updates#################
        ttk.Button(self, text="save change", command=self.update).grid(row=5, column=2)

    def update(self):
        #check if the name follows the correct format
        if bool(self.entry0.get()) == True:
            if re.fullmatch(r'[a-zA-Z]+[?\-|a-zA-z_ ]*', self.entry0.get()):
                userC.changeMyProfile('customerName', self.entry0.get())# update name in DB
                userC.name=self.entry0.get() # update userC.name
                tk.messagebox.showinfo('complete','Name update successful')
            else:
                tk.messagebox.showerror('error', 'Name does not follow correct format : \nonly letters, "-" and "_" allowed')

        # check if the e-mail address follows the correct format
        if bool(self.entry1.get()) == True:
            if re.fullmatch(r'[a-zA-Z_\-0-9]+(.[a-zA-Z_\-0-9]+)*[\@][a-zA-Z_\-0-9]+[.][a-zA-Z_\-0-9]+[.a-zA-Z_\-0-9]*', self.entry1.get()):
                userC.changeMyProfile('EmailAddress', self.entry1.get())# update e-mail address in DB
                userC.emailAddress = self.entry1.get()
                tk.messagebox.showinfo('complete', 'E-mail address update successful')
            else:
                tk.messagebox.showerror('error', 'E-mail address does not follow correct format')


class ViewMyHistory(CustomerWindows):

    def __init__(self, **kwargs):
        CustomerWindows.__init__(self, **kwargs)
        headText = userC.name + ' History'
        try:
            self.history = userC.readHistory()
            self.len = len(self.history)
            self.totalPage = math.ceil(self.len/5)
            tk.Label(self, text=headText, font=LARGE_FONT).grid(row=0, column=0)

            #defin the titles
            tk.Label(self, text='Date', font=MEDIAN_FONT).grid(row=1, column=1, padx = 5, pady = 5)
            tk.Label(self, text='Time', font=MEDIAN_FONT).grid(row=1, column=2, padx = 5, pady = 5)
            tk.Label(self, text='Film Name', font=MEDIAN_FONT).grid(row=1, column=3, padx = 25, pady = 5)
            tk.Label(self, text='Screen', font=MEDIAN_FONT).grid(row=1, column=4, padx = 5, pady = 5)
            tk.Label(self, text='Tickets', font=MEDIAN_FONT).grid(row=1, column=5, padx = 5, pady = 5)
            tk.Label(self, text='Seats', font=MEDIAN_FONT).grid(row=1, column=6, padx = 5, pady = 5)

            ttk.Button(self, text='PrePage', command=self.pagePrevious).grid(row=7, column=4, padx=5,pady=5)
            ttk.Button(self, text='NextPage', command=self.pageNext).grid(row=7, column=5, padx=5, pady=5)


            self.page()
            tk.Label(self, text='Page '+str(userC.historyPageNumber)+' / '+str(self.totalPage), font=MEDIAN_FONT, width=15).grid(row=0, column=3, padx=5, pady=5)

        except IndexError:
            tk.messagebox.showinfo('info','You have no history.')

    def page(self):
        count = 2  # set the position of the row
        try:
            i = 5*(userC.historyPageNumber-1)
            while i < 5*userC.historyPageNumber and i < self.len:
                filmTime = dt.datetime.strptime(self.history[i][1] + ' ' + self.history[i][2], '%Y-%m-%d %H:%M')
                if filmTime > dt.datetime.now():
                    self.removalbeHistory(i,count)
                else:
                    self.fixHistory(i,count)
                i=i+1
                count=count+1

        except IndexError:
            print('Index Error')

    def removalbeHistory(self, i, count):
        tk.Label(self, text=self.history[i][1], font=MEDIAN_FONT).grid(row=count, column=1, padx=5, pady=5)  # date
        tk.Label(self, text=self.history[i][2], font=MEDIAN_FONT).grid(row=count, column=2, padx=5, pady=5)  # time
        tk.Label(self, text=self.history[i][3], font=SMALL_FONT, height=3, width=15, wraplength=110,
                 justify='left').grid(
            row=count, column=3, padx=5, pady=5)  # film name
        tk.Label(self, text=self.history[i][4], font=MEDIAN_FONT).grid(row=count, column=4, padx=5, pady=5)  # screen
        tk.Label(self, text=self.history[i][5], font=MEDIAN_FONT).grid(row=count, column=5, padx=5,
                                                                       pady=5)  # number of tickets
        tk.Label(self, text=self.history[i][6], font=SMALL_FONT, height=2, width=8, wraplength=65).grid(
            row=count, column=6, padx=5, pady=5)  # seats info

        def refreshSelf():
            userC.cancelBooking(self.history[i][3], self.history[i][1], self.history[i][2], int(self.history[i][5]),
                                self.history[i][6])  # filmName, Date, Time, Tickets, Seat

            self.destroy()
            app = ViewMyHistory()
            app.mainloop()

        ttk.Button(self, text='Delete', width=8, command=refreshSelf).grid(row=count, column=7, padx=5,
                                                                           pady=5)  # delete button

    def fixHistory(self,i, count):
        tk.Label(self, text=self.history[i][1], font=MEDIAN_FONT).grid(row=count, column=1, padx=5, pady=5)  # date
        tk.Label(self, text=self.history[i][2], font=MEDIAN_FONT).grid(row=count, column=2, padx=5, pady=5)  # time
        tk.Label(self, text=self.history[i][3], font=SMALL_FONT, height=3, width=15, wraplength=110,
                 justify='left').grid(
            row=count, column=3, padx=5, pady=5)  # film name
        tk.Label(self, text=self.history[i][4], font=MEDIAN_FONT).grid(row=count, column=4, padx=5, pady=5)  # screen
        tk.Label(self, text=self.history[i][5], font=MEDIAN_FONT).grid(row=count, column=5, padx=5,
                                                                       pady=5)  # number of tickets
        tk.Label(self, text=self.history[i][6], font=SMALL_FONT, height=2, width=8, wraplength=65).grid(
            row=count, column=6, padx=5, pady=5)  # seats info

        tk.Label(self, text='Cannot \nEdit', font=SMALL_FONT, height=2, width=8, wraplength=65).grid(
            row=count, column=7, padx=5, pady=5)  # cannot delete

    def pagePrevious(self):
        if userC.historyPageNumber>1:
            userC.historyPageNumber=userC.historyPageNumber-1
            self.destroy()
            app=ViewMyHistory()
            app.mainloop()
        else:
            tk.messagebox.showinfo('info', 'No more page available')

    def pageNext(self):
        if userC.historyPageNumber<self.totalPage:
            userC.historyPageNumber=userC.historyPageNumber+1
            self.destroy()
            app=ViewMyHistory()
            app.mainloop()
        else:
            tk.messagebox.showinfo('info','No more page available')


class MakeBooking(CustomerWindows):

    def __init__(self, **kwargs):
        self.value = None
        CustomerWindows.__init__(self, **kwargs)
        headText = userC.name + ' Booking'
        tk.Label(self, text=headText, font=LARGE_FONT).grid(row=0, column=0)
        self.poster = tk.PhotoImage(file='blank.gif')
        tk.Label(self, image=self.poster, bg = 'white').grid(row=1, column=2, rowspan=10, columnspan=2, sticky='E', padx=50, pady=10)

        ##provide a dropdown list for filmName##
        c3.execute("SELECT DISTINCT filmName FROM cinema_films ")
        filmTitleList = ['Select your film here']
        for i in c3.fetchall():
            filmTitleList.append(i[0]) #list of filmName from DB
        variable = tk.StringVar(self)
        variable.set(filmTitleList[0])  # default value
        filmNameDropDown=tk.OptionMenu(self, variable, *filmTitleList, command=self.getFilmName)
        filmNameDropDown.grid(row=2, column=1, sticky='we', padx=10, pady=10)
        filmNameDropDown.config(width=45)

    def getFilmName(self, value):
        userC.selectFilm = value
        ##provide a drop down list for filmDate upon the selection of filmName##
        self.refreshPageForDate()

    def refreshPageForDate(self):
        #bring out the poster for the chosen film#
        c4.execute("SELECT poster FROM film_posters WHERE filmName=?", (userC.selectFilm,))
        posterRef = c4.fetchone()
        if bool(posterRef) != False:
            self.poster = tk.PhotoImage(file=posterRef[0])
            tk.Label(self, image=self.poster, bg = 'white').grid(row=1, column=2, rowspan=10, columnspan=2, sticky='E', padx=50, pady=10)
        else:
            self.poster = tk.PhotoImage(file='blank.gif')
            tk.Label(self, image=self.poster, bg = 'white').grid(row=1, column=2, rowspan=10, columnspan=2, sticky='E', padx=50, pady=10)


        #creat a dropdown list for the date#
        filmDateList = ['Select date']
        c3.execute("SELECT DISTINCT date FROM cinema_films WHERE filmName=? ", (userC.selectFilm,))
        self.dateToday = dt.datetime.now() #update current date/time
        for i in c3.fetchall():
            #only select date that's in the future
            datetime_filmDate = dt.datetime.strptime(i[0]+' 23:59', '%Y-%m-%d %H:%M')
            if datetime_filmDate >= self.dateToday:
                filmDateList.append(i[0])

        variable = tk.StringVar(self)
        variable.set(filmDateList[0])  # default value

        filmDateDropDown=tk.OptionMenu(self, variable, *filmDateList, command=self.getFilmDate)
        filmDateDropDown.grid(row=3, column=1, padx=10, pady=10)
        filmDateDropDown.config(width=15)

    def getFilmDate(self, value):
        userC.selectDate = value # type = string
        self.refreshPageForTime()
        return userC.selectDate

    def refreshPageForTime(self):
        # creat a dropdown list for the time upon selected film and date#
        filmTimeList = ['Time ']

        # if the date selected is today, then only display future timing
        try:
            self.dateToday = dt.datetime.now() #update current date/time
            if self.dateToday >= dt.datetime.strptime(userC.selectDate +' 00:00', '%Y-%m-%d %H:%M'):
                #print(self.dateToday)
                #print(userC.selectDate)
                c3.execute("SELECT DISTINCT time FROM cinema_films WHERE filmName=? AND date=? ", (userC.selectFilm, userC.selectDate))

                ##creat a dropdown list for the time##
                for i in c3.fetchall():
                    # only select time that's in the future
                    datetime_filmTime = dt.datetime.strptime(userC.selectDate+' '+i[0], '%Y-%m-%d %H:%M')
                    if datetime_filmTime >= self.dateToday:
                        filmTimeList.append(i[0])
            else:
                #the date selected is a future date, in which case display all possible time for selected film
                c3.execute("SELECT DISTINCT time FROM cinema_films WHERE filmName=? AND date=? ", (userC.selectFilm, userC.selectDate))
                for i in c3.fetchall():
                    filmTimeList.append(i[0])


            variable = tk.StringVar(self)
            variable.set(filmTimeList[0])  # default value

            timeDropDown=tk.OptionMenu(self, variable, *filmTimeList, command=self.getFilmTime)
            timeDropDown.grid(row=4, column=1, padx=10, pady=10)
            timeDropDown.config(width=8)

        except ValueError:
            tk.messagebox.showerror('error', 'Please select a film/date first')

    def getFilmTime(self, value):
        #print('UserC selected time: ', value)
        userC.selectTime = value # type = string
        self.refreshPageForTickets()

    def refreshPageForTickets(self):
        #buy 1-5 tickets
        numberList=['Ticket']
        for i in range(0,5):
            numberList.append('    {}    '.format(i+1))

        variable = tk.StringVar(self)
        variable.set(numberList[0])  # default value
        ticketDropDown=tk.OptionMenu(self, variable, *numberList, command=self.getTicktes)
        ticketDropDown.grid(row=5, column=1, padx=10, pady=10)
        ticketDropDown.config(width=6)

    def getTicktes(self, value):
        #print('UserC number of tickets: ', value)
        userC.selectNumberTickets = value
        self.dummyCollect()

    def dummyCollect(self):

        #only support payment and collect tickets at door atm
        #maybe card payment and e-mail ticket one day?

        dummyCollectAtDoor=('Payment and collect tickets at door',)

        variable = tk.StringVar(self)
        variable.set(dummyCollectAtDoor[0])  # default value
        tk.OptionMenu(self, variable, *dummyCollectAtDoor).grid(row=6, column=1, padx=10, pady=10)

        ##submit button
        ttk.Button(self, text='Submit', command=self.submitButton, width=20).grid(row=7, column=1, padx=10, pady=10)

    def submitButton(self):
        try:

            #check it the time has expired since selection
            self.dateToday = dt.datetime.now()
            filmTime = dt.datetime.strptime(userC.selectDate + ' ' +userC.selectTime, '%Y-%m-%d %H:%M')
            if filmTime > self.dateToday:
                # check if the number of seats is avaliable
                c3.execute("SELECT tickets FROM cinema_films WHERE filmName=? AND date=? AND time=? ",
                                         (userC.selectFilm, userC.selectDate, userC.selectTime))

                ticketsLeft = c3.fetchall()[0][0]

                if ticketsLeft >= int(userC.selectNumberTickets):
                    global newTicketsLeft
                    newTicketsLeft = ticketsLeft - int(userC.selectNumberTickets)

                    self.destroy()
                    app = SelectSeats()
                    app.mainloop()

                else:
                    tk.messagebox.showerror('error', 'Sorry, there are {} tickets left for this film'.format(ticketsLeft))

            else:
                tk.messagebox.showerror('error', 'Sorry, you can no longer book this film')
        except ValueError:
            pass

        # next select seating


class SelectSeats(CustomerWindows):
    def __init__(self, **kwargs):
        CustomerWindows.__init__(self, **kwargs)
        headText = 'Choose'+userC.selectNumberTickets+'seats please:\n(A is front and C is back)'
        tk.Label(self, text=headText, font=LARGE_FONT).grid(row=0, column=0)

        ###booked seats will be recorded in DB as string###
        c3.execute("SELECT seating FROM cinema_films WHERE filmName=? AND date=? AND time=? ", (userC.selectFilm, userC.selectDate, userC.selectTime))
        a = str(c3.fetchall()[0][0]) #recall booked seats

        ##creat label for booked seats and button for available seats###
        self.selectedSeat = []

        x = 1  # define row position
        seatButtons = {}
        for i in ['A', 'B', 'C']:
            x = x + 1
            y = 2  # define column position
            for j in range(5):
                y = y + 1
                # print(x,y)
                label = i + str(j)  # seats are label in A0,A1 etc
                if label in a:
                    self.seatLabel(label,x,y)

                else:
                    self.seatButton(label,x,y)

        #this Button catches the seats selected
        ttk.Button(self, text='Submit', width=8, command=self.checkSeat).grid(row=6, column=6)
        ##this Button to refresh the page
        ttk.Button(self, text='Refresh', width=8, command=self.refreshSelf).grid(row=6, column=4)





    ##Initiate seats##
    def seatButton(self, label, x,y):
        def returnLabel():
            if label not in self.selectedSeat:
                self.selectedSeat.append(label)
            else:
                #print('double select')
                tk.messagebox.showwarning('warning','You cannot select the same seat twice')

        ttk.Button(self, text=label, width=5, command=returnLabel).grid(row=x, column=y)

    def seatLabel(self,label,x,y):
        tk.Label(self, text=label, font=MEDIAN_FONT).grid(row=x, column=y)

    def checkSeat(self):
        if len(self.selectedSeat) ==  int(userC.selectNumberTickets):
            c3.execute("SELECT screen FROM cinema_films WHERE filmName=? AND date=? AND time=? ",
                       (userC.selectFilm, userC.selectDate, userC.selectTime))
            userC.screen = c3.fetchone()[0]

            tk.messagebox.showinfo('Booking complete', '''You have booked:\n{},
                                    \ndate: {},
                                    \ntime: {},
                                    \nscreen: {},
                                    \nseats: {}'''.format(userC.selectFilm, userC.selectDate,
                                                          userC.selectTime,
                                                          userC.screen,
                                                          self.selectedSeat))
            userC.makeBooking(newTicketsLeft, self.selectedSeat)
            self.destroy()
            app=MakeBooking()
            app.mainloop()

        elif len(self.selectedSeat) < int(userC.selectNumberTickets):
            tk.messagebox.showerror('error', 'You did not select enough seats, \nplease select more and submit')
        else:
            tk.messagebox.showerror('error','You have selected too many seats, \nplease refresh the page and try again')

    def refreshSelf(self):
        self.destroy()
        self.selectedSeat=[]
        app = SelectSeats()
        app.mainloop()


##################################################################################################################


class EmployeeWindows(tk.Tk):

    def __init__(self, **kwargs):
        # initialise tkinter
        tk.Tk.__init__(self, **kwargs)
        self.geometry('{}x{}'.format(820, 400))
        self.wm_title('Song Cinema Employee Window')
        self.configure(background='white')
        self.resizable(0, 0)
        ttk.Button(self, text='Home Page', command=self.returnToHome, width=20).grid(row=1, column=0,padx=10, pady=15)
        ttk.Button(self, text='View Film', command=self.viewFilmPage, width=20).grid(row=2, column=0, padx=10, pady=15)
        ttk.Button(self, text='Add Film', command=self.adddFilm, width=20).grid(row=3, column=0,padx=10, pady=15)
        ttk.Button(self, text='Manage Seating', command=self.manageSeating, width=20).grid(row=4, column=0,padx=10, pady=15)
        ttk.Button(self, text='Export Film Details', command=self.exportFilmDetails, width=20).grid(row=5, column=0,padx=10, pady=15)
        ttk.Button(self, text='Log out', command =self.logoutEmployee, width=20).grid(row=6, column=0,padx=10, pady=15)

    def returnToHome(self):
        self.destroy()
        app = EmployeeHomePage()
        return app.mainloop()

    def viewFilmPage(self):
        self.destroy()
        app = ViewFilm()
        return app.mainloop()

    def adddFilm(self):#this naming is deliberate
        self.destroy()
        app = AddFilmPage()
        return app.mainloop()

    def manageSeating(self):
        self.destroy()
        app = ManageSeating()
        return app.mainloop()

    def exportFilmDetails(self):
        self.destroy()
        app = ExportFilmDetails()
        return app.mainloop()

    def logoutEmployee(self):
        self.destroy()
        app = LoginPage()
        return app.mainloop()


class EmployeeHomePage(EmployeeWindows):

    def __init__(self, **kwargs):
        EmployeeWindows.__init__(self, **kwargs)
        welcomeText = 'Have a nice day! ' + userE.userName
        dateToday = dt.datetime.now()
        dateToday = dateToday.strftime("%Y-%m-%d")
        tk.Label(self, text=dateToday, font=MEDIAN_FONT).grid(row=0, column=2, sticky='E')
        tk.Label(self, text=welcomeText, font=LARGE_FONT).grid(row=0, column=0)
        self.photo1 = tk.PhotoImage(file='cat.gif')
        tk.Label(self, image=self.photo1, bg='grey').grid(row=1, column=1, rowspan=10, columnspan=2, sticky='E')


class ViewFilm(EmployeeWindows):
    def __init__(self, **kwargs):
        EmployeeWindows.__init__(self, **kwargs)
        tk.Label(self, text='Films and Seating', font=LARGE_FONT).grid(row=0, column=0)
        self.date = None
        self.dateToday = dt.datetime.now()

        try:
            ##creat a filter for date / in the form of a dropdown list##
            c3.execute('SELECT DISTINCT date FROM cinema_films ')
            filmDateList = ['Select your date here']
            for i in c3.fetchall():
                # only select date that's in the future
                datetime_filmDate = dt.datetime.strptime(i[0] + ' 23:59', '%Y-%m-%d %H:%M')
                if datetime_filmDate >= self.dateToday:
                    filmDateList.append(i[0])  # list of film dates from DB
            variable = tk.StringVar(self)
            variable.set(filmDateList[0])  # default value
            fileTitleDropDown=tk.OptionMenu(self, variable, *filmDateList, command=self.getFilmTitle)#.grid(row=1,
            fileTitleDropDown.grid(row=1, column=1, sticky='we', padx=10, pady=10)
            fileTitleDropDown.config(width=45)
        except TypeError:
            pass

    def getFilmTitle(self, value):
        self.date = value
        try:
            c3.execute("SELECT DISTINCT filmName FROM cinema_films WHERE date=?", (value,))
            filmTitleList = ['Select your film here']

            self.poster = tk.PhotoImage(file='blank.gif')
            tk.Label(self, image=self.poster, bg='white').grid(row=1, column=2, rowspan=10, columnspan=2, sticky='E',
                                                               padx=50, pady=10)

            for i in c3.fetchall():  # List of film titles
                filmTitleList.append(i[0])

            variable = tk.StringVar(self)
            variable.set(filmTitleList[0])  # default value
            filmDetailDropDown=tk.OptionMenu(self, variable, *filmTitleList, command=self.getFilmDetail)
            filmDetailDropDown.grid(row=2, column=1, sticky='we',padx=10, pady=10)
            filmDetailDropDown.config(width=45)
        except TypeError:
            pass

    def getFilmDetail(self, value):
        try:
            # label to show the description of the film
            c4.execute("SELECT description FROM film_posters WHERE filmName=?", (value,))
            description = c4.fetchone()[0]
            #tk.Label(self, text='Description: ', font=MEDIAN_FONT).grid(row=3, column=1, sticky='w', padx=10, pady=10)
            tk.Label(self, text='Description: '+description, height=6, width=40, wraplength=310, font=MEDIAN_FONT, justify='left').grid(
                row=3, rowspan=2, column=1, sticky='w', padx=10, pady=10)

            # bring out the poster for the chosen film
            c4.execute("SELECT poster FROM film_posters WHERE filmName=?", (value,))
            posterRef = c4.fetchone()
            if bool(posterRef) != False:
                self.poster = tk.PhotoImage(file=posterRef[0])
                tk.Label(self, image=self.poster, bg='white').grid(row=1, column=2, rowspan=10, columnspan=2,
                                                                   padx=10, pady=10)
            else:
                self.poster = tk.PhotoImage(file='blank.gif')
                tk.Label(self, image=self.poster, bg='white').grid(row=1, column=2, rowspan=10, columnspan=2,
                                                                    padx=10, pady=10)
            # bring out the duration of the film
            c4.execute("SELECT duration FROM film_posters WHERE filmName=?", (value,))
            duration = str(c4.fetchone()[0])
            duration = 'Duration: ' + duration + ' min'
            tk.Label(self, text=duration, font=MEDIAN_FONT, justify='left', width=40).grid(row=5, column=1, sticky='w',
                                                                                           padx=10, pady=10)

            # bring out the screen time for the chosen film
            c3.execute("SELECT DISTINCT time FROM cinema_films WHERE filmName=? AND date=?", (value, self.date))
            time = ''
            for i in c3.fetchall():
                time = time + i[0] + ' '
            tk.Label(self, text='Screen time: ' + time, font=MEDIAN_FONT, justify='left', width=40).grid(row=6,
                                                         column=1,sticky='w',padx=10,pady=10)

        except IndexError:
            pass

        except TypeError:
            pass


class AddFilmPage(EmployeeWindows):

    def __init__(self, **kwargs):
        EmployeeWindows.__init__(self, **kwargs)
        tk.Label(self, text='Add Film Page', font=MEDIAN_FONT).grid(row=0, column=2, sticky='E')

        tk.Label(self, text='Film Name (Max 45 char)', font=MEDIAN_FONT).grid(row=1, column=1, sticky='w')
        tk.Label(self, text='Duration (min)', font=MEDIAN_FONT).grid(row=1, column=3, sticky='w')
        tk.Label(self, text='Begin Date (20YY-MM-DD)', font=MEDIAN_FONT).grid(row=2, column=1, sticky='w')
        tk.Label(self, text='End Date (20YY-MM-DD)', font=MEDIAN_FONT).grid(row=2, column=3, sticky='w')
        tk.Label(self, text='Time (HH:MM, separate by ,)', font=MEDIAN_FONT).grid(row=3, column=1, sticky='w')
        tk.Label(self, text='Screen (1,2)', font=MEDIAN_FONT).grid(row=3, column=3, sticky='w')
        tk.Label(self, text='Poster ( .gif)', font=MEDIAN_FONT).grid(row=4, column=3, sticky='w')
        tk.Label(self, text='Number of Tickets (Max 15)', font=MEDIAN_FONT).grid(row=4, column=1, sticky='w') #number of tickets available #Max 15
        tk.Label(self, text='Description (Max 150 char)', font=MEDIAN_FONT).grid(row=5, column=1, sticky='w')

        self.entryFilmName = tk.Entry(self)
        self.entryDuration = tk.Entry(self)
        self.entryBeginDate = tk.Entry(self)
        self.entryEndDate = tk.Entry(self)
        self.entryScreenTime = tk.Entry(self)
        self.entryScreen = tk.Entry(self)
        self.entryPoster = tk.Entry(self)
        self.entryNumberTickets = tk.Entry(self)
        self.entryDescription = tk.Entry(self)

        self.entryFilmName.grid(row=1, column=2, sticky='w')
        self.entryDuration.grid(row=1, column=4, sticky='w')
        self.entryBeginDate.grid(row=2, column=2, sticky='w')
        self.entryEndDate.grid(row=2, column=4, sticky='w')
        self.entryScreenTime.grid(row=3, column=2, sticky='w')
        self.entryScreen.grid(row=3, column=4, sticky='w')
        self.entryPoster.grid(row=4, column=4, sticky='w')
        self.entryNumberTickets.grid(row=4, column=2, sticky='w')
        self.entryDescription.grid(row=6, column=1, sticky='w', padx=10)

        ttk.Button(self, text="Submit", command=self.addFilm).grid(row=7, column=2,sticky='w')
        ttk.Button(self, text="Check screen availability", command=self.checkAvailability).grid(row=7, column=1, sticky='w')

    #check the format of all Entry
    def checkEntry(self):
        try:
            self.enteredFilmName=self.entryFilmName.get()
            self.enteredDuration=math.ceil(float(self.entryDuration.get()))#convert to float and take ceiling

            self.enteredBeginDate=self.entryBeginDate.get()
            # Check date in valid format
            if re.fullmatch(r'20[0-9][0-9]-[012][0-9]-[0123][0-9]', self.enteredBeginDate):
                pass
            else:
                tk.messagebox.showerror('error','Begin Date is not of the correct format.')
                return False
            self.beginDate=self.enteredBeginDate.split('-') #[yyyy,mm,dd]

            self.enteredEndDate=self.entryEndDate.get()
            # Check date in valid formad
            if re.fullmatch(r'20[0-9][0-9]-[012][0-9]-[0123][0-9]', self.enteredEndDate):
                pass
            else:
                tk.messagebox.showerror('error', 'End Date is not of the correct format.')
                return False
            self.endDate = self.enteredEndDate.split('-') #[yyyy,mm,dd]
            self.enteredScreenTime=self.entryScreenTime.get()
            self.screenTime=self.enteredScreenTime.split(',') #list of times
            self.enteredScreen=self.entryScreen.get()
            self.enteredPoster=self.entryPoster.get()
            self.enteredNumberTickets=self.entryNumberTickets.get()
            self.enteredDescription=self.entryDescription.get()
        except ValueError:
            tk.messagebox.showerror('error','Invalid entry')
            return False

        #Check title
        if len(self.enteredFilmName)>45 or len(self.enteredFilmName)<1:
            tk.messagebox.showerror('error', 'Invalid film name')
            return False

        #Check description
        if len(self.enteredDescription)>150 or len(self.enteredDescription)<1:
            tk.messagebox.showerror('error', 'Invalid film description')
            return False

        #Check poster address
        if bool(re.fullmatch('[a-zA-Z_0-9]+.gif',self.enteredPoster))==False:
            tk.messagebox.showerror('error', 'Poster file not of\nthe correct format')
            return False
        else:
            try:
                tk.PhotoImage(file=self.enteredPoster)
            except:
                tk.messagebox.showerror('error','gif not found in\ncurrent folder')
                return False

        #Check number of ticket
        try:
            if int(self.enteredNumberTickets)>0 and int(self.enteredNumberTickets)<16:
                pass
            else:
                tk.messagebox.showerror('error', 'Invalid entry for ticket number')
                return False
        except ValueError:
            tk.messagebox.showerror('error', 'Invalid entry for ticket number')
            return False

        #Check duration is +ve and less than 400
        if self.enteredDuration<0 or self.enteredDuration>400:
            tk.messagebox.showerror('error', 'Invalid film duration\n(0<duration<400)')
            return False

        #Check valid screen
        if self.enteredScreen=='1' or self.enteredScreen=='2':
            pass
        else:
            tk.messagebox.showerror('error', 'Invalid screen\n("1"or"2")')
            return False

        #Check in correct format and valid time
        for i in self.screenTime:
            try:
                timeDummy = dt.datetime.strptime(i, '%H:%M')#check if time is in correct format
                endOfDay = dt.datetime.strptime('23:59', '%H:%M')
                diff = endOfDay-timeDummy#check if the film runs over 00:00
                if diff.total_seconds()/60 > self.enteredDuration:
                    pass
                else:
                    tk.messagebox.showerror('error', 'This film runs over to the next day\nplease adjust screen time')
                    return False

            except ValueError:
                tk.messagebox.showerror('error', 'Invalid time/format')
                return False

        #Check endDate is in future of beginDate
        try:
            self.startDate = dt.date(int(self.beginDate[0]), int(self.beginDate[1]), int(self.beginDate[2]))
            self.endDate = dt.date(int(self.endDate[0]),int(self.endDate[1]),int(self.endDate[2]))
            self.days = self.endDate-self.startDate
            if self.startDate > self.endDate:
                tk.messagebox.showerror('error', 'Begin Date is after End Date!')
                return False
            else:
                return True

        except IndexError:
            tk.messagebox.showerror('error', 'Invalid date entry, please check you\nhave followed the correct format.')
            return False
        except ValueError:
            tk.messagebox.showerror('error', 'Invalid date entry, please check you\nhave followed the correct format.')
            return False


    def checkAvailability(self):
        if self.checkEntry()==True:
            #pass into function self.startDate, self.days #all in datetime type
            #pass in self.enteredScreen(str) self.screenTime(list of str) self.enteredDuration(int)
            result=userE.checkScreenAvailability(self.enteredScreen, self.startDate, self.days, self.enteredDuration, *self.screenTime)
            # screen, startDate, endDate, days, duration, *screenTime
            if bool(result)==True:
                tk.messagebox.showwarning('warning','Current film overlaps with existing film\nsee "screen time overlap dump.txt" for detail.')
            else:
                tk.messagebox.showinfo('Info','No overlap in schedule has been found.')








        else:
            tk.messagebox.showerror('Error', 'Please correct entry and submit again')


    def addFilm(self):
        if self.checkEntry()==True:
            try:
                for x in range(0, self.days.days + 1):
                        self.filmDate = self.startDate + dt.timedelta(x)
                        for y in self.screenTime: #different screen time
                            film = {'filmName': self.enteredFilmName,
                                    'description': self.enteredDescription,
                                    'duration': self.enteredDuration,
                                    'date' : str(self.filmDate),
                                    'time' : y,
                                    'screen' : self.enteredScreen,
                                    'tickets': int(self.enteredNumberTickets),
                                    'seating' : '',
                                    'poster': self.enteredPoster}

                            userE.addFilms(**film) #add film to DB
                tk.messagebox.showinfo('Complete', 'Film successfully added! ')
                self.destroy()
                app=AddFilmPage()
                app.mainloop()
            except:
                tk.messagebox.showerror('Error', 'An unexpected error has occurred\nplease check your entries and try again')
        else:
            tk.messagebox.showerror('Error', 'Please correct entry and submit again')


class ManageSeating(EmployeeWindows):
    def __init__(self, **kwargs):
        EmployeeWindows.__init__(self, **kwargs)
        tk.Label(self, text='Manage Seating', font=MEDIAN_FONT).grid(row=0, column=2, sticky='E')

        #Make a entry for date
        tk.Label(self, text='Enter the date here: 20YY-MM-DD', font=MEDIAN_FONT).grid(row=1, column=2, columnspan=2, sticky='E')
        self.entryDate = tk.Entry(self)
        self.entryDate.grid(row=2, column=2, sticky='w')
        ttk.Button(self, text="Submit", command=self.findTitle).grid(row=2, column=3)

    def findTitle(self):
        userE.date = self.entryDate.get()
        try:
            if bool(re.fullmatch('20[0-9][0-9]-[01][0-9]-[0-3][0-9]', userE.date)) == True:
                filmList = ['Select your film here']
                c3.execute('SELECT DISTINCT filmName FROM cinema_films WHERE date=?',(userE.date,))
                a=c3.fetchall()
                if bool(a)==True:
                    for i in a:
                        filmList.append(i[0])
                    variable = tk.StringVar(self)
                    variable.set(filmList[0])  # default value
                    filmTimeDropDown=tk.OptionMenu(self, variable, *filmList, command=self.getFilmTime)
                    filmTimeDropDown.grid(row=3, column=2, columnspan=2, sticky='we', padx=20, pady=10)
                    filmTimeDropDown.config(width=25)
                else:
                    tk.messagebox.showerror('error','No film found for the entered date.\nPlease retry with a different date!')
            else:
                tk.messagebox.showerror('error', 'Entry is not of the correct format!')

        except IndexError:
            pass

    def getFilmTime(self,value):
        if value == 'Select your film here':
            pass
        else:
            userE.filmName=value
            tk.Label(self, text='Select film time', font=MEDIAN_FONT).grid(row=4, column=2, sticky='E')
            self.destroy()
            app=ViewSeats()
            app.mainloop()


class ViewSeats(EmployeeWindows):
    def __init__(self, **kwargs):
        EmployeeWindows.__init__(self, **kwargs)
        titleLabel=tk.Label(self, text='Manage Seating for '+userE.filmName, font=MEDIAN_FONT)
        titleLabel.grid(row=0, column=1, columnspan=7, sticky='w', padx=10, pady=10)
        titleLabel.config(width=60)

        #used for counting
        self.availableSeats = 0
        self.bookedSteats = 0

        tk.Label(self, text='Select time: ', font=MEDIAN_FONT).grid(row=1, column=1, sticky='w', padx=10, pady=10)
        timeList=['Time']
        c3.execute('SELECT DISTINCT time FROM cinema_films WHERE date=? AND filmName=?', (userE.date,userE.filmName))
        for i in c3.fetchall():
            timeList.append(i[0])
        variable = tk.StringVar(self)
        variable.set(timeList[0])  # default value
        getSeatDropDown=tk.OptionMenu(self, variable, *timeList, command=self.getSeats)
        getSeatDropDown.grid(row=1, column=2, columnspan=6, sticky='we', padx=10, pady=10)

    def getSeats(self,value):
        userE.time=value
        try:
            ###booked seats will be recorded in DB as string###
            c3.execute("SELECT seating FROM cinema_films WHERE filmName=? AND date=? AND time=? ",
                       (userE.filmName, userE.date, userE.time))
            a = str(c3.fetchall()[0][0])  # recall booked seats

            #label for the location of the screen
            tk.Label(self, text='Screen', font=MEDIAN_FONT).grid(row=2, column=3, sticky='we', columnspan=5, padx=10, pady=10)

            ##creat label for booked seats and button for available seats###
            self.selectedSeat = []


            x = 2 # define row position
            for i in ['A', 'B', 'C']:
                x = x + 1
                y = 2  # define column position
                for j in range(5):
                    y = y + 1
                    label = i + str(j)  # seats are label in A0,A1 etc
                    if label in a:
                        tk.Label(self, text=label, font=MEDIAN_FONT, bg='red').grid(row=x, column=y,padx=5,pady=5)
                        self.bookedSteats=self.bookedSteats+1

                    else:
                        tk.Label(self, text=label, font=MEDIAN_FONT, bg='green').grid(row=x, column=y,padx=5,pady=5)
                        self.availableSeats=self.availableSeats+1

            tk.Label(self, text='colour code:\ngreen=available\nred=not available', font=SMALL_FONT).grid(row=6, column=1, padx=5, pady=5,sticky='w')
            self.getTicketNumber()

        except IndexError:
            pass

        except TypeError:
            pass

    def getTicketNumber(self):
        try:
            ###booked seats will be recorded in DB as string###
            c3.execute("SELECT tickets FROM cinema_films WHERE filmName=? AND date=? AND time=? ",
                       (userE.filmName, userE.date, userE.time))
            a = str(c3.fetchall()[0][0])  # recall number of tickets left
            tk.Label(self, text='Tickets left:'+a, font=MEDIAN_FONT).grid(row=2, column=1, padx=5, pady=5, sticky='w')
            tk.Label(self, text='Available seats:\n'+str(self.availableSeats), font=SMALL_FONT).grid(row=3, column=1, padx=5, pady=5, sticky='w')
            tk.Label(self, text='Booked seats:\n'+str(self.bookedSteats), font=SMALL_FONT).grid(row=4, column=1, padx=5, pady=5, sticky='w')


        except IndexError:
            pass

        except TypeError:
            pass

        return


class ExportFilmDetails(EmployeeWindows):

    def __init__(self, **kwargs):
        EmployeeWindows.__init__(self, **kwargs)
        tk.Label(self, text='Export Film Details', font=MEDIAN_FONT).grid(row=0, column=2, sticky='E')
        tk.Label(self, text='Enter the file name', font=MEDIAN_FONT).grid(row=1, column=2, sticky='E')
        self.entryFileName = tk.Entry(self)
        self.entryFileName.grid(row=2, column=2, sticky='w')
        tk.Label(self, text='.csv', font=MEDIAN_FONT, bg='white').grid(row=2, column=3, sticky='w')
        ttk.Button(self, text="Submit", command=self.export).grid(row=3, column=2)

    def export(self):
        try:
            fileName = self.entryFileName.get()
            if re.fullmatch(r'[a-zA-Z_0-9]+',fileName):
                if len(fileName)<30:
                    userE.exportList(**{'exportFileName':fileName})
                    tk.messagebox.showinfo('Complete','File successfully exported to csv')
                else:
                    tk.messagebox.showerror('error', 'File name should be less than 30 char long')
            else:
                tk.messagebox.showerror('error', 'Illegal characters in file name')
        except ValueError:
            print('Value Error raised trying to export film list')




if __name__ == "__main__":

    app = LoginPage()
    app.mainloop()