import mysql.connector
import sys
from datetime import datetime
class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        #self.conn = self.connect()
        self.data = None

    def connect(self):
        try:
            conn = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )
            print("Connected to the database")
            return conn
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            sys.exit(1)

    def receive_message(self, msg):
        # print('database ', msg.get_data())
        self.data = msg.get_data()
        self.export_data()

    def export_data(self):
        current_time = datetime.now()
        # print(current_time, data)
        try:
            cursor = self.conn.cursor()
            sql = f"INSERT INTO TempRecord (timeData, tempData, humidityData, deltaTempSec, degreeCfromTarget) VALUES ('{current_time}', {self.data[0]}, {self.data[1]}, {self.data[2]}, {self.data[3]})"  # Using parameterized query
            cursor.execute(sql) 
            self.conn.commit()
            print("Data inserted successfully")
        except mysql.connector.Error as err:
            print("Error: ", err)
            self.conn.rollback()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")

