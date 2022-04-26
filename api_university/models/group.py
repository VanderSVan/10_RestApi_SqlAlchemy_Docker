from sqlalchemy import asc
from api_university.db.db_sqlalchemy import db


class GroupModel(db.Model):
    __tablename__ = "groups"

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    students = db.relationship('StudentModel',
                               backref=db.backref('group'),
                               order_by='StudentModel.student_id',
                               lazy=True)

    def __repr__(self):
        return f"GroupModel {self.group_id}"

    @classmethod
    def get_all_groups(cls):
        return cls.query.order_by(asc(cls.group_id))

    @classmethod
    def get_group_students(cls, group_id):
        return cls.query.filter_by(group_id=group_id).first().students

    @classmethod
    def find_by_name(cls, group_name):
        return cls.query.filter_by(name=group_name).first()

    @classmethod
    def find_by_id_or_404(cls, group_id):
        return cls.query.get_or_404(group_id, description=f"group '{group_id}' not found")

    @classmethod
    def not_find_by_id_or_400(cls, group_id: int) -> None:
        return cls.query.not_exists_or_400(group_id, description=f"group '{group_id}' already exists")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()