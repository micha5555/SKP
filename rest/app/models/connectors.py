from app.db import db
from app.models.notPaidCaseModel import NotPaidCase
from app.models.problematicCaseModel import ProblematicCase

user_notPaidCase = db.Table(
  "user_notPaidCase",
  db.Model.metadata,
  db.Column("userId", db.Integer, db.ForeignKey("user.id")),
  db.Column("notPaidCaseId", db.Integer, db.ForeignKey("not_paid_case.id")),
)

user_problematicCase = db.Table(
  "user_problematicCase",
  db.Model.metadata,
  db.Column("userId", db.Integer, db.ForeignKey("user.id")),
  db.Column("problematicCaseId", db.Integer, db.ForeignKey("problematic_case.id")),
)

