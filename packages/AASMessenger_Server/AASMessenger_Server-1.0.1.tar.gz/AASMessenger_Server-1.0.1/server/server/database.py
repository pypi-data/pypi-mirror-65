import datetime

from sqlalchemy import create_engine, Column, Integer, String, \
    ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ServerDataBase:
    '''
    Класс - оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется декларативный подход.
    '''

    Base = declarative_base()

    class AllUsers(Base):
        '''Класс - отображение таблицы всех пользователей.'''
        __tablename__ = 'all_users'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        last_login = Column(DateTime)
        passwd_hash = Column(String)
        pubkey = Column(Text)

        def __init__(self, username, passwd_hash):
            self.name = username
            self.last_login = datetime.datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None
            self.id = None

    class ActiveUsers(Base):
        '''Класс - отображение таблицы активных пользователей.'''
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'), unique=True)
        ip_address = Column(String)
        port = Column(Integer)
        login_time = Column(DateTime)

        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    class LoginHistory(Base):
        '''Класс - отображение таблицы истории входов.'''
        __tablename__ = 'login_history'
        id = Column(Integer, primary_key=True)
        name = Column(String, ForeignKey('all_users.id'))
        date_time = Column(DateTime)
        ip = Column(String)
        port = Column(String)

        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    class UsersContacts(Base):
        '''Класс - отображение таблицы контактов пользователей.'''
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('all_users.id'))
        contact = Column(ForeignKey('all_users.id'))

        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class UsersHistory(Base):
        '''Класс - отображение таблицы истории действий.'''
        __tablename__ = 'history'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('all_users.id'))
        sent = Column(Integer)
        accepted = Column(Integer)

        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        # Создаём движок базы данных:
        self.engine = create_engine(f'sqlite:///{path}',
                                    echo=False,
                                    pool_recycle=7200,
                                    connect_args={
                                        'check_same_thread': False})
        self.Base.metadata.create_all(self.engine)

        # Создаём сессию:
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Если в таблице активных пользователей есть записи,
        # то их необходимо удалить
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port, key):
        '''
        Метод выполняющийся при входе пользователя,
        записывает в базу факт входа.
        Обновляет открытый ключ пользователя при его изменении.
        '''
        # Запрос в таблицу пользователей на наличие там пользователя с таким
        # именем
        rez = self.session.query(self.AllUsers).filter_by(name=username)

        # Если имя пользователя уже присутствует в таблице,
        # обновляем время последнего входа и проверяем корректность ключа.
        # Если клиент прислал новый ключ, сохраняем его:
        if rez.count():
            user = rez.first()
            user.last_login = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
        # Если нету, то генерируем исключение:
        else:
            raise ValueError('Пользователь не заврегистрирован.')

        # Теперь можно создать запись в таблицу активных пользователей
        # о факте входа:
        new_active_user = self.ActiveUsers(user.id, ip_address, port,
                                           datetime.datetime.now())
        self.session.add(new_active_user)

        # И сохранить в историю входов:
        history = self.LoginHistory(user.id, datetime.datetime.now(),
                                    ip_address, port)
        self.session.add(history)

        self.session.commit()

    def add_user(self, name, passwd_hash):
        '''
        Метод регистрации пользователя.
        Принимает имя и хэш пароля, создаёт запись в таблице статистики.
        '''
        user_row = self.AllUsers(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.UsersHistory(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    def remove_user(self, name):
        '''Метод удаляющий пользователя из базы.'''
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        self.session.query(self.AllUsers).filter_by(user=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(name=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(
            self.UsersContacts).filter_by(contact=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
        self.session.query(self.AllUsers).filter_by(name=name).delete()
        self.session.commit()

    def get_hash(self, name):
        '''Метод получения хэша пароля пользователя.'''
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.passwd_hash

    def get_pubkey(self, name):
        '''Метод получения публичного ключа пользователя.'''
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.pubkey

    def check_user(self, name):
        '''Метод проверяющий существование пользователя.'''
        if self.session.query(self.AllUsers).filter_by(name=name).count():
            return True
        else:
            return False

    def user_logout(self, username):
        '''Метод фиксирующий отключения пользователя.'''
        # Запрашиваем пользователя, что покидает нас:
        user = self.session.query(self.AllUsers).filter_by(
            name=username).first()
        # Удаляем его из таблицы активных пользователей:
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        self.session.commit()

    def process_message(self, sender, recipient):
        '''Метод записывающий в таблицу статистики факт передачи сообщения.'''
        # Получаем ID отправителя и получателя:
        sender = self.session.query(self.AllUsers).filter_by(
            name=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(
            name=recipient).first().id
        # Запрашиваем строки из истории и увеличиваем счётчики:
        sender_row = self.session.query(self.UsersHistory).filter_by(
            user=sender).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UsersHistory).filter_by(
            user=recipient).first()
        recipient_row.accepted += 1

        self.session.commit()

    # Функция добавляет контакт для пользователя:
    def add_contact(self, user, contact):
        '''Метод добавления контакта для пользователя.'''
        # Получаем ID пользователей
        user = self.session.query(self.AllUsers).filter_by(
            name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(
            name=contact).first()

        # Проверяем что не дубль и что контакт может существовать (полю
        # пользователь мы доверяем):
        if not contact or self.session.query(self.UsersContacts).filter_by(
                user=user.id, contact=contact.id).count():
            return

        # Создаём объект и заносим его в базу:
        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_contact(self, user, contact):
        '''Метод удаления контакта пользователя.'''
        # Получаем ID пользователей:
        user = self.session.query(self.AllUsers).filter_by(
            name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(
            name=contact).first()

        # Проверяем что контакт может существовать (полю пользователь мы
        # доверяем):
        if not contact:
            return

        # Удаляем требуемое:
        self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id
        ).delete()
        self.session.commit()

    def users_list(self):
        '''
        Метод возвращающий список известных пользователей
        со временем последнего входа.
        '''
        # Запрос строк таблицы пользователей:
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login
        )
        # Возвращаем список кортежей:
        return query.all()

    def active_users_list(self):
        '''Метод возвращающий список активных пользователей.'''
        # Запрашиваем соединение таблиц
        # и собираем кортежи имя, адрес, порт, время:
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.AllUsers)
        # Возвращаем список кортежей:
        return query.all()

    def login_history(self, username=None):
        '''Метод возвращающий историю входов.'''
        # Запрашиваем историю входа:
        query = self.session.query(
            self.AllUsers.name,
            self.LoginHistory.date_time,
            self.LoginHistory.ip,
            self.LoginHistory.port,
        ).join(self.AllUsers)
        # Если было указано имя пользователя, то фильтруем по нему:
        if username:
            query = query.filter(self.AllUsers.name == username)
        # Возвращаем список кортежей:
        return query.all()

    def get_contacts(self, username):
        '''Метод возвращающий список контактов пользователя.'''
        # Запрашивааем указанного пользователя:
        user = self.session.query(self.AllUsers).filter_by(
            name=username).one()

        # Запрашиваем его список контактов:
        query = self.session.query(self.UsersContacts, self.AllUsers.name). \
            filter_by(user=user.id). \
            join(self.AllUsers, self.UsersContacts.contact == self.AllUsers.id)

        # Выбираем только имена пользователей и возвращаем их:
        return [contact[1] for contact in query.all()]

    def message_history(self):
        '''Метод возвращающий статистику сообщений.'''
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.AllUsers)
        # Возвращаем список кортежей:
        return query.all()

# Отладка:
if __name__ == '__main__':
    test_db = ServerDataBase('../../server_database.db3')
    test_db.user_login('test1', '192.168.1.113', 8080, 'jhgfd')
    test_db.user_login('test2', '192.168.1.113', 8081, 'kjfyd')
    print(test_db.users_list())
    # print(test_db.active_users_list())
    # test_db.user_logout('McG')
    # print(test_db.login_history('re'))
    # test_db.add_contact('test2', 'test1')
    # test_db.add_contact('test1', 'test3')
    # test_db.add_contact('test1', 'test6')
    # test_db.remove_contact('test1', 'test3')
    test_db.process_message('test1', 'test2')
    print(test_db.message_history())