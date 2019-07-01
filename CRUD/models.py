from CRUD import db

# The name of the table would be same as the name of the class, i.e "Book"
class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    jobid=db.Column(db.String())

    def __init__(self, name, author, jobid):
        self.name = name
        self.author = author
        self.jobid = jobid

    def __repr__(self):
        return '<id {}>'.format(self.id)

# Execute it only once during the program
# db.create_all()
