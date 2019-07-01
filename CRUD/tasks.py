from CRUD import celery, cache, logger
from CRUD.models import *

@celery.task(name='tasks.insertThroughCelery')
def insertThroughCelery(name, author, uui):
    try:
        book = Book(
            name=name,
            author=author,
            jobid=uui,
        )
        db.session.add(book)
        db.session.commit()
        # To update in cache
        books = Book.query.all()
        for book in books:
            cache.set(str(book.id), book)
        return "Book has been added asynchronously. book id={}".format(book.id)
    except Exception as e:
        return logger.exception("Exception occurred during insertion")




@celery.task(name='tasks.updateThroughCelery')
def updateThroughCelery(name1, author1, id1, t):
    try:
        if name1:
            Book.query.filter_by(id=id1).update({Book.name: name1} , synchronize_session=False)
        if author1:
            Book.query.filter_by(id=id1).update({Book.author: author1}, synchronize_session=False)
        Book.query.filter_by(id=id1).update({Book.jobid: t}, synchronize_session=False)
        db.session.commit()
        # Updating the cache
        books = Book.query.filter_by(id=id1).all()
        cache.set(id1, books)
        return "Book has been updated asynchronously. book id={}".format(id1)
    except Exception as e:
        return logger.exception("Exception occurred during updation")



@celery.task(name='tasks.deleteThroughCelery')
def deleteThroughCelery(id1):
    try:
        book = Book.query.filter_by(id=id1).first()
        db.session.delete(book)
        db.session.commit()
        #updating the cache
        cache.delete(id1)
        return "Book has been deleted asynchronously. book id={}".format(id1)
    except Exception as e:
        return logger.exception("Exception occurred during deletion")

