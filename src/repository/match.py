from sqlalchemy.orm import Session
from entity.match import MatchEntity

class MatchEntityRepository:

    @staticmethod
    def find_all(db: Session) -> list[MatchEntity]:
        return db.query(MatchEntity).all()

    @staticmethod
    def save(db: Session, match: MatchEntity) -> MatchEntity:
        if match.id:
            db.merge(match)
        else:
            db.add(match)
        db.commit()
        return match

    @staticmethod
    def find_by_id(db: Session, id: int) -> MatchEntity:
        return db.query(MatchEntity).filter(MatchEntity.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(MatchEntity).filter(MatchEntity.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        match = db.query(MatchEntity).filter(MatchEntity.id == id).first()
        if match is not None:
            db.delete(match)
            db.commit()
