import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
    __tablename__ = 'image'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)

class Topic(Base):
    __tablename__ = 'topic'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.Text, nullable=False)
    image_id = sa.Column(sa.Integer, sa.ForeignKey('image.id'), nullable=False)
    image = sa.orm.relationship(Image)  # inner join=True для JOIN
    questions = sa.orm.relationship('Question')
    users = sa.orm.relationship('User', secondary='topic_user')
    # association
    # users = sa.orm.relationship('TopicUser', back_populates='topic')


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)
    # association
    # topics = sa.orm.relationship('TopicUser', back_populates='user')


class TopicUser(Base):
    __tablename__ = 'topic_user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    topic_id = sa.Column(sa.Integer, sa.ForeignKey('topic.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    role = sa.Column(sa.Text)
    # association
    # user = sa.orm.relationship(User, back_populates='topics')
    # topic = sa.orm.relationship(Topic, back_populates='users')


class Question(Base):
    __tablename__ = 'question'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text = sa.Column(sa.Text)
    topic_id = sa.Column(sa.Integer, sa.ForeignKey('topic.id'), nullable=False)
    topic = sa.orm.relationship(Topic)  # inner join = True для использования JOIN вместо LEFT JOIN



from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
import json

with open("data.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)

engine = None
try:
    # pip install psycopg
    # pip install --upgrade pip
    # pip install "psycopg[binary,pool]"
    engine = sa.create_engine(f"postgresql+psycopg://{data['user']}:{data['password']}@{data['host']}/{data['database']}",
        echo=True,  # Включаем SQL логирование для отладки
        pool_size=5,  # Устанавливаем размер пула соединений
        max_overflow=10  # Максимальное количество дополнительных соединений
    )
    print(f"PostgreSQL: Соединение с БД на {data['host']} созданно успешно !")
except Exception as e:
    print(f"Error: Ошибка создания базы данных: Исключение - {e}")

DBSession = sessionmaker(binds=engine, expire_on_commit=False,)

@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations."""
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == '__main__':
    s = session_scope()
    # Пример 1
    # Хотим получить десять последних вопросов из определенного топика.
    '''
            SELECT *
            FROM question
            WHERE topic_id = 1
            ORDER BY id DESC
            LIMIT 10;
    '''
        
    # Чтобы добиться такого запроса в алхимии:

    t1_id = 1  # Заменить на id топика из вашего базы

    #questions = s.query(Question).filter(
    questions = s.select(Question).filter(
            Question.topic_id == t1_id,
    ).order_by(Question.id.desc()).limit(10).all()        

    print(f"Пример 1: {questions}")




