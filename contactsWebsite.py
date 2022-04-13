from flask import Flask, request, render_template
import pandas as pd
import csv

df = pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\ContactList\contacts.csv", header=0)  # Make Dataframe
contacts = df[['Name', 'Phone', 'Email']].values  # Dataframe to numpy 2d array (w/o titles)
contacts = contacts.tolist()  # Make 2d numpy array to regular array
contacts.insert(0, ['Name', 'Phone', 'Email'])  # Add the titles back into the 2d array
selectRow=-1  # variable for saving the editing row
app = Flask(__name__)

def save():  # Method for saving contacts list
  with open(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\ContactList\contacts.csv", 'w') as csvfile:  # File as written mode
      csvwriter = csv.writer(csvfile)  # Create csv writing function
      rows = 0
      while rows < len(contacts):
          csvwriter.writerow(contacts[rows])  # Rewrite 2d array back into file
          rows += 1

@app.route("/")  # Home page
def home():
  return render_template("home.html")

@app.route('/view')  # Viewing contacts
def view():
  return render_template("view.html",contacts=contacts,len=len(contacts))

@app.route('/add')  # Addition form to create a new contact
def add():
  return render_template("add.html")
  
@app.route('/select')  # Selection form to select which contact edit
def edit():
  return render_template("select.html",contacts=contacts,len=len(contacts))

@app.route('/editing', methods=["POST"])  # Editing contact
def editing():
  choice=request.form["selection"]
  selectRow=int(choice)
  return render_template("editing.html",name=contacts[selectRow][0],email=contacts[selectRow][1],address=contacts[selectRow][2])    

@app.route('/delete')  # Deleting contact selection
def delete():
  return render_template("delete.html",contacts=contacts,len=len(contacts))

@app.route('/deleting', methods=["POST"])  # Deletion of said contact
def deleting():
  choice=request.form["selection"]
  deleteRow=int(choice)
  contacts.pop(deleteRow)
  save()
  return render_template("submit.html")    

@app.route('/addsubmit', methods=["POST"])  # Submitting/saving of additional contct
def addsubmit():
  name=request.form["name"]
  email=request.form["email"]
  address=request.form["address"]
  contacts.append([name,email,address])
  save()
  return render_template("submit.html")

@app.route('/editsubmit', methods=["POST"])  # Submitting/saving of edited contact
def editsubmit():
  name=request.form["name"]
  email=request.form["email"]
  address=request.form["address"]
  contacts[selectRow]=[name,email,address]
  save()
  return render_template("submit.html")

if __name__ == '__main__':
  app.run(debug = True)
