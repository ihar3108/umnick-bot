from sqlalchemy import create_engine, Column, BigInteger, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime as dt

engine = create_engine("sqlite:///umnick.db", pool_pre_ping=True, echo=False)
Session  = sessionmaker(bind=engine, expire_on_commit=False)
Base     = declarative_base()

class User(Base):
    __tablename__ = "users"
    uid        = Column(BigInteger, primary_key=True)
    full_name  = Column(String)
    username   = Column(String)
    score      = Column(Integer, default=0)
    ref        = Column(BigInteger)               # кто пригласил
    created    = Column(DateTime, default=dt.datetime.utcnow)

class Payout(Base):
    __tablename__ = "payouts"
    id      = Column(Integer, primary_key=True, autoincrement=True)
    uid     = Column(BigInteger)
    amount  = Column(Integer)                     # в баллах
    wallet  = Column(String)                      # TON-кошелёк
    status  = Column(String, default="pending")   # pending / done
    created = Column(DateTime, default=dt.datetime.utcnow)

Base.metadata.create_all(engine)
def add_score(uid: int, points: int):
    """Безопасно прибавляет баллы пользователю."""
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    with Session() as s:
        user = s.get(User, uid)
        if user:
            user.score += points
            s.commit()