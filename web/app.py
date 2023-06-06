from flask import Flask, redirect, url_for, render_template, request, send_from_directory, session ,flash
from flask_sqlalchemy import SQLAlchemy
import yaml
from werkzeug.utils import secure_filename
import os

with open('config.json', 'r') as c:
    data = yaml.safe_load(c)["data"]

local_server=True    

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['UPLOAD_FOLDER'] = data['upload_location']

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = data['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = data['prod_uri']
    
    
db = SQLAlchemy()
db.init_app(app)


class Details(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(14), nullable=False)
    secondary = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String, nullable=False)
    confirm = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    services = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)



@app.route('/')

def index():
    return render_template("index.html")


@app.route('/dormitories')
def dormitories():
    return render_template('dormitories.html')


@app.route('/home_stay')
def home_stay():
    return render_template('home_stay.html')


@app.route('/local_workforce')
def local_workforce():
    return render_template('local_workforce.html')


@app.route('/plantation_crops')
def plantation_crops():
    return render_template('plantation _crops.html')


@app.route('/resorts')
def resorts():
    return render_template('resorts.html')


@app.route('/tent_camping')
def tent_camping():
    return render_template('tent_camping.html')


@app.route('/transport')
def transport():
    return render_template('transport.html')


@app.route('/where_to_stay')
def where_to_stay():
    return render_template('where_to_stay.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if (request.method == 'POST'):
        f = request.files('file1')
        f.save(os.path.join(app.config['UPLOAD_FOLDER']))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if(request.method == 'POST'):
        name = request.form.get('name')
        address = request.form.get('address')
        contact = request.form.get('contact')
        secondary = request.form.get('secondary')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        services = request.form.get('services')
        year = request.form.get('year')
                                                 
        entry = Details(name=name, address=address, contact=contact, secondary = secondary, password=password, confirm=confirm, email=email, services=services, year=year  )
        
        db.session.add(entry)
        db.session.commit()
        
        
    return render_template('register.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/view')
def view():
    return render_template('view.html')


@app.route("/admin",  methods = ['GET', 'POST'])
def admin():
    error = None
    if request.method=="POST":
        username = request.form.get("username")       
        userpass = request.form.get("password")
        if ( username == data['admin_username'] and userpass == data['admin_password'] ):
            return redirect(url_for('dash'))
            #HAVE TO ADD SESSION AND ADMIN DASHBOARD and change redirect to render_template  
        else:
            error=data['error']
    return render_template('admin.html', data=data , error=error)


@app.route('/dash', methods=["GET" ,"POST"])
def dash():
    
    list = Details.query.filter_by().all()
    return render_template('dash.html', list=list)


@app.route('/confirm')
def confirm():
    return render_template('confirm.html')


@app.route('/<text>', methods=['GET', 'POST'])
def all_routes(text):
    return redirect(url_for('index'))


if __name__ == ("__main__"):
    app.run(debug=True)
