from sqlalchemy.orm import Session
import models, schemas

def get_filmes(db: Session):
    return db.query(models.Filme).all()

def get_filme(db: Session, filme_id: int):
    return db.query(models.Filme).filter(models.Filme.id == filme_id).first()

def create_filme(db: Session, filme: schemas.FilmeCreate):
    db_filme = models.Filme(**filme.dict())
    db.add(db_filme)
    db.commit()
    db.refresh(db_filme)
    return db_filme

def delete_filme(db: Session, filme_id: int):
    filme = db.query(models.Filme).filter(models.Filme.id == filme_id).first()
    if filme:
        db.delete(filme)
        db.commit()
    return filme

def update_filme(db: Session, filme_id: int, filme_data: schemas.FilmeCreate):
    filme = db.query(models.Filme).filter(models.Filme.id == filme_id).first()
    if filme:
        for key, value in filme_data.dict().items():
            setattr(filme, key, value)
        db.commit()
        db.refresh(filme)
    return filme
