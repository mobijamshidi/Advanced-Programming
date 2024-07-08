from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import CourseBase, CourseEdit
from crud import create_course_db, delete_course_db, update_course_db
from database import get_db
import models

router = APIRouter()

@router.post("/courses/RegCourse/", response_model=CourseBase)
def create_course(course: CourseBase, db: Session = Depends(get_db)):
    return create_course_db(db=db, course=course)

@router.get("/courses/{course_id}")
def read_course(course_id: int, db: Session = Depends(get_db)):
    course_db = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course_db is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_db

@router.put("/courses/EditCourse/{course_id}", response_model=CourseBase)
def update_course(course_id: int, course: CourseEdit, db: Session = Depends(get_db)):
    db_course = update_course_db(db=db, course_id=course_id, course_data=course)
    if not db_course:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_course

@router.delete("/courses/DelCourse/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    result = delete_course_db(db=db, CID=course_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}
