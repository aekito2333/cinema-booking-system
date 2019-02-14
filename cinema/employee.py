import sqlite3
import csv
import tkinter
import datetime as dt
import sys


####################creat database for employee login#########################
conn = sqlite3.connect('employee_login.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS employee_login (
            userName text, password text)""")

#########################insert employees#####################################
#employee_1: Bucky:1111
c.execute("INSERT INTO employee_login VALUES ('Bucky', '1111')")
#employee_2: Captain:1111
c.execute("INSERT INTO employee_login VALUES ('Captain', '1111')")
conn.commit()
conn.close()

#####################creat database for films##################################
conn = sqlite3.connect('cinema_films.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS cinema_films (
            filmName text, date text, 
            time text, screen text, tickets int, seating text,
             bookedSeat int, availableSeat int)""")
conn.commit()
conn.close()

#####################creat database for films posters###########################
conn = sqlite3.connect('film_posters.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS film_posters (
            filmName text, description text, poster text, duration int)""")
conn.commit()
conn.close()


#Build a class for employee#
class Employee:
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
        self.time=''
        self.date=''
        self.filmName=''

        self.cinemaFilms = sqlite3.connect('cinema_films.db')
        self.filmDB = self.cinemaFilms.cursor()

        self.cinemaPoster = sqlite3.connect('film_posters.db')
        self.posterDB = self.cinemaPoster.cursor()

    def checkScreenAvailability(self, screen, startDate, days, duration, *screenTime):
        #text file for dumping output
        f = open('screen time overlap dump.txt', 'w+')
        results = []

        def overlap(startTime1, duration1, startTime2, duration2):#time type str
            #convert str into datetime:
            startTime1 = dt.datetime.strptime(startTime1, "%H:%M")
            startTime2 = dt.datetime.strptime(startTime2, "%H:%M")

            interval1 = [startTime1,startTime1+dt.timedelta(minutes=int(duration1))]
            interval2 = [startTime2, startTime2 + dt.timedelta(minutes=int(duration2))]
            results = []
            for i in interval1:
                results.append(interval2[0] <= i <= interval2[1])
            for i in interval2:
                results.append(interval1[0] <= i <= interval1[1])
            return True in results

        for x in range(0, days.days + 1):
            filmDate = startDate + dt.timedelta(x)
            #select all films on that day
            self.filmDB.execute('SELECT DISTINCT filmName FROM cinema_films WHERE screen=? AND date=?',(screen, filmDate))
            titleList=self.filmDB.fetchall()

            for title in titleList:
                self.posterDB.execute('SELECT duration FROM film_posters WHERE filmName=?',(title[0],))
                titleDuration=int(self.posterDB.fetchone()[0])#find the duration of the film
                self.filmDB.execute('SELECT DISTINCT time FROM cinema_films WHERE filmName=? AND screen=? AND date=?', (title[0], screen, filmDate))
                selectedTime=self.filmDB.fetchall()

                for i in screenTime:#time of film to be added
                    for j in selectedTime:#time of other films on the same day
                        if overlap(i,duration,j[0],titleDuration):
                            results.append(True)
                            f.write('SCREEN:{} {} {} {} OVERLAP with current film {} \r\n'.format(screen,filmDate,title[0],j[0],i))

        f.close()
        return(results)

    def addFilms(self, **kwargs):
        self.filmName = kwargs.get('filmName')
        self.duration = kwargs.get('duration')
        self.description = kwargs.get('description')
        self.date = kwargs.get('date')
        self.time = kwargs.get('time')
        self.screen = kwargs.get('screen')
        self.seating = kwargs.get('seating')
        self.poster = kwargs.get('poster')
        self.tickets = kwargs.get('tickets')

        self.filmDB.execute("INSERT INTO cinema_films VALUES (:filmName, :date, :time, :screen, :tickets, :seating, :bookedSeat, :availableSeat)",
                            {'filmName': self.filmName, 'date': self.date, 'time': self.time, 'screen': self.screen,
                             'tickets': self.tickets, 'seating': self.seating, 'bookedSeat': 0, 'availableSeat': 15})
        self.cinemaFilms.commit()

        #check if film is already in posterDB
        self.posterDB.execute("SELECT * FROM film_posters WHERE filmName=?", (self.filmName,))
        a = self.posterDB.fetchall()

        if bool(a) == False:#if return empty list
            self.posterDB.execute("INSERT INTO film_posters VALUES (?,?,?,?)",(self.filmName,self.description, self.poster, self.duration))
            self.cinemaPoster.commit()

        return

    def exportList(self, **kwargs):
        self.exportFileName = kwargs.get('exportFileName')+'.csv'
        self.filmDB.execute('SELECT * FROM cinema_films')
        with open(self.exportFileName, 'w') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            # write header
            csv_out.writerow([d[0] for d in self.filmDB.description])
            # write data
            for i in self.filmDB:
                csv_out.writerow(i)
        return


###########################manually create employee instance####################
employee_1 = Employee('Bucky', '1111')
employee_2 = Employee('Captain', '1111')
dictOfEmployees = {'Bucky': employee_1, 'Captain' : employee_2}


############################add some films to database##########################

# ##film_1, 'Fantastic Beasts: The Crimes Of Grindelwald'##

startDate = dt.date(2019, 1, 1)
endDate = dt.date(2019,1,20)
days = endDate-startDate

for x in range(0,days.days+1):
    filmDate = startDate + dt.timedelta(x)
    for y in ('09:00', '12:00', '19:30'):
        film_1 = {'filmName': 'Fantastic Beasts: The Crimes Of Grindelwald',
                 'description': 'In an effort to thwart the powerful Dark wizard Gellert Grindelwald\'s plans, Albus Dumbledore enlists his former student Newt Scamander.',
                 'duration': 120, 'date' : str(filmDate),'time' : y , 'screen' : '2', 'tickets': 3,
                 'seating' : ' ', 'poster': 'fantastic_beast.gif'}
        employee_1.addFilms(**film_1)

##film_2, 'Aquaman'##

startDate = dt.date(2019, 1, 1)
endDate = dt.date(2019,1,13)
days = endDate-startDate

for x in range(0,days.days+1):
    filmDate = startDate + dt.timedelta(x)
    for y in ('11:00', '15:00'):
        film_2 = {'filmName': 'Aquaman',
                  'description': '"Aquaman" reveals the origin story of half-human, half-Atlantean Arthur Curry and takes him on the journey of his lifetime.',
                  'duration': 150, 'date': str(filmDate), 'time': y, 'screen': '1', 'tickets': 15,
                  'seating': '', 'poster': 'aquaman.gif'}
        employee_1.addFilms(**film_2)

##film_3, 'Dragon Ball Super: Broly'##

startDate = dt.date(2019, 1, 1)
endDate = dt.date(2019, 1, 23)
days = endDate - startDate

for x in range(0, days.days + 1):
    filmDate = startDate + dt.timedelta(x)
    film_3_1 = {'filmName': 'Dragon Ball Super: Broly',
                 'description': 'Goku and Vegeta encounter Broly, a Saiyan warrior unlike any fighter they\'ve faced before.',
                 'duration': 60, 'date': str(filmDate), 'time': '18:00', 'screen': '1', 'tickets': 15,
                 'seating': '', 'poster': 'dragon_ball.gif'}
    employee_1.addFilms(**film_3_1)
    film_3_2 = {'filmName': 'Dragon Ball Super: Broly',
                'description': 'Goku and Vegeta encounter Broly, a Saiyan warrior unlike any fighter they\'ve faced before.',
                'duration': 60, 'date': str(filmDate), 'time': '15:00', 'screen': '2', 'tickets': 15,
                'seating': '', 'poster': 'dragon_ball.gif'}

    employee_1.addFilms(**film_3_2)

##film_4, 'zootropolis'##

startDate = dt.date(2019, 1, 4)
endDate = dt.date(2019,1,20)
days = endDate-startDate

for x in range(0,days.days+1):
    filmDate = startDate + dt.timedelta(x)
    for y in ('22:00',):
        film_4 = {'filmName': 'Zootropolis',
                  'description': 'In a world populated by anthropomorphic mammals, rabbit Judy Hopps from rural Bunnyburrow fulfills her childhood dream of becoming a police officer in urban zootropolis.',
                  'duration': 90, 'date': str(filmDate), 'time': y, 'screen': '1', 'tickets': 10,
                  'seating': '', 'poster': 'zootropolis.gif'}
        employee_1.addFilms(**film_4)





######For testing################################################################
# ascreen='2'
# astartDate=dt.date(2019,1,1)
# aendDate=dt.date(2019,1,21)
# adays = aendDate-astartDate
# duration='120'
# screenTime=['09:00','18:00']
#
#
#
# #def checkScreenAvailability(self, screen, startDate, days, duration, *screenTime)
# employee_1.checkScreenAvailability(ascreen,astartDate,adays,duration,*screenTime)