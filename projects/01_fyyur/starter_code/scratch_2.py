from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
# some lab stiff related to db operation s
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sven@localhost:5432/lab'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    cases = db.relationship('Cases', backref='users')


    def __repr__(self):
        return '<User %r>' % self.last_name


    def insertUser(self):

        try:
            db.session.add(self)
            db.session.commit()
            id = self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return id

    def updateUser(self, payload):

        updData = Users.query.filter_by(id=payload.id).first()

        try:
            updData.first_name = payload.first_name
            updData.last_name = payload.last_name
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return id

    def deleteUser(self, payload):
        try:
            Users.query.filter_by(id=payload.id).delete()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

class Cases(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    case_action = db.relationship('CaseAction', backref='cases')

    def __repr__(self):
        return '<Case %r>' % self.id

class CaseAction(db.Model):
    __tablename__ = 'caseaction'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key= True, nullable=False)
    comment = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<CaseAction %r>' % self.id


db.create_all()

user = Users()

user.last_name = 'Kuehn'
user.first_name = 'Johanna'

user.id = user.insertUser()
user.id = 34
user.first_name = 'Johannes'
user.last_name = 'Kühn'

user.updateUser(user)
user.id = 33
user.deleteUser(user)

result = db.session.query(Users.last_name).filter(Users.last_name == 'Kuehn' ).group_by(Users.last_name).all()
print(result[0])

aUser = Users()
aCase = Cases()
aCase.subject = 'ToDo'
aCase.description = 'This is a really bade Case we have here '
aUser.last_name = 'Case User'
aUser.cases = [aCase]

db.session.add(aUser)
db.session.commit()
