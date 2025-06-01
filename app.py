from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Guest model to store guest info and RSVP status
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rsvp_status = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Guest {self.name} RSVP: {self.rsvp_status}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/rsvp/<guest_id>', methods=['GET', 'POST'])
def rsvp(guest_id):
    guest = Guest.query.filter_by(guest_id=guest_id).first()
    if not guest:
        return "Guest not found", 404

    if request.method == 'POST':
        status = request.form.get('status')
        if status:
            guest.rsvp_status = status
            db.session.commit()
            return redirect(url_for('rsvp', guest_id=guest_id))

    return render_template('rsvp.html', name=guest.name, rsvp_status=guest.rsvp_status)

@app.route('/admin')
def admin():
    confirmed = Guest.query.filter_by(rsvp_status='confirmed').count()
    pending = Guest.query.filter_by(rsvp_status=None).count()
    declined = Guest.query.filter_by(rsvp_status='declined').count()
    total = Guest.query.count()

    return f'''
    <h1>Admin Dashboard</h1>
    <p>Total Guests: {total}</p>
    <p>Confirmed: {confirmed}</p>
    <p>Pending: {pending}</p>
    <p>Declined: {declined}</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
