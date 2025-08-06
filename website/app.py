from flask import Flask, render_template, request, redirect, flash
import json
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "meow_secret_key"  # required for flash messages

DATABASE_FILE = "database.json"

# Ensure database file exists
if not os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, "w") as f:
        json.dump([], f)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            flash("⛔ नाव आणि ईमेल दोन्ही आवश्यक आहेत.")
            return redirect("/register")

        try:
            with open(DATABASE_FILE, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            users = []

        # Email duplication check
        for user in users:
            if user["email"].lower() == email.lower():
                flash("⚠️ हे ईमेल आधीच वापरले आहे.")
                return redirect("/register")

        # Save new user
        users.append({"name": name, "email": email})
        with open(DATABASE_FILE, "w") as f:
            json.dump(users, f, indent=4)

        flash("✅ रजिस्ट्रेशन यशस्वी झाले!")
        return redirect("/register")

    return render_template("register.html")

if __name__ == '__main__':
    app.run(port=7700)
