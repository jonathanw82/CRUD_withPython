from flask import Flask, render_template, request
from bson.objectid import ObjectId
import os
import env
import pymongo


app = Flask(__name__)


# SET UP - WHAT CLUSTER/SEVER - WHAT DATABASE - WHAT COLLECTION
MONGO_URI = os.environ.get("MONGO_URI")      # What machine to speak to, who I am and my password (+ what database I want to deal with)
DBS_NAME = "myFirstMDB"                      # What database (serie of "tables")
COLLECTION_NAME = "movies"                   # What collection (what table)


# CONNECTING TO IT
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


# REPRESENTS THE DATABASE SERVER
conn = mongo_connect(MONGO_URI)
# REPRESENTS THE COLLECTION
coll = conn[DBS_NAME][COLLECTION_NAME]


@app.route("/")
def home():
    return render_template('hello.html')


# CRUD - Create, Read, Update, Delete


# CREATE
@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == 'GET':
        return render_template('create.html')

    if request.method == 'POST':
        # GET THE DATA FROM MY FORM (COMING FROM THE CLIENT)
        title = request.form['title']
        release_year = request.form['release_year']
        synopsis = request.form['synopsis']

        # BUILD MY NEW DOC TO CREATE
        my_wonderful_new_document = {'title': title,
                                     'release_year': release_year,
                                     'synopsis': synopsis}

        # SEND IT TO THE DATABASE
        coll.insert_one(my_wonderful_new_document)

        return render_template('created.html', document=my_wonderful_new_document)


# READ
@app.route("/read")
def read():
    documents = coll.find()
    return render_template('read.html', documents=documents)


# UPDATE
@app.route("/update")
def update():

    # What doc do I want to target for an update ?
    id_ = "..."
    what_doc = {'_id': ObjectId(id_)}

    # What is the new content for that document ?
    doc_content = {'title': 'Pulp Fiction',
                   'release_year': '1984',
                   'synopsis': 'A gangster movie'}

    # update it
    coll.update(what_doc, doc_content)

    return render_template('update.html')


# DELETE
@app.route('/delete')
def delete():

    # What doc do I want to target for an update ?
    id_ = "..."
    what_doc = {'_id': ObjectId(id_)}

    # remove it
    coll.remove(what_doc)

    return render_template('delete.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)