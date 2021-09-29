from datetime import datetime
from apps import App

app_object = App()
mongo = app_object.mongo
now = datetime.now()

now = now.strftime('%Y-%m-%d %H:%M')

name = ['AJ', 'AJ', 'Banpreet', 'Vaishnavi', 'Shivam']
designation = ['a', 'b', 'c', 'd', 'e']
email = [
    'atharvajoshi10@gmail.com',
    'atharvajoshi10@gmail.com',
    'iwvaidvoawpw2@123.com',
    'atharva1996@gmail.com',
    'atharva.patil@b.com']
job_title = ['a', 'b', 'c', 'd', 'e']
job_description = ['a', 'b', 'c', 'd', 'e']

for i in range(5):
    id = mongo.db.jobs.insert({'name': name[i],
                               'email': email[i],
                               'designation': designation[i],
                               'job_title': job_title[i],
                               'job_description': job_description[i],
                               'time_posted': now})
