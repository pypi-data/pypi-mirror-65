import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
# Для использования декларативного стиля необходима функция declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import POOL_RECYCLE


class ClientDB:
    base = declarative_base()

    # таблица со списком контактов
    class Contacts(base):
        __tablename__ = 'Contacts'
        id = Column(Integer, primary_key=True)
        username = Column(String)

        def __init__(self, username):
            self.username = username

        def __repr__(self):
            return f'<User({self.username})>'

    # таблица истории сообщений
    class MessagesHistory(base):
        __tablename__ = 'Messages_history'
        id = Column(Integer, primary_key=True)
        contact = Column(String)
        direction = Column(String)
        message = Column(Text)
        date = Column(DateTime)

        def __init__(self, contact, direction, message, date):
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = date

        def __repr__(self):
            return f'<User({self.contact}, {self.direction}, {self.message}, {self.date})>'

    def __init__(self, name):
        self.engine = create_engine(f'sqlite:///client_{name}.db3', echo=False, pool_recycle=POOL_RECYCLE,
                                    connect_args={'check_same_thread': False})

        # Создаём таблицы
        self.base.metadata.create_all(self.engine)

        session = sessionmaker(bind=self.engine)
        self.session = session()

        # при запуске БД очищаем список контактов
        self.session.query(self.Contacts).delete()
        self.session.commit()

    # Функция добавления списка контактов при подключении базы
    def fill_contacts(self, contacts):
        for contact in contacts:
            self.add_contact(contact)

    # Функция добавления нового контакта
    def add_contact(self, contact):
        if not self.session.query(self.Contacts).filter_by(username=contact).count():
            new_contact = self.Contacts(contact)
            self.session.add(new_contact)
            self.session.commit()

    # Функция удаления контакта
    def del_contact(self, contact):
        self.session.query(self.Contacts).filter_by(username=contact).delete()
        self.session.commit()

    # Функция, сохраняющяя сообщения
    def save_message(self, contact, direction, message):
        new_message = self.MessagesHistory(contact, direction, message, datetime.datetime.now())
        self.session.add(new_message)
        self.session.commit()

    # Функция возвращающяя контакты
    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacts.username).all()]

    # Функция возвращающая историю переписки
    def get_history(self, contact):
        query = self.session.query(self.MessagesHistory).filter_by(contact=contact)
        return [
            [history_row.contact,
             history_row.direction,
             history_row.message,
             history_row.date.strftime("%Y-%m-%d-%H.%M.%S")]
            for history_row in query.all()
        ]
        # return query.all()


if __name__ == '__main__':
    test_db = ClientDB('test1')
    # test_db.add_contact('test1')
    # test_db.del_contact('n')
    # test_db.save_message('test1', 'in', 'in_msg')
    # print(test_db.get_history('test1'))
    print(test_db.get_contacts())
