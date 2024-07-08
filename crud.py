from fastapi import HTTPException
from sqlalchemy.orm import Session
import schemas
import models

def create_student_db(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        sSTID=student.sSTID,
        sFName=student.sFName,
        sLName=student.sLName,
        sFather=student.sFather,
        sBirth=student.sBirth,
        sIDS=student.sIDS,
        sBornCity=student.sBornCity,
        sAddress=student.sAddress,
        sPostalCode=student.sPostalCode,
        sCPhone=student.sCPhone,
        sHPhone=student.sHPhone,
        sDepartment=student.sDepartment,
        sMajor=student.sMajor,
        smarried=student.sMarried,
        sID=student.sID,
        sSCourseIDs=student.sSCourseIDs,
        sLIDs=student.sLIDs,
    )

    courses = db.query(models.Course).all()
    course_ids = [course.cCID for course in courses]
    
    for sSCourseID in student.sSCourseIDs:
        if sSCourseID not in course_ids:
            course_names = [course.cCName for course in courses]
            raise HTTPException(status_code=400, detail=f"There is no course with ID {sSCourseID} in courses list {course_names}")

    professors = db.query(models.Professor).all()
    professor_ids = [professor.pPID for professor in professors]

    for sLID in student.sLIDs:
        if sLID not in professor_ids:
            professor_names = [f"{professor.pFName} {professor.pLName}" for professor in professors]
            raise HTTPException(status_code=400, detail=f"There is no professor with ID {sLID} in professor list {professor_names}")

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student_db(db: Session, student_id: int, student_data: schemas.StudentEdit):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        return None
    for var, value in vars(student_data).items():
        if value is not None:
            setattr(db_student, var, value)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student_db(db: Session, STID: str):
    db_student = db.query(models.Student).filter(models.Student.sSTID == STID).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

def create_professor_db(db: Session, professor: schemas.ProfessorCreate):
    db_professor = models.Professor(
        pPID=professor.pPID,
        pFName=professor.pFName,
        pLName=professor.pLName,
        pBirth=professor.pBirth,
        pBornCity=professor.pBornCity,
        pAddress=professor.pAddress,
        pPostalCode=professor.pPostalCode,
        pCPhone=professor.pCPhone,
        pHPhone=professor.pHPhone,
        pDepartment=professor.pDepartment,
        pMajor=professor.pMajor,
        pID=professor.pID,
        pPCourseIDs=professor.pPCourseIDs
    )

    courses = db.query(models.Course).all()
    course_ids = [course.cCID for course in courses]
    
    for PCourseID in professor.pPCourseIDs:
        if PCourseID not in course_ids:
            course_names = [course.cCName for course in courses]
            raise HTTPException(status_code=400, detail=f"There is no course with ID {PCourseID} in courses list {course_names}")


    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def update_professor_db(db: Session, professor_id: int, professor_data: schemas.ProfessorEdit):
    db_professor = db.query(models.Professor).filter(models.Professor.id == professor_id).first()
    if not db_professor:
        return None
    for var, value in vars(professor_data).items():
        if value is not None:
            setattr(db_professor, var, value)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def delete_professor_db(db: Session, PID: int):
    db_professor = db.query(models.Professor).filter(models.Professor.pPID == PID).first()
    if db_professor:
        db.delete(db_professor)
        db.commit()
        return True
    return False

def create_course_db(db: Session, course: schemas.CourseBase):
    db_course = models.Course(
        cCID=course.cCID,
        cCName=course.cCName,
        cDepartment=course.cDepartment,
        cCredit=course.cCredit
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course_db(db: Session, course_id: int, course_data: schemas.CourseEdit):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        return None
    for var, value in vars(course_data).items():
        if value is not None:
            setattr(db_course, var, value)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course_db(db: Session, CID: int):
    db_course = db.query(models.Course).filter(models.Course.cCID == CID).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False
