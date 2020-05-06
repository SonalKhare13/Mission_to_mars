# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars = mongo.db.mars_app.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():    
    mars=mongo.db.mars_app
    # Run the scrape function (in scrape_mars.py, mars_dictionary being returned at end of scrape function)
    mars_dictionary = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars.replace_one({}, mars_dictionary, upsert=True)

    # Redirect back to home page
    #return "Scrape sucessful"
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)