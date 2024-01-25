import pyodbc
from flask import Flask, jsonify, request, render_template


server = 'DESKTOP-3SQKCMU\WORKSERVER'
database = 'SocialApp'
driver = '{SQL Server}'

conn = pyodbc.connect('DRIVER=' + driver +
                      ';SERVER=' + server +
                      ';DATABASE=' + database +
                      ';Trusted_Connection=yes')

class DataAccess:
    def __init__(self):
        return

    def get_user_data(self):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Main")
        data = cursor.fetchall()
        cursor.close()
        return data

    def getUserName(self,data):
        cursor = conn.cursor()
        email = data.get('email')
        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        user = cursor.fetchone()  # fetchone kullanarak sadece bir satırı alın
        cursor.close()
        return user

    def add_data(self, data):
        userName = data.get('userName')
        location = data.get('location')
        purpose = data.get('purpose')
        hobbies = data.get('hobbies')
        startTime = data.get('startTime')
        finishTime = data.get('finishTime')

        # Veritabanına veri ekle
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Main (userName, location, purpose, hobbies, startTime, finishTime) VALUES (?, ?, ?, ?, ?, ?)",
            (userName, location, purpose, hobbies, startTime, finishTime))
        matched_users = self.check_matching_data(location, purpose, hobbies, cursor, userName)
        conn.commit()
        cursor.close()
        return matched_users


    def check_matching_data(self,location, purpose, hobbies, cursor, userName):
        query = """
                SELECT TOP 1 userName
            FROM Main
            WHERE location = ? AND purpose = ? AND hobbies = ? AND userName <> ?
        """
        cursor.execute(query, (location, purpose, hobbies, userName))
        matching_data = cursor.fetchall()

        matchedUserName = []
        for data in matching_data:
            matchedUserName.append({
                'matchedUserName': data.userName
            })

        return matchedUserName

    def register(self,nameSurname,email,password):
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        last = result.fetchall()
        print(last)
        if last:
            cursor.close()
            return jsonify({'message': 'Already Registerd!!'})

        else:
            cursor.execute("INSERT INTO Users (nameSurname, email, password) VALUES (?, ?, ?)",
                           (nameSurname, email, password))
            conn.commit()
            cursor.close()
            return jsonify({'message': 'Veriler veritabanına başarıyla eklendi!'})


    def login(self,email,password):
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email, password))
        last = result.fetchall()
        cursor.close()
        print(last)
        return last
