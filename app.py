from flask import Flask

"""initializing the flask app."""
app=Flask(__name__)
""" Creating a route for homepage."""
@app.route("/")   ### Homepage
def homepage_message():
    return "Welcome to the homepage!"

@app.route("/affirmation")  ### Affirmation page.
def affirmation_message():
    return "You are hardworking"


if __name__=="__main__":
    app.run()