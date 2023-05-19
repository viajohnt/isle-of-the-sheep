from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///game.db')
Session = sessionmaker(bind=engine)
session = Session()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer(), primary_key=True)
    username = Column(String())

    scores = relationship('Score', backref='player')

    def __repr__(self):
        return f'<Player {self.id}: {self.username}>'

class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())

    player_id = Column(Integer(), ForeignKey('players.id'))

    def __repr__(self):
        return f'<Score {self.id}: {self.score}>'

Base.metadata.create_all(engine)


