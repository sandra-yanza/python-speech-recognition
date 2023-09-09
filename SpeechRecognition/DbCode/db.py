import sqlite3
from contextlib import closing

# Class to define the objects to store in the database
class SpeechToAudio():
    def __init__(self, file_name, file_blob, text_speech):
        self.id = id
        self.file_name = file_name
        self.file_blob = file_blob
        self.text_speech = text_speech

    def __str__(self)->str:
        return f"{self.file_name} {self.text_speech}"

# Class to manage the database connection. We are using SQLite Database.
class DB():
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

    def ping(self):
        with closing(self.conn.cursor()) as cur:
            sql = "select 'ping' as col"
            resp = cur.execute(sql)
            for r in resp.fetchall():
                print(r['col'])

    # Method to get the list of recorded audios
    def get_audios(self):
        with closing(self.conn.cursor()) as cur:
            sql = '''select file_name,file_blob,text_speech from speechtoaudio order by id asc;'''
            audios = []
            rows = cur.execute(sql)
            for row in rows.fetchall():
                audio = SpeechToAudio(row['file_name'],row['file_blob'],row['text_speech'])
                audios.append(audio)
            return audios
        
     # Method to insert a record   
    def insert(self, speechToAudio):
        with closing(self.conn.cursor()) as cur:
            sql = '''
            insert into speechtoaudio (file_name,file_blob,text_speech) values(?,?,?);
            '''
            cur.execute(sql,[speechToAudio.file_name, speechToAudio.file_blob,speechToAudio.text_speech])
            self.conn.commit()
