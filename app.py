from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__)

#login system copy paste
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        
users = {
    'admin': User(1, 'admin', generate_password_hash('password123'))
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

#login system ends

@app.route('/')
@login_required 
def index():
    customers = database.get_all_customers()
    return render_template('index.html', customers=customers)

@app.route('/add', methods=["POST"])
@login_required 
def add():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    notes = request.form["notes"]
    database.add_customers(name,email,phone,notes)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required 
def delete(id):
    database.delete_customer(id)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
@login_required 
def edit(id):
    customers = database.get_customer(id)
    return render_template('edit.html', customers=customers)

@app.route('/update', methods=['POST'])
@login_required 
def update():
    id = request.form["id"]
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    notes = request.form["notes"]
    database.update_customer(id,name,email,phone,notes)
    return redirect(url_for('index'))

#copy paste

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Wrong username or password!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)