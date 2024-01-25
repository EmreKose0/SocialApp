from flask import Flask, jsonify, request, render_template
import pyodbc
import DataAccess as Db
from datetime import datetime


class BussinesLayer:
    def __init__(self):
        return
    def get_data(self):
        dbl = Db.DataAccess()
        data = dbl.get_user_data()
        response = []
        for row in data:
            response.append({
                'userName': row.userName,
                'location': row.location,
                'purpose': row.purpose,
                'hobbies': row.hobbies,
                'startTime': row.startTime,
                'finishTime': row.finishTime
            })

        return jsonify({'data': response})

    def getUserName(self,data):
        if request.method == 'POST':
           dbl = Db.DataAccess()
           user = dbl.getUserName(data)
           if user:
                return jsonify({'userName': user[1]})  # user[1] olarak kullanıcı adını alın
           else:
                return jsonify({'error': 'Kullanıcı bulunamadı'}), 404

        else:
            return jsonify({'error': 'Kullanıcı bulunamadı'}), 404


    def add_data(self,data):
        if request.method == 'POST':
            # Gelen isteği JSON olarak al

            # Gelen JSON verisinden istenen parametreleri al
            dbl = Db.DataAccess()
            matched_users = dbl.add_data(data)
            print(matched_users)
            response_data = {
                'message': 'Veriler veritabanına başarıyla eklendi!',
                'matchedUsers': matched_users
            }

            return jsonify(response_data)



    def register(self,data):
        if request.method == 'POST':
            # Gelen isteği JSON olarak al

            # Gelen JSON verisinden istenen parametreleri al
            nameSurname = data.get('nameSurname')
            email = data.get('email')
            password = data.get('password')

            # Veritabanına veri ekle
            dbl = Db.DataAccess()
            return dbl.register(nameSurname,email,password)



    def login(self,data):
        if request.method == 'POST':
            # Gelen isteği JSON olarak al

            # Gelen JSON verisinden istenen parametreleri al
            email = data.get('email')
            password = data.get('password')

            # Veritabanına veri ekle
            dbl = Db.DataAccess()
            last = dbl.login(email,password)
            if last:
                return jsonify({'message': 'Success'}), 200
            else:
                return jsonify({'message': 'Error'}), 401

        return jsonify({'message': 'Error'}), 401