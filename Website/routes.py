from Website import app
from flask import render_template,redirect,url_for,request,flash,jsonify
from flask_login import login_user,current_user,login_required,logout_user
from Website import bcrypt
from Website.models import Users,Notes
from Website import db
import json

# Routes of the Website :

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password,password):
                flash(f'Logged in successfully! as {user.username}', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@app.route('/reg-form',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email    = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user =  Users.query.filter_by(email=email).first()
        user_name =  Users.query.filter_by(username=username).first()
        if user:
            flash('Email already exists. Please try a different one.',category='error')
        elif user_name:  
            flash('Username already exists. Please try a different one.',category='error')
        elif len(username) < 7:
            flash('Username must be greater than 7 characters',category='error')
        elif len(password1) <= 8:
            flash('Password must be greater or equal to 8 characters',category='error')
        elif password1!= password2 :
            flash('Passwords do not match. Please Try Again',category='error')
        else:
            password = bcrypt.generate_password_hash(password1)
            new_user = Users(username=username,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully.',category='success')
            login_user(user=new_user)
            return redirect(url_for('home'))
    return render_template('register.html')
@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html',user=current_user)
@app.route('/notes',methods=['GET','POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 2:
            flash('Note is too short !',category='error')
        else:
            new_note = Notes(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully !',category='success')

    return render_template('notes.html',user=current_user,no_of_notes=0)
@app.route('/profile')
@login_required
def profile():
    user=current_user
    no_of_notes = len(user.notes)
    return render_template('profile.html',user=user,no_of_notes=no_of_notes)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@app.route("/admin-notes")
@login_required
def admin():
    return render_template('admin.html')