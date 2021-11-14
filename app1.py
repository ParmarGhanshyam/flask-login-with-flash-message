from flask import Flask,render_template,redirect,url_for,session,jsonify,flash
from flask_sqlalchemy import SQLAlchemy,request
from werkzeug.wrappers.response import Response
app = Flask(__name__) #creating the Flask class object   
app.secret_key = "Hardik"  
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ghp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class ghp(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    un = db.Column(db.String(80), unique=True, nullable=False)
    pd = db.Column(db.String(30),nullable = False)

    # def __repr__(self) -> str:
    #     return f"{self.sno} - {self.Uname} - {self.Passwd}"


@app.route('/')  
def home():  
    return render_template('home.html')   

@app.route('/login',methods = ['GET','POST'])
#@app.route('/login')  
def login():
    if request.method == "POST":
        # session['un'] = request.form['un']
        
        un1 = request.form['username']
        pw = request.form['password'] 
        
        print(un1,pw)
        mytodo = ghp.query.filter_by(un=un1,pd= pw).first()

        if mytodo is not None:
            flash("you have been login sucessfully","info")
            return render_template('Message.html',username = un1,password = pw)   
        else:
            flash("Not Log in","info")
            return render_template('login.html',username = un1,password = pw)
        print(mytodo)     
    mytodo = ghp.query.all()
    return render_template('login.html',mytodo = mytodo)

@app.route('/sign_up',methods = ['GET','POST'])
def sign_up():
    if request.method=="POST":
        un = request.form['username']
        pw = request.form['password']
        print(un,pw)
        try:
            flash("register Sucessfully","sucess")   
            myfunc = ghp(un = un,pd = pw)
            db.session.add(myfunc)
            db.session.commit()
            return render_template('login.html',username = un,password = pw)
            
        except Exception as e:
            flash("Not Register","info")
            return render_template('Message.html',username = un,password = pw)
            
    mytodo1 = ghp.query.all()
    return render_template('sign_up.html',mytodo1 = mytodo1)

@app.route('/Message')
def dashboard():
    return render_template('Message.html')

@app.route('/data',methods = ['GET','POST'])
def data():
    # data = {"Key": []}
    my_dict = {"sno":[],"Username":[],"Password":[]}
    try:
        alltodo = ghp.query.all()
        print("hello",alltodo)

        for i in alltodo:
            my_dict["sno"].append(i.sno)
            my_dict["Username"].append(i.un)
            my_dict["Password"].append(i.pd)
        return my_dict
    except Exception as e:
        print(e)
        return "Hello"


if __name__ == '__main__':  
    app.run(debug = True,port = 5000) 