# # import stuff here
#
# twilio_account_sid = app.flask_app.config['TWILIO_ACCOUNT_SID']
# twilio_auth_token = app.flask_app.config['TWILIO_AUTH_TOKEN']
# twilio_number = app.flask_app.config['TWILIO_NUMBER']
#
# client = TwilioRestClient(account=twilio_account_sid, token=twilio_auth_token)
#
# @celery_task()
# def send_sms_ping(ping_id):
#
#     try:
#         ping = db.session.query(Ping).filter_by(id=ping_id).one()
#     except NoResultFound:
#         return
#
#     body = "What are you doing right now? (1) - entering data, (2) clinical rounds, (3) patient visit, (4) travel"
#
#     client.messages.create(
#         body=body,
#         to=ping.phone_number,
#         from_=twilio_number,
#     )