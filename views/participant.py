from flask.views import MethodView
from forms.new_participant import NewParticipantForm
from models import Participant
from flask import request, redirect, url_for
import app

class ParticipantResourceCreate(MethodView):

    def post(self):
        form = NewParticipantForm(request.form)

        if form.validate():
            participant = Participant(**form.data)
            app.db.session.add(participant)
            app.db.session.commit()

            return redirect(url_for('participants.index'), code=303)
        else:
            return render_template('participants/new.html', form=form), 400

class ParticipantResourceIndex(MethodView):

    def get(self):
        all_participants = app.db.session.query(Participant).all()
        return render_template('participants/index.html',
                               appintments=all_appointments)


class ParticipantFormResource(MethodView):

    def get(self):
        form = NewParticipantForm()
        return render_template('participants/new.html', form=form)


