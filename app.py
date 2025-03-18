from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Loads Model
class Load(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    how_many = db.Column(db.Integer, nullable=False)
    power = db.Column(db.Float, nullable=False)
    duration_total = db.Column(db.Float, nullable=False)
    duration_night = db.Column(db.Float, nullable=False)

# Batteries Model
class Battery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    how_many = db.Column(db.Integer, nullable=False)
    voltage = db.Column(db.Float, nullable=False)
    power = db.Column(db.Float, nullable=False)

# Panels Model
class Panel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    how_many = db.Column(db.Integer, nullable=False)
    voltage = db.Column(db.Float, nullable=False)
    duration_total_night = db.Column(db.Float, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loads', methods=['GET', 'POST'])
def loads():
    if request.method == 'POST':
        name = request.form['name']
        how_many = int(request.form['how_many'])
        power = float(request.form['power'])
        duration_total = float(request.form['duration_total'])
        duration_night = float(request.form['duration_night'])
        new_load = Load(name=name, how_many=how_many, power=power, duration_total=duration_total, duration_night=duration_night)
        db.session.add(new_load)
        db.session.commit()
        return redirect(url_for('loads'))
    loads = Load.query.all()
    total_power = sum(load.power * load.how_many for load in loads)
    total_duration = sum(load.duration_total * load.how_many for load in loads)
    total_night = sum(load.duration_night * load.how_many for load in loads)
    return render_template('loads.html', loads=loads, total_power=total_power, total_duration=total_duration, total_night=total_night)

@app.route('/batteries', methods=['GET', 'POST'])
def batteries():
    if request.method == 'POST':
        name = request.form['name']
        how_many = int(request.form['how_many'])
        voltage = float(request.form['voltage'])
        power = float(request.form['power'])
        new_battery = Battery(name=name, how_many=how_many, voltage=voltage, power=power)
        db.session.add(new_battery)
        db.session.commit()
        return redirect(url_for('batteries'))
    batteries = Battery.query.all()
    total_power = sum(battery.power * battery.how_many for battery in batteries)
    return render_template('batteries.html', batteries=batteries, total_power=total_power)

@app.route('/panels', methods=['GET', 'POST'])
def panels():
    if request.method == 'POST':
        name = request.form['name']
        how_many = int(request.form['how_many'])
        voltage = float(request.form['voltage'])
        duration_total_night = float(request.form['duration_total_night'])
        new_panel = Panel(name=name, how_many=how_many, voltage=voltage, duration_total_night=duration_total_night)
        db.session.add(new_panel)
        db.session.commit()
        return redirect(url_for('panels'))
    panels = Panel.query.all()
    total_voltage = sum(panel.voltage * panel.how_many for panel in panels)
    return render_template('panels.html', panels=panels, total_voltage=total_voltage)

if __name__ == '__main__':
    app.run(debug=True)
