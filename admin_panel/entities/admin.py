from admin_panel.database import db_admins
from admin_panel.exception.admin import AdminExistsError, AdminLimitError
from admin_panel.panel import core


class Admin:

    @classmethod
    def count(cls):
        return len(db_admins.get_all())

    @classmethod
    def is_new(cls, admin_id):
        if db_admins.get(["*"], ["admin_id", int(admin_id)]):
            return False
        return True

    @classmethod
    def add(cls, admin_id):
        if not cls.is_new(admin_id=admin_id):
            raise AdminExistsError
        if cls.count() >= 5:
            raise AdminLimitError
        db_admins.insert({
            "admin_id": int(admin_id)
        })

    @classmethod
    def delete(cls, admin_id):
        if cls.is_new(admin_id):
            raise AdminExistsError
        db_admins.delete(["admin_id", int(admin_id)])

    @classmethod
    def admins(cls):
        admins = [i[0] for i in db_admins.get_all()]
        admins.append(core.main_admin)
        return admins