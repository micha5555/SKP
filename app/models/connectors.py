from app.db import db

user_not_paid_case_association = db.Table('user_not_paid_case',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('not_paid_case_id', db.Integer, db.ForeignKey('not_paid_case.id'))
)

user_problematic_case_association = db.Table('user_problematic_case',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('problematic_case_id', db.Integer, db.ForeignKey('problematic_case.id'))
)
