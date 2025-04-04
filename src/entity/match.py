from sqlalchemy import Column, Integer, String
from core.database import Base

class MatchEntity(Base):
    __tablename__ = 'match'
    __table_args__ = { 'extend_existing': True }

    id = Column(Integer, primary_key = True, autoincrement = True)
    match_id = Column(Integer, nullable = True, unique = True) # id from API
    home_team = Column(String(20), nullable = False)
    away_team = Column(String(20), nullable = False)
    shots_on_goal = Column(Integer, nullable = False)
    finishes = Column(Integer, nullable = True)
    corners = Column(Integer, nullable = False)
    goals = Column(Integer, nullable = False)
    winner = Column(Integer, nullable = False)
