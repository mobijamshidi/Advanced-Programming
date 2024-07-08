# *Final Project of Advanced Programming*

*This is a project that works like a university unit selection system, as the courses are entered first, then the professors choose the courses they want to teach, and then the students choose the courses and professors they want.   Next, we will check the project codes*


## main
*To run the project, we need to run the main file to first create the tables and then connect the routers and then use uvicorn to run the API.*

```python

from fastapi import FastAPI
from database import engine, Base
from routerS import router as student_router
from routerP import router as professor_router
from routerC import router as course_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(student_router, tags=['students'])
app.include_router(professor_router, tags=['professors'])
app.include_router(course_router, tags=['courses'])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

```

## *database*
*In this file, we connect to the database we want, the database used in this project is SQLite*

```python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


```

## *models*
*When we create the database, we must have different tables and columns to save user information, we use SQLAlchemy models to create them and create the tables.*

```python

from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    sSTID = Column(String, unique=True, index=True)
    sFName = Column(String)
    sLName = Column(String)
    sFather = Column(String)
    sBirth = Column(String)
    sIDS = Column(String)
    sBornCity = Column(String)
    sAddress = Column(String)
    sPostalCode = Column(Integer)
    sCPhone = Column(Integer)
    sHPhone = Column(Integer)
    sDepartment = Column(String)
    sMajor = Column(String)
    smarried = Column(String)
    sID = Column(Integer)
    sSCourseIDs = Column(JSON)
    sLIDs = Column(JSON)

class Professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True, index=True)
    pPID = Column(Integer, unique=True, index=True)
    pFName = Column(String)
    pLName = Column(String)
    pBirth = Column(String)
    pBornCity = Column(String)
    pAddress = Column(String)
    pPostalCode = Column(Integer)
    pCPhone = Column(Integer)
    pHPhone = Column(Integer)
    pDepartment = Column(String)
    pMajor = Column(String)
    pID = Column(Integer)
    pPCourseIDs = Column(JSON)

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    cCID = Column(Integer, unique=True, index=True)
    cCName = Column(String)
    cDepartment = Column(String)
    cCredit = Column(Integer)


```


## *schemas*
*The schema file is used for data validation and different fields are validated one by one so that the answers can be managed according to the user's needs.*

```python

from typing_extensions import Annotated
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re

cities = ['تبریز', 'ارومیه', 'اردبیل', 'اصفهان', 'کرج', 'ایلام', 'بندر بوشهر', 'تهران', 'شهرکرد', 'بیرجند', 'مشهد',
          'اهواز', 'زنجان', 'سمنان', 'زاهدان', 'شیراز', 'قزوین', 'قم', 'سنندج', 'کرمان', 'کرمانشاه', 'یاسوج',
          'گرگان', 'رشت', 'خرم آباد', 'ساری', 'اراک', 'بندرعباس', 'همدان', 'یزد', 'بجنورد']

departments = ["فنی و مهندسی", "علوم پایه", "علوم انسانی", "دامپزشکی", "اقتصاد", "کشاورزی", "منابع طبیعی"]
majors = ["مهندسی برق - سامانه های برقی حمل و نقل", "مهندسی برق", "مهندسی صنایع - کیفیت و بهره وری",
          "مهندسی صنایع - مدیریت مهندسی", "مهندسی صنایع - مهندسی صنایع", "مهندسی صنایع - مدیریت سیستم و بهره وری",
          "مهندسی  صنایع", "مهندسی  پزشکی - بیوالکتریک", "مهندسی پزشکی - بیومتریال", "مهندسی پزشکی - توانبخشی",
          "مهندسی پزشکی - مهندسی توانبخشی", "مهندسی پزشکی", "مهندسی عمران - ژئوتکنیک", "مهندسی عمران - مدیریت ساخت",
          "مهندسی عمران - مهندسی راه و ترابری", "مهندسی عمران - مهندسی و مدیریت ساخت", "مهندسی عمران",
          "مهندسی فناوری اطلاعات - تجارت الکترونیکی", "مهندسی فناوری اطلاعات - شبکه های کامپیوتری",
          "مهندسی کامپیوتر - معماری سیستم های کامپیوتری", "مهندسی کامپیوتر - نرم افزار",
          "مهندسی کامپیوتر - هوش مصنوعی و رباتیک", "مهندسی فناوری اطلاعات", "مهندسی کامپیوتر - فناوری اطلاعات",
          "مهندسی کامپیوتر", "مهندسی حرفه ای کامپیوتر نرم افزار", "مهندسی معدن - استخراج مواد معدنی",
          "مهندسی مکاترونیک", "مهندسی مکانیک - تبدیل انرژی", "مهندسی مکانیک", "مهندسی شیمی - طراحی فرآیند",
          "مهندسی شیمی - محیط زیست", "مهندسی نفت"]

class StudentBase(BaseModel):
    sSTID: Annotated[str, Field(min_length=11, max_length=11)]
    sFName: Annotated[str, Field(max_length=10)]
    sLName: Annotated[str, Field(max_length=10)]
    sFather: Annotated[str, Field(max_length=10)]

    @validator('sSTID')
    def validate_stid(cls, value):
        pattern = re.compile(r"^(09[0-9]|400|401|402)114150[0-9]{2}$")
        if not pattern.match(value):
            raise ValueError('Invalid STID')
        return value

    @validator('sFName', 'sLName', 'sFather')
    def validate_name(cls, value):
        pattern = re.compile(r"^[\u0627-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u06C0\s]+$")
        if not pattern.match(value):
            raise ValueError('Invalid name')
        return value

class StudentCreate(StudentBase):
    sBirth: Annotated[str, Field()]
    sIDS: Annotated[str, Field()]
    sBornCity: str
    sAddress: Annotated[str, Field(max_length=100)]
    sPostalCode: Annotated[int, Field(gt=999999999, lt=10000000000)]
    sCPhone: Annotated[str, Field()]
    sHPhone: Annotated[str, Field()]
    sDepartment: str
    sMajor: str
    sMarried: Annotated[str, Field()]
    sID: Annotated[str, Field(min_length=10, max_length=10)]
    sSCourseIDs: List[int]
    sLIDs: List[int]

    @validator('sBirth')
    def validate_birth(cls, value):
        pattern = re.compile(r"^\d{4}/\d{2}/\d{2}$")
        if not pattern.match(value):
            raise ValueError('Invalid Birth date')
        return value

    @validator('sIDS')
    def validate_ids(cls, value):
        pattern = re.compile(r"^\d{6}\-[\u0627-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u06C0]\-\d{2}$") 
        if not pattern.match(value):
            raise ValueError('Invalid IDS')
        return value

    @validator('sCPhone')
    def validate_cphone(cls, value):
        pattern = re.compile(r"^09[0-9]{9}$")
        if not pattern.match(value):
            raise ValueError('Invalid CPhone')
        return value

    @validator('sHPhone')
    def validate_hphone(cls, value):
        pattern = re.compile(r"^0(41|44|45|26|31|84|77|21|38|56|58|61|24|23|54|71|28|25|87|34|83|74|17|13|66|11|86|76|81|35)[0-9]{8}$")
        if not pattern.match(value):
            raise ValueError('Invalid HPhone')
        return value

    @validator('sMarried')
    def validate_married(cls, value):
        if value not in ['married', 'not married','Married', 'Not married','Yes', 'yes','no', 'No']:
            raise ValueError('Invalid Married status')
        return value

    @validator('sBornCity')
    def validate_born_city(cls, v):
        if v not in cities:
            raise ValueError('شهر وارد شده معتبر نیست')
        return v

    @validator('sDepartment')
    def validate_department(cls, v):
        if v not in departments:
            raise ValueError('دانشکده وارد شده معتبر نیست')
        return v

    @validator('sMajor')
    def validate_major(cls, v):
        if v not in majors:
            raise ValueError('رشته وارد شده معتبر نیست')
        return v
    
    @validator('sID')
    def validate_ID(cls, v):
        sum = 0
        l = len(v)
        for i in range(0,l-1):
            c = ord(v[i])
            c -= 48
            sum += c * (l - i)
        r = sum % 11
        c = ord(v[l - 1])
        c -= 48
        if r > 2:
            r = 11 - r
        if r != c:
            raise ValueError('Invalid ID')
        return v

class ProfessorBase(BaseModel):
    pPID: Annotated[int, Field(gt=99999, lt=1000000)]
    pFName: Annotated[str, Field(max_length=10)]
    pLName: Annotated[str, Field(max_length=10)]
    pID: Annotated[int, Field(gt=999999999, lt=10000000000)]


    @validator('pFName', 'pLName')
    def validate_name(cls, value):
        pattern = re.compile(r"^[\u0627-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u06C0\s]+$")
        if not pattern.match(value):
            raise ValueError('Invalid name')
        return value
    
    @validator('pID')
    def validate_ID(cls, v):
        sum = 0
        l = len(str(v))
        for i in range(0,l-1):
            c = ord(str(v)[i])
            c -= 48
            sum += c * (l - i)
        r = sum % 11
        c = ord(str(v)[l - 1])
        c -= 48
        if r > 2:
            r = 11 - r
        if r != c:
            raise ValueError('کدملی استاد معتبر نیست')
        return v


class ProfessorCreate(ProfessorBase):
    pBirth: Annotated[str, Field()]
    pBornCity: str
    pAddress: Annotated[str, Field(max_length=100)]
    pPostalCode: Annotated[int, Field(gt=999999999, lt=10000000000)]
    pCPhone: Annotated[str, Field()]
    pHPhone: Annotated[str, Field()]
    pDepartment: str
    pMajor: str
    pPCourseIDs: List[int]

    @validator('pBirth')
    def validate_birth(cls, v):
        if not re.match(r'^\d{4}/\d{2}/\d{2}$', v):
            raise ValueError('تاریخ تولد معتبر نیست')
        return v

    @validator('pBornCity')
    def validate_born_city(cls, v):
        if v not in cities:
            raise ValueError('شهر وارد شده معتبر نیست')
        return v
    
    @validator('pCPhone')
    def validate_cphone(cls, value):
        pattern = re.compile(r"^09[0-9]{9}$")
        if not pattern.match(value):
            raise ValueError('Invalid CPhone')
        return value

    @validator('pHPhone')
    def validate_hphone(cls, value):
        pattern = re.compile(r"^0(41|44|45|26|31|84|77|21|38|56|58|61|24|23|54|71|28|25|87|34|83|74|17|13|66|11|86|76|81|35)[0-9]{8}$")
        if not pattern.match(value):
            raise ValueError('Invalid HPhone')
        return value

    @validator('pDepartment')
    def validate_department(cls, v):
        if v not in departments:
            raise ValueError('دانشکده وارد شده معتبر نیست')
        return v

    @validator('pMajor')
    def validate_major(cls, v):
        if v not in majors:
            raise ValueError('رشته وارد شده معتبر نیست')
        return v


class Professor(ProfessorBase):
    id: int



class CourseBase(BaseModel):
    cCID: Annotated[int, Field(gt=9999, lt=100000)]
    cCName: Annotated[str, Field(max_length=25)]
    cDepartment: str
    cCredit: Annotated[int, Field(ge=1 ,le=4)]


    @validator('cCName')
    def validate_Cname(cls, value):
        pattern = re.compile(r"^[\u0627-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u06C0\s]+$")
        if not pattern.match(value):
            raise ValueError('Invalid name')
        return value
    
    @validator('cDepartment')
    def validate_department(cls, v):
        if v not in departments:
            raise ValueError('دانشکده وارد شده معتبر نیست')
        return v
    

class Course(CourseBase):
    id: int



class StudentEdit(BaseModel):
    sSTID: Optional[str] = None
    sFName: Optional[str] = None
    sLName: Optional[str] = None
    sFather: Optional[str] = None
    sBirth: Optional[str] = None
    sIDS: Optional[str] = None
    sBornCity: Optional[str] = None
    sAddress: Optional[str] = None
    sPostalCode: Optional[int] = None
    sCPhone: Optional[str] = None
    sHPhone: Optional[str] = None
    sDepartment: Optional[str] = None
    sMajor: Optional[str] = None
    sMarried: Optional[str] = None
    sID: Optional[str] = None
    sSCourseIDs: Optional[List[int]] = None
    sLIDs: Optional[List[int]] = None


    @validator('sSTID')
    def validate_optinal_stid(cls, value):
        if value is not None:
            pattern = re.compile(r"^(09[0-9]|400|401|402)114150[0-9]{2}$")
            if not pattern.match(value):
                raise ValueError('Invalid STID')
        return value

    @validator('sFName', 'sLName', 'sFather')
    def validate_optional_name(cls, value):
        if value is not None:
            pattern = re.compile(r"^[\u0627-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u06C0\s]+$")
            if not pattern.match(value):
                raise ValueError('Invalid name')
        return value
    
    @validator('sBirth')
    def validate_optional_birth(cls, value):
        if value is not None:
            pattern = re.compile(r"^\d{4}/\d{2}/\d{2}$")
            if not pattern.match(value):
                raise ValueError('Invalid Birth date')
        return value

    @validator('sIDS')
    def validate_optional_ids(cls, value):
        if value is not None:
            pattern = re.compile(r"^\d{6}\-[\u0627-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u06C0]\-\d{2}$") 
            if not pattern.match(value):
                raise ValueError('Invalid IDS')
        return value

    @validator('sCPhone')
    def validate_optionl_cphone(cls, value):
        if value is not None:
            pattern = re.compile(r"^09[0-9]{9}$")
            if not pattern.match(value):
                raise ValueError('Invalid CPhone')
        return value

    @validator('sHPhone')
    def validate_optinal_hphone(cls, value):
        if value is not None:
            pattern = re.compile(r"^0(41|44|45|26|31|84|77|21|38|56|58|61|24|23|54|71|28|25|87|34|83|74|17|13|66|11|86|76|81|35)[0-9]{8}$")
            if not pattern.match(value):
                raise ValueError('Invalid HPhone')
        return value

    @validator('sMarried')
    def validate_optional_married(cls, value):
        if value is not None:
            if value not in ['married', 'not married','Married', 'Not married','Yes', 'yes','no', 'No']:
                raise ValueError('Invalid Married status')
        return value

    @validator('sBornCity')
    def validate_optional_borncity(cls, value):
        if value is not None:
            if value not in cities:
                raise ValueError('شهر وارد شده معتبر نیست')
        return value
    
    

    @validator('sDepartment')
    def validate_optional_department(cls, value):
        if value is not None:
            if value not in departments:
                raise ValueError('دانشکده وارد شده معتبر نیست')
        return value

    @validator('sMajor')
    def validate_optional_major(cls, value):
        if value is not None:
            if value not in majors:
                raise ValueError('رشته وارد شده معتبر نیست')
        return value
    
    @validator('sID')
    def validate_optional_ID(cls, v):
        if v is not None:
            sum = 0
            l = len(v)
            for i in range(0,l-1):
                c = ord(v[i])
                c -= 48
                sum += c * (l - i)
            r = sum % 11
            c = ord(v[l - 1])
            c -= 48
            if r > 2:
                r = 11 - r
            if r != c:
                raise ValueError('Invalid ID')
        return v
    

class ProfessorEdit(BaseModel):
    pPID: Optional[int] = None
    pFName: Optional[str] = None
    pLName: Optional[str] = None
    pBirth: Optional[str] = None
    pID: Optional[str] = None
    pBornCity: Optional[str] = None
    pAddress: Optional[str] = None
    pPostalCode: Optional[int] = None
    pCPhone: Optional[str] = None
    pHPhone: Optional[str] = None
    pDepartment: Optional[str] = None
    pMajor: Optional[str] = None
    pPCourseIDs: Optional[List[int]] = None


    @validator('pFName', 'pLName')
    def validate_optional_name(cls, value):
        if value is not None:
            pattern = re.compile(r"^[\u0627-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u06C0\s]+$")
            if not pattern.match(value):
                raise ValueError('Invalid name')
        return value
    
    @validator('pBirth')
    def validate_optional_birth(cls, value):
        if value is not None:
            pattern = re.compile(r"^\d{4}/\d{2}/\d{2}$")
            if not pattern.match(value):
                raise ValueError('Invalid Birth date')
        return value


    @validator('pCPhone')
    def validate_optionl_cphone(cls, value):
        if value is not None:
            pattern = re.compile(r"^09[0-9]{9}$")
            if not pattern.match(value):
                raise ValueError('Invalid CPhone')
        return value

    @validator('pHPhone')
    def validate_optinal_hphone(cls, value):
        if value is not None:
            pattern = re.compile(r"^0(41|44|45|26|31|84|77|21|38|56|58|61|24|23|54|71|28|25|87|34|83|74|17|13|66|11|86|76|81|35)[0-9]{8}$")
            if not pattern.match(value):
                raise ValueError('Invalid HPhone')
        return value


    @validator('pBornCity')
    def validate_optional_borncity(cls, value):
        if value is not None:
            if value not in cities:
                raise ValueError('شهر وارد شده معتبر نیست')
        return value
    
    @validator('pDepartment')
    def validate_optional_department(cls, value):
        if value is not None:
            if value not in departments:
                raise ValueError('دانشکده وارد شده معتبر نیست')
        return value

    @validator('pMajor')
    def validate_optional_major(cls, value):
        if value is not None:
            if value not in majors:
                raise ValueError('رشته وارد شده معتبر نیست')
        return value
    
    @validator('pID')
    def validate_optional_ID(cls, v):
        if v is not None:
            sum = 0
            l = len(v)
            for i in range(0,l-1):
                c = ord(v[i])
                c -= 48
                sum += c * (l - i)
            r = sum % 11
            c = ord(v[l - 1])
            c -= 48
            if r > 2:
                r = 11 - r
            if r != c:
                raise ValueError('Invalid ID')
        return v
    

class CourseEdit(BaseModel):
    cCID: Optional[int] = None
    cCName: Optional[str] = None
    cDepartment: Optional[str] = None
    cCredit: Optional[int] = None


    @validator('cCName')
    def validate_optinal_Cname(cls, value):
        if value is not None:
            pattern = re.compile(r"^[\u0627-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u06C0\s]+$")
            if not pattern.match(value):
                raise ValueError('Invalid name')
        return value
    
    @validator('cDepartment')
    def validate_department(cls, v):
        if v is not None:
            if v not in departments:
                raise ValueError('دانشکده وارد شده معتبر نیست')
        return v
    
    @validator('cCredit')
    def validate_optinal_credit(cls, value):
        if value is not None:
            if value not in [1,2,3,4]:
                raise ValueError('Invalid Credit')
        return value
    

```

## *crud*
*The name of this file stands for the four actions create, read, update, and delete, in which these four actions are performed and saved for students, professors, and courses.*

```python

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


```

## *routers*
*We use routers to separate URLs from each other and manage them better*

## *routerS*
*In this file, routers for students are written in which post, get, put, delete functions are used to create students, read student information, edit student information, and delete students.  Each of these actions has its own URL, and if needed, their response model is specified*

```python

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


```

## *routerP*
*In this file, the routers for professor are written, in which the post, get, put, delete functions are used to create professor, read professor's information, edit professor's information, and delete professor.  Each of these actions has its own URL, and if needed, their response model is specified.*

```python

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


```

## *routerC*
*In this file, lesson routers are written, in which post, get, put, delete functions are used to create lessons, read lesson information, edit lesson information, and delete lessons.  Each of these actions has its own URL, and if needed, their response model is specified.*

```python

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


```
