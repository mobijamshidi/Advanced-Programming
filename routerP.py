from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ProfessorBase, ProfessorCreate, ProfessorEdit
from crud import create_professor_db, delete_professor_db, update_professor_db
from database import get_db
import models

router = APIRouter()

@router.post("/professors/RegProf/", response_model=ProfessorBase)
def create_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    return create_professor_db(db=db, professor=professor)

@router.get("/professors/{professor_id}")
def read_professor(professor_id: int, db: Session = Depends(get_db)):
    professor_db = db.query(models.Professor).filter(models.Professor.id == professor_id).first()
    if professor_db is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor_db

@router.put("/professors/EditProf/{professor_id}", response_model=ProfessorBase)
def update_professor(professor_id: int, professor: ProfessorEdit, db: Session = Depends(get_db)):
    db_professor = update_professor_db(db=db, professor_id=professor_id, professor_data=professor)
    if not db_professor:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_professor

@router.delete("/professors/DelProf/{professor_id}")
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    result = delete_professor_db(db=db, PID=professor_id)
    if not result:
        raise HTTPException(status_code=404, detail="Professor not found")
    return {"message": "Professor deleted successfully"}
