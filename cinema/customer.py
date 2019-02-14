import sqlite3
import tkinter
import sys

##############set up DB for customer login###############
conn= sqlite3.connect('customer_login.db')
#conn= sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS customer_login (
            userName text, password text)""")
conn.commit()
conn.close()

##############set up DB for customer profile###############
conn= sqlite3.connect('customer_profile.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS customer_profile (
            userName text,
            customerName text,
            EmailAddress text)""")
conn.commit()
conn.close()

##############set up DB for customer profile###############
conn= sqlite3.connect('customer_history.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS customer_history (
            userName text,
            date text,
            time text,
            filmName text,
            screen text,
            numberOfTickets text,
            seat text)""")

###set some past history for user TonyStark for demo purpose###
c.execute("INSERT INTO customer_history VALUES (?,?,?,?,?,?,?)",('TonyStark', '2016-12-31',
                                '09:00', 'Ironman 2', '1', '2', 'A3,A4'))

c.execute("INSERT INTO customer_history VALUES (?,?,?,?,?,?,?)",('TonyStark', '2017-09-30',
                                '12:00', 'Captain America: Winter soldier', '2', '3', 'B3,B4,B5'))

c.execute("INSERT INTO customer_history VALUES (?,?,?,?,?,?,?)",('TonyStark', '2017-06-30',
                                '12:00', 'Star Trek', '2', '3', 'A0,A1,A2'))

c.execute("INSERT INTO customer_history VALUES (?,?,?,?,?,?,?)",('TonyStark', '2017-03-30',
                                '16:00', 'Black Mirror', '2', '3', 'B3,B4,B5'))

c.execute("INSERT INTO customer_history VALUES (?,?,?,?,?,?,?)",('TonyStark', '2016-02-05',
                                '09:00', 'Hulk', '1', '1', 'B3'))

c.execute("INSERT INTO customer_history VALUES (?,?,?,?,?,?,?)",('TonyStark', '2017-10-09',
                                '12:30', 'Captain America: Civil War', '2', '1', 'B5'))


conn.commit()
conn.close()
###########################################################
#connect to film database
connFilm = sqlite3.connect('cinema_films.db')
filmDB = connFilm.cursor()


# Build a class for customer#
class Customer:

    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
        self.selectFilm = 'undefined_song_cinema'
        self.selectDate = 'undefined_song_cinema'
        self.selectTime = None
        self.selectNumberTickets = None
        self.screen = None
        self.selectSeat = None
        self.historyPageNumber = 1 #used to flip the history page

        # import the database
        self.customerLogin = sqlite3.connect('customer_login.db')
        self.loginDB = self.customerLogin.cursor()

        self.customerProfile = sqlite3.connect('customer_profile.db')
        self.profileDB = self.customerProfile.cursor()

        self.customerHistory = sqlite3.connect('customer_history.db')
        self.historyDB = self.customerHistory.cursor()

        self.booking = sqlite3.connect('cinema_films.db')
        self.bookingDB = self.booking.cursor()

    def addToDB(self, name, emailAddress):
        self.name=name
        self.emailAddress=emailAddress
        # check if username already exsits in DB
        self.loginDB.execute("SELECT * FROM customer_login WHERE userName=?", (self.userName,))
        a = self.loginDB.fetchall()
        if bool(a) == False:
            self.loginDB.execute("INSERT INTO customer_login VALUES (?, ?)",(self.userName, self.password))
            self.profileDB.execute("INSERT INTO customer_profile VALUES (?, ?, ?)", (self.userName, self.name, self.emailAddress))
            self.customerLogin.commit()
            self.customerProfile.commit()

    # read user profile
    def readMyProfile(self):
        self.profileDB.execute("SELECT * FROM customer_profile WHERE userName=?", (self.userName,))
        a = self.profileDB.fetchall()
        if bool(a) == True:
            return a
        else:
            raise IndexError

    # instance method for changing user profile
    def changeMyProfile(self, title, changeTo):

        #change customer name
        if title == 'customerName':
            with self.customerProfile:
                self.profileDB.execute("""UPDATE customer_profile SET customerName = ?
                                        WHERE userName = ?""", (changeTo, self.userName))
                self.customerProfile.commit()

        # change email address
        elif title == 'EmailAddress':
            with self.customerProfile:
                self.profileDB.execute("""UPDATE customer_profile SET EmailAddress = ?
                                         WHERE userName = ?""", (changeTo, self.userName))
                self.customerProfile.commit()

    def makeBooking(self, newTicketNumber, seatList):
        #get the screen number from DB
        self.bookingDB.execute("SELECT screen FROM cinema_films WHERE filmName=? AND date=? AND time=?",
                               (self.selectFilm, self.selectDate, self.selectTime))

        self.screen = self.bookingDB.fetchall()[0][0]

        #update customer history
        self.selectSeat = ','.join(seatList)
        self.historyDB.execute("INSERT INTO customer_history VALUES (?,?,?,?,?,?,?)",(self.userName, self.selectDate,
                                self.selectTime, self.selectFilm, self.screen, self.selectNumberTickets, self.selectSeat))
        self.customerHistory.commit()
        #update the number of ticket left
        self.bookingDB.execute("UPDATE cinema_films SET tickets=? WHERE filmName=? AND date=? AND time=?",
                               (newTicketNumber, self.selectFilm, self.selectDate, self.selectTime))
        #update the seats left
        self.bookingDB.execute("SELECT seating, bookedSeat, availableSeat FROM cinema_films WHERE filmName=? AND date=? AND time=?",
                                                          (self.selectFilm, self.selectDate, self.selectTime))
        fetched=self.bookingDB.fetchone()

        oldSeating = fetched[0]
        newSeating = oldSeating + ',' + self.selectSeat
        oldBookedSeat = int(fetched[1])
        newBookedSeat = oldBookedSeat + int(self.selectNumberTickets)
        oldAvailableSeat = int(fetched[2])
        newAvailableSeat = oldAvailableSeat - int(self.selectNumberTickets)

        # print('make booking:')
        # print('old booked seat: ', oldBookedSeat, 'new booked seat: ', newBookedSeat)
        # print('old available seat: ', oldAvailableSeat, 'new available seat: ', newAvailableSeat)

        self.bookingDB.execute("UPDATE cinema_films SET seating=?, bookedSeat=?, availableSeat=? WHERE filmName=? AND date=? AND time=?",
                               (newSeating, newBookedSeat, newAvailableSeat, self.selectFilm, self.selectDate, self.selectTime))


        self.booking.commit()

    def readHistory(self):
        self.historyDB.execute("SELECT * FROM customer_history WHERE userName=? ORDER BY date DESC, time DESC", (self.userName,))
        a = self.historyDB.fetchall()
        if bool(a) == True:
            return a
        else:
            raise IndexError

    def cancelBooking(self, filmName, Date, Time, Tickets, Seat):
        #delete from history DB
        self.historyDB.execute("DELETE FROM customer_history WHERE userName=? AND date=? AND time=? AND filmName=? AND seat=?",
                               (self.userName, Date, Time, filmName, Seat))
        self.customerHistory.commit()

        #update the cinema_film DB
        self.bookingDB.execute("SELECT tickets, seating, bookedSeat, availableSeat FROM cinema_films WHERE filmName=? AND date=? AND time=?",
                                (filmName, Date, Time))
        fetched=self.bookingDB.fetchone()
        #add ticket number
        oldTicketNumber = fetched[0]
        newTicketNumber = oldTicketNumber + Tickets
        #update the seating list and seat numbers
        oldSeating = fetched[1]
        newSeating = oldSeating.replace(Seat,'')
        #update the number of seating
        oldAvailableSeat = int(fetched[3])
        newAvailableSeat = oldAvailableSeat+Tickets
        oldBookedSeat = int(fetched[2])
        newBookedSeat = oldBookedSeat-Tickets

        # print('cancel booking:')
        # print('old booked seat: ', oldBookedSeat, 'new booked seat: ', newBookedSeat)
        # print('old available seat: ', oldAvailableSeat, 'new available seat: ', newAvailableSeat)

        self.bookingDB.execute("""UPDATE cinema_films SET tickets=?, seating=?, availableSeat=?, bookedSeat=? WHERE filmName=? AND date=? AND time=?""",
                               (newTicketNumber, newSeating, newAvailableSeat, newBookedSeat, filmName, Date, Time))
        self.booking.commit()







######
customer_1 = Customer('TonyStark', 'aaaa')
customer_1.addToDB('Tony Stark', 'iam@ironman.com')
customer_2 = Customer('PeterParker', 'bbbb')
customer_2.addToDB('Peter Parker', 'young@spiderman.com')
######



