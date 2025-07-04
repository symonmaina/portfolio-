from flask import Flask,render_template

app=Flask(__name__)

@app.route("/")
def home_page():
    
    return render_template("home.html")

@app.route("/projects")
def projects_page():
    
    return render_template("projects.html")
@app.route("/contact")
def contact_page():
    
    return render_template("contact.html")


if __name__=="__main__":
    app.run(debug=True)