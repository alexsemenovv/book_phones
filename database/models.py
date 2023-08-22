from peewee import *
import os

db = SqliteDatabase(os.path.abspath(os.path.join('database', 'people.db')))


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Contact(BaseModel):
    name = CharField()  # Имя
    sec_name = CharField(null=True)  # Фамилия - не обязательное для заполнения
    patronymic = CharField(null=True)  # Отчество - не обязательное для заполнения
    company = CharField(null=True)  # Название организации - не обязательное для заполнения
    work_phone = IntegerField(null=True)  # Рабочий телефон - не обязательное для заполнения
    personal_phone = IntegerField()  # Личный телефон

    class Meta:
        db_table = 'contacts'
        order_by = 'name'