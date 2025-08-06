from flask import Flask, render_template, request, redirect, jsonify
import json
import random
import string

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        otp = request.form.get('otp')

        if otp != "123456":
            return "❌ Invalid OTP", 400

        with open("database.json", "r+") as db:
            try:
                data = json.load(db)
            except:
                data = []

            data.append({
                "email": email,
                "password": password
            })
            db.seek(0)
            json.dump(data, db, indent=2)

        return "✅ Registration Successful"
    
    return render_template("register.html")

@app.route('/')
def home():
    return redirect('/register')

if __name__ == '__main__':
    app.run(port=7700)
