from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import StudentBase, StudentCreate, StudentEdit
from crud import create_student_db, delete_student_db, update_student_db
from database import get_db
import models

router = APIRouter()

@router.post("/students/RegStu/", response_model=StudentBase)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student_db(db=db, student=student)

@router.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student_db = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student_db is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_db

@router.put("/students/EditStu/{student_id}", response_model=StudentBase)
def update_student(student_id: int, student: StudentEdit, db: Session = Depends(get_db)):
    db_student = update_student_db(db=db, student_id=student_id, student_data=student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/students/DelStu/{STID}")
def delete_student(STID: str, db: Session = Depends(get_db)):
    result = delete_student_db(db=db, STID=STID)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
