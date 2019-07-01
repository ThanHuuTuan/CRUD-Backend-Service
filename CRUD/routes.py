from flask import request, render_template
from CRUD import app
from CRUD.tasks import *
from CRUD.models import *

# To generate unique ids for the tasks
import uuid


# Inserting into the table
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    name = request.form['name']
    author=request.form['author']

    #Generating the job id or task id
    t=uuid.uuid1()
    # Giving the task to celery
    insertThroughCelery.delay(name, author, t)
    return render_template("taskresults.html", job=t)


# Updating the table
@app.route('/updateData', methods=['GET', 'POST'])
def updateData():
    if request.method == 'GET':
         return render_template('index.html')

    # Generating the job id or task id
    t = uuid.uuid1()
    # Giving the task to celery
    updateThroughCelery.delay(request.form['name1'], request.form['author1'], request.form['id'], t)
    return render_template("taskresults.html", job=t)


# Deleting in the table
@app.route('/deleteData', methods=['GET', 'POST'])
def deleteData():
    if request.method == 'GET':
         return render_template('index.html')

    # Generating the job id or task id
    t = uuid.uuid1()
    # Giving the task to celery
    deleteThroughCelery.delay(request.form['id'])
    return render_template("taskresults.html", job=t)


# fetching the data from the table
@app.route('/getEntry', methods=['GET', 'POST'])
def getEntry():
    if request.method == 'GET':
         return render_template('index.html')
    try:
        id = request.form['id']
        books = cache.get(id)
        # check if books contains something. If it conatains then the entry is already in a cache
        if books==None:
            books = Book.query.filter_by(id=id).all()
            cache.set(id, books)
        return render_template("home.html", books=books)
    except Exception as e:
        return logger.exception("Exception occurred during get entry")


# Showing the whole table
@app.route('/showResults', methods=['GET', 'POST'])
def showResults():
    if request.method == 'GET':
         return render_template('index.html')
    try:
        books = Book.query.all()
        return render_template("showresults.html", books=books)
    except Exception as e:
        return logger.exception("Exception occurred during showing the results")



# Check if the task is completed or not
@app.route('/taskResults', methods=['GET', 'POST'])
def taskResults():
    if request.method == 'GET':
         return render_template('index.html')

    try:
        book = Book.query.filter_by(jobid=request.form['id']).first()
        if book==None:
            return 'Task is pending or has been deleted'
        else:
            return 'Task is executed successfully ' + str(book.id) + '. ' + str(book.name) + ' (' + str(book.author) + ")"
    except Exception as e:
        return logger.exception("Exception occurred during task results")


