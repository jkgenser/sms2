from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
import config
import twilio.twiml
import os
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

# endpoint for app to get hit by twilio POST reqests
@app.route('/message', methods=['POST'])
def store_response():

    try:
        ping = {}

        # Eventually make this do a lookup from participants
        # if the number is not in participants, do not store the ping in DB.
        ping['from_num'] = request.values['From']

        # Eventually check if response is integer, otherwise store as string
        # Or always store as string ... not sure
        ping['response'] = request.values['Body']

        ping['received_time'] = datetime.datetime.now()
        ping['received'] = 1

        db.session.add(Ping(**ping))
        db.session.commit()
        print('things were saved succesfully')

    except:
        print('something went wrong')

    print(request.values['From'], request.values['Body'], datetime.datetime.now())
    print(ping)


    return


if __name__ == '__main__':
    app.run()


from models import Participant, Survey, Ping