# -*- coding: utf-8 -*-
import sqlite3

def initiate_db_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL  
    ) 
    ''')

    cursor.execute("SELECT * FROM Products")
    if cursor.fetchone() is None:
        for i in range(4):
            cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                           ('Продукт' + str(i + 1), 'Описание ' + str(i + 1), 100 * (i + 1)))


    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products

def initiate_db_users():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL          
    ) 
    ''')
    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        return False
    else:
        return True


def get_user(username):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    return user

if __name__ == '__main__':
    initiate_db_products()
    initiate_db_users()
    get_all_products()

