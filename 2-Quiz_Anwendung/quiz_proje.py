import random
import sqlite3

def get_db_connection():
    db_conn=sqlite3.connect("quiz_db.sqlite")
    db_conn.row_factory=sqlite3.Row
    return db_conn



class Admin():
    def __init__(self, vorname='', nachname='', email='', passwort='', geburtsdatum='', id=''):
        self.vorname=vorname
        self.nachname=nachname
        self.email=email
        self.passwort=passwort
        self.geburtsdatum=geburtsdatum
        self.id=random.randint(10**9, 10**10-1)
        self.db_conn=get_db_connection()
        self.db_cursor=self.db_conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                                    id INTEGER PRIMARY KEY,
                                    vorname TEXT,
                                    nachname TEXT,
                                    email TEXT UNIQUE,
                                    passwort TEXT,
                                    geburtsdatum TEXT)''')
        self.db_conn.commit()
    
    def databaseErstellen(self):

        try:
            self.db_cursor.execute("INSERT INTO admins (id, vorname, nachname, email, passwort, geburtsdatum) VALUES (?, ?, ?, ?, ?, ?)", 
                                   (self.id, self.vorname, self.nachname, self.email, self.passwort, self.geburtsdatum))
            self.db_conn.commit()
            print(f'Admin erstellt. Benutzername: {self.vorname} {self.nachname}, ID: {self.id}, Passwort: {self.passwort} ')

        except sqlite3.IntegrityError:
            print("Fehler: Diese E-Mail-Adresse wird bereits verwendet.")
            


    def databaseCheck(self, email, passwort):

        self.db_cursor.execute("SELECT * FROM admins WHERE email=? AND passwort=?", (email, passwort))
        result = self.db_cursor.fetchone()
        self.adminCheck(result)
        

    def adminCheck(self, result):
        
        if result:
            print('Login erfolgreich. Was möchten Sie tun?')
            self.welchePart()
        
        else:
            print('Login fehlgeschlagen. Sie werden zum Hauptmenü weitergeleitet.')
            startseit()

    def adminErstellen(self):
        self.vorname=input('Vorname:')
        self.nachname=input('Nachname:')
        self.email=input('Email:')
        self.geburtsdatum=input('Geburtsdatum:')
        self.passwort=input('Passwort:')
        self.databaseErstellen()

        

    def adminLogin(self):
        email=input('Email:')
        passwort=input('Passwort:')
        self.databaseCheck(email, passwort)




    def welchePart(self):
        islem=int(input('Welche Aktion möchten Sie durchführen? \n 1. Admin erstellen \n 2. Frage hochladen'))
        frage=Fragen()

        if islem == 1:
            self.adminErstellen()

        elif islem == 2:
            frage.frageHinzufügen()
            
class Nutzer():
    def __init__(self, vorname='', nachname='', email='', passwort='', geburtsdatum='', id=''):
        self.vorname=vorname
        self.nachname=nachname
        self.email=email
        self.passwort=passwort
        self.geburtsdatum=geburtsdatum
        self.id=random.randint(10**9, 10**10-1)
        self.db_conn=get_db_connection()
        self.db_cursor=self.db_conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS nutzers (
                                    id INTEGER PRIMARY KEY,
                                    vorname TEXT,
                                    nachname TEXT,
                                    email TEXT UNIQUE,
                                    passwort TEXT,
                                    geburtsdatum TEXT)''')
        self.db_conn.commit()
    


    def databaseErstellen(self):

        try:
            self.db_cursor.execute("INSERT INTO nutzers (id, vorname, nachname, email, passwort, geburtsdatum) VALUES (?, ?, ?, ?, ?, ?)", 
                                   (self.id, self.vorname, self.nachname, self.email, self.passwort, self.geburtsdatum))
            self.db_conn.commit()
            print(f'Benutzer erstellt. Benutzername: {self.vorname} {self.nachname}, ID: {self.id}, Passwort: {self.passwort}')

        except sqlite3.IntegrityError:
            print("Fehler: Diese E-Mail-Adresse wird bereits verwendet.")
            


    def databaseCheck(self, email, passwort):

        self.db_cursor.execute("SELECT id FROM nutzers WHERE email=? AND passwort=?", (email, passwort))
        id = self.db_cursor.fetchone()
        self.nutzerCheck(id)
        

    def nutzerCheck(self, id):
        
        if id:
            print('Login erfolgreich. Was möchten Sie tun?')

            self.welchePart(id)

        else:
            print('Login fehlgeschlagen. Sie werden zum Hauptmenü weitergeleitet.')
            
            startseit()


    def nutzerErstellen(self):
        self.vorname=input('Vorname:')
        self.nachname=input('Nachname:')
        self.email=input('Email:')
        self.geburtsdatum=input('Geburtsdatum:')
        self.passwort=input('Passwort:')
        self.databaseErstellen()

        

    def nutzerLogin(self):
        email=input('Email:')
        passwort=input('Passwort:')
        self.databaseCheck(email, passwort)


    def hauptPart(self):
        islem=int(input('Welche Aktion möchten Sie durchführen? \n 1. Benutzeranmeldung, 2. Benutzerregistrierung'))

        if islem==1:
            self.nutzerLogin()
        else:
            self.nutzerErstellen()

    def welchePart(self, id):
        eingang=int(input('Welche Aktion möchten Sie durchführen? \n 1. Quiz lösen, 2. Ergebnisliste ansehen'))
        quiz=Quiz()
        user_id=id[0]

        if eingang==1:
            quiz.benutzercheck(user_id)
        elif eingang == 2:
            pass
        else:
            print('Falsche Taste gedrückt, bitte erneut eine Taste drücken.')
            self.welchePart()


class Fragen():
    def __init__(self, text='', antwortA='', antwortB='', antwortC='', antwortD='', richtig='' ):
        self.text=text
        self.antwortA=antwortA
        self.antwortB=antwortB
        self.antwortC=antwortC
        self.antwortD=antwortD
        self.richtig=richtig
        self.db_conn=get_db_connection()
        self.db_cursor=self.db_conn.cursor()
        self.create_table()
        
    
    def create_table(self):
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS fragen (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    text TEXT UNIQUE,
                                    antwortA TEXT,
                                    antwortB TEXT,
                                    antwortC TEXT,
                                    antwortD TEXT,
                                    richtig TEXT)''')
        self.db_conn.commit()




    def databaseErstellen(self):

        try:
            self.db_cursor.execute("INSERT INTO fragen (text, antwortA, antwortB, antwortC, antwortD, richtig) VALUES (?, ?, ?, ?, ?, ?)", 
                                   (self.text, self.antwortA, self.antwortB, self.antwortC, self.antwortD, self.richtig))
            self.db_conn.commit()
            print(f'Frage wurde erfolgreich gespecheirt. \n {self.text} \n A: {self.antwortA}, B: {self.antwortB}, C: {self.antwortC}, D: {self.antwortD} \n richtige antwort ist {self.richtig} ')
            kontrol=input('Möchten Sie die Frage erneut hochladen? j/n')

            if kontrol=='j':
                self.frageHinzufügen()
            else:
                vorherige=Admin()
                vorherige.welchePart()



        except sqlite3.IntegrityError:
            print("Fehler: Diese Frage existiert bereits!")

    def frageHinzufügen(self):
        self.text=input('Bitte geben Sie die Frage ein: ').capitalize()
        self.antwortA=input('Geben Sie Antwort A ein: ')
        self.antwortB=input('Geben Sie Antwort B ein: ')
        self.antwortC=input('Geben Sie Antwort C ein: ')
        self.antwortD=input('Geben Sie Antwort D ein: ')
        self.richtig=input('Geben Sie die richtige Antwort ein: ').upper()
        
        self.databaseErstellen()


class Quiz():
    def __init__(self):
        self.punkte=0
        self.check={}
        self.db_conn=get_db_connection()
        self.db_cursor=self.db_conn.cursor()
        self.create_table()
        self.neuecolumnhinzufugen()

    def fragenZahl(self):
        self.db_cursor.execute("SELECT count(*) FROM fragen ")
        return self.db_cursor.fetchone()[0]


    def create_table(self):

        fragenzahl= self.fragenZahl()

        if fragenzahl == 0:
            print("Die Tabelle wurde nicht erstellt, da keine Fragen vorhanden sind!")
            return  

        column_definitions = ", ".join([f"soru{i+1} TEXT DEFAULT '0'" for i in range(fragenzahl)])
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS quiz_sorulari (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER,
            {column_definitions},
            FOREIGN KEY (user_id) REFERENCES nutzers(id) ON DELETE CASCADE
        )
        """

        self.db_cursor.execute(create_table_query)
        self.db_conn.commit()


    def neuecolumnhinzufugen(self):

        fragenzahl= self.fragenZahl()
        self.db_cursor.execute("PRAGMA table_info(quiz_sorulari)")  # Quiz tablosunun sütun bilgilerini al
        columns = [column[1] for column in self.db_cursor.fetchall()]  # Tablo sütunlarını listele


        # Eğer yeni bir soru varsa, yeni sütun ekle
        if len(columns) - 2 < fragenzahl:  # -1 çünkü 'id' ve 'user_id' zaten var
            for i in range(len(columns) - 2, fragenzahl):  # Yeni sorular eklemek için döngü
                self.db_cursor.execute(f"ALTER TABLE quiz_sorulari ADD COLUMN soru{i+1} TEXT DEFAULT '0'")
                self.db_conn.commit()


    
    def neudataErstellen(self, user_id):
    # Soruların sayısını al
        self.db_cursor.execute("SELECT count(*) FROM fragen")
        fragenzahl = self.db_cursor.fetchone()[0]

        if fragenzahl == 0:
            print("Es gibt keine Fragen in der Datenbank.")
            return

        # Sorular için varsayılan değerlerle bir satır ekleyelim
        column_names = ", ".join([f"soru{i+1}" for i in range(fragenzahl)])
        default_values = ", ".join(['0' for _ in range(fragenzahl)])

        # Kullanıcı için yeni bir satır ekleyelim
        insert_query = f"""
        INSERT INTO quiz_sorulari (user_id, {column_names})
        VALUES ({user_id}, {default_values})
        """

            # Parametreler: user_id ve her soruya varsayılan 0
        self.db_cursor.execute(insert_query)
        self.db_conn.commit()
        self.benutzercheck(user_id)


        


    
    def updatedata(self):

        self.db_cursor.execute("SELECT count(*) FROM fragen")
        fragenzahl = self.db_cursor.fetchone()[0]

        update_columns = []
        update_values = []

        # values sözlüğündeki her bir soru için sütun adı ve değerini ekle
        for i in range(2, len(self.check)):
            update_columns.append(f"Soru{i-1} = ?")  # Güncellenmek istenen sütun
            update_values.append(self.check[i])  # Güncellenmek istenen değer

        # Güncelleme sorgusu
        update_query = f"""
            UPDATE quiz_sorulari
            SET {', '.join(update_columns)}
            WHERE user_id = ?
            """
        update_values.append(self.check[1])  # son olarak user_id eklenmeli

        # Sorguyu çalıştır
        self.db_cursor.execute(update_query, tuple(update_values))
        self.db_conn.commit()
        print("Die Quiz-Ergebnisse wurden aktualisiert!")

    


    def benutzercheck(self, id):
        self.db_cursor.execute("SELECT * FROM quiz_sorulari WHERE user_id = ?", (id,))
        self.check=self.db_cursor.fetchone()

        self.check = list(self.check) if self.check else None
          

        if self.check:
            self.zeigenFragen()

        else:
            self.neudataErstellen(id)


            
        
        
    def frageBekommen(self, zahl=5):
        self.db_cursor.execute("SELECT * FROM fragen ORDER BY RANDOM() LIMIT ?", (zahl,))
        return self.db_cursor.fetchall()
    
    


    def zeigenFragen(self):
        fragen = self.frageBekommen()


        i= 1
        
        for frage in fragen:
            self.frageProcess(i)
            print(f'Frage {i}: {frage[1]}')
            print(f'A:{frage[2]},  B:{frage[3]}, C:{frage[4]}, D:{frage[5]} ')

            self.frageAnnahme(frage[0], frage[6])

            i+=1

        self.frageProcess(i)

            



    def frageAnnahme(self, frageid, richtig):
        while True:
            antwort = input('Bitte geben Sie die richtige Antwort an:').upper()
            
            if antwort in ['A', 'B', 'C', 'D']:  
                break  
            else:
                print("Fehler! Bitte geben Sie eine der Optionen A, B, C oder D ein.")

        if antwort==richtig:
            self.punkte += 1
            print(self.check[frageid+1])
            self.check[frageid+1] = str(int(self.check[frageid+1]) + 1)
            

        else:
            self.check[frageid+1] = str(int(self.check[frageid+1]) - 1)


        

    def frageProcess(self, i):

        if i>5:
            print('Das Quiz ist fertig'.center(50,'*'))
            self.zeigePunkte()

        else:
            print(f'Frage {i} in 5'.center(100,'*'))




    def zeigePunkte(self):
        print(f'Ihr Punktestand:{self.punkte}')


        self.updatedata()







def startseit():
    islem=int(input('Welche Aktion möchten Sie durchführen? \n 1. Administrator Aktionen \n 2. Benutzer Aktionen'))

    if islem==1:
        admin=Admin()
        admin.adminLogin()
    
    elif islem==2:
        
        nutzer=Nutzer()
        nutzer.hauptPart()
    
startseit()


    
    
    
        
















        
