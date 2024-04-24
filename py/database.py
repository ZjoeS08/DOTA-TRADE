import py.config as cfg
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    user_name = Column(String)
    status = Column(String)


def create():
    engine = create_engine(cfg.DATABASE_PATH)
    Base.metadata.create_all(engine)
    print("[DB] Создана новая таблица пользователей")


def load():
    engine = create_engine(cfg.DATABASE_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(User).all()


def save(data):
    engine = create_engine(cfg.DATABASE_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(data)
    session.commit()
    print("[DB] Данные успешно сохранены")


def is_exist(user_id):
    engine = create_engine(cfg.DATABASE_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        return True

    return False


def register(user_id, user_name):
    engine = create_engine(cfg.DATABASE_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_user = User(user_id=user_id, user_name=user_name, status=cfg.UFREE)
    session.add(new_user)
    session.commit()
    print(f"[DB] Зарегистрирован новый пользователь: {user_id}")


def update(user_id, status=None):
    engine = create_engine(cfg.DATABASE_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        if status is not None:
            user.status = status
        session.commit()


def get_user(user_id):
    engine = create_engine(cfg.DATABASE_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(User).filter_by(user_id=user_id).first()


def reset_status():
    engine = create_engine(cfg.DATABASE_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).update({User.status: cfg.UFREE})
    session.commit()
    print("[DB] Статусы пользователей сброшены")
