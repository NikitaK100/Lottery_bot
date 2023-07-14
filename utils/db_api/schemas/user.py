from sqlalchemy import BigInteger, Column, String, Integer
from utils.db_api.db_gino import db
from sqlalchemy import sql


class User(db.Model):
    __tablename__ = "GINO_ORM"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    wallet = Column(BigInteger)

    query: sql.Select


class Participants(db.Model):

    __tablename__ = 'users_lottery'

    index_id = Column(Integer)
    id = Column(Integer, primary_key=True)
    id_admin = Column(BigInteger)
    name = Column(String(50))
    description = Column(String(500))
    photo = Column(String(250))
    quantity = Column(Integer)
    price = Column(Integer)

    query: sql.Select


class PurchaseLottery(db.Model):
    __tablename__ = 'purchases_lottery'

    id = Column(BigInteger)
    lottery_id = Column(Integer)
    name = Column(String(100))

    query: sql.Select



























