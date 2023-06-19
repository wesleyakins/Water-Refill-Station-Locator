from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, RefillForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
import folium

@app.route('/')
@app.route('/index')
@login_required

def index():  
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # When submit is clicked checks the values inputted against ones in the database
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data): # Error if the values are incorrect
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': # Redirects to index page if the values are correct
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')

def logout(): # Logs the user out of the application
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit(): # When submit is clicked adds new user to the database
        user = User(username=form.username.data, email=form.email.data, reward_points=0)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/redeem_points')
def redeem_points(): # Returns an under construction page
    return render_template('wip.html')

@app.route('/settings')
def settings(): # Returns an under construction page
    return render_template('wip.html')

@app.route('/refill_station')

def refill_station():
    return render_template('refill_station.html')

@app.route('/show_map')
# This function uses the folium module to produce a map of the campus area
def show_map():
    map = folium.Map(
    location=[54.58531847171733, -5.93441441254851],
    tiles= 'Stamen Terrain',
    zoom_start=15
    )
# The marker is used on the map to show specific refill stations
    folium.Marker(
        location=[54.58182698878067, -5.9373950586437845],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="Computer Science Building",
        icon=folium.Icon(color='red')
    ).add_to(map)

    folium.Marker(
        location=[54.58128682792822, -5.935975648922612],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="QUB David Keir Building",
        icon=folium.Icon(color='red')
    ).add_to(map)

    folium.Marker(
        location=[54.58469903885533, -5.937153225323336],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="Queen's Students' Union",
        icon=folium.Icon(color='red')
    ).add_to(map)

    folium.Marker(
        location=[54.584827085769014, -5.933450560765014],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="Peter Froggatt Centre",
        icon=folium.Icon(color='red')
    ).add_to(map)

    folium.Marker(
        location=[54.58558700607439, -5.933921047546236],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="Queen’s Film Theatre",
        icon=folium.Icon(color='red')
    ).add_to(map)

    folium.Marker(
        location=[54.58515193893183, -5.932930022198555],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="QUB Music Building",
        icon=folium.Icon(color='red')
    ).add_to(map)

    folium.Marker(
        location=[54.58563921381927, -5.936143346810733],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="School of Arts, English and Languages",
        icon=folium.Icon(color='red')
    ).add_to(map)

    folium.Marker(
        location=[54.58396572776259, -5.935961685766402],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="Physics building, Queen's University Belfast",
        icon=folium.Icon(color='red')
    ).add_to(map)

    folium.Marker(
        location=[54.58406292462757, -5.933058215998401],
        popup="<a href='/refill'>Refill water here</a>",
        tooltip="School of Maths and Physics Teaching Centre",
        icon=folium.Icon(color='red')
    ).add_to(map)

    return map._repr_html_()

@app.route('/refill', methods=['GET', 'POST'])
def refill(): 
    form = RefillForm()      
    points = 0
    if form.validate_on_submit(): # Determines how many points user will get based on value from the form then adds them to points value in the database
        if form.refill_val.data >= 0 and form.refill_val.data <= 500:
            points = 5
        elif form.refill_val.data >= 501 and form.refill_val.data <= 750:
            points = 10
        elif form.refill_val.data >= 751 and form.refill_val.data <= 1000:
            points = 15
        
        user = User.query.get(current_user.id)
        user.reward_points += points
        db.session.commit()
        flash('Congratulations, you have refilled your water bottle!')
        return redirect(url_for('index'))
    return render_template('refill.html', form=form)
