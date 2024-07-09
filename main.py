from fastapi import FastAPI,Depends,Request
from database import engine, Base
from routerS import router as student_router
from routerP import router as professor_router
from routerC import router as course_router
from fastapi.templating import Jinja2Templates
from database import engine,SessionLocal
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(student_router, tags=['students'])
app.include_router(professor_router, tags=['professors'])
app.include_router(course_router, tags=['courses'])













app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from routerS import router as student_router
from routerP import router as professor_router
from routerC import router as course_router
import models
from models import Professor, Student, Course

# Create all the tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(student_router, tags=['students'])
app.include_router(professor_router, tags=['professors'])
app.include_router(course_router, tags=['courses'])

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.id.desc()).all()
    return templates.TemplateResponse("home.html", {"request": request, "students": students})

@app.get("/home")
async def home_redirect(request: Request, db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.id.desc()).all()
    return templates.TemplateResponse("home.html", {"request": request, "students": students})

# Students routes
@app.get("/showstu")
async def students_info(request: Request, db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.id.desc()).all()
    return templates.TemplateResponse("showstu.html", {"request": request, "students": students})

@app.post("/addstu")
async def add_student(request: Request, 
                      sSTID: str = Form(...), sFName: str = Form(...), sLName: str = Form(...), sFather: str = Form(...), 
                      sBirth: str = Form(...), sIDS: str = Form(...), sBornCity: str = Form(...), sAddress: str = Form(...), 
                      sPostalCode: int = Form(...), sCPhone: int = Form(...), sHPhone: int = Form(...), sDepartment: str = Form(...), 
                      sMajor: str = Form(...), smarried: str = Form(...), sID: int = Form(...), sSCourseIDs: str = Form(...), 
                      sLIDs: str = Form(...), db: Session = Depends(get_db)):
    new_student = Student(
        sSTID=sSTID, sFName=sFName, sLName=sLName, sFather=sFather, sBirth=sBirth, sIDS=sIDS, sBornCity=sBornCity, 
        sAddress=sAddress, sPostalCode=sPostalCode, sCPhone=sCPhone, sHPhone=sHPhone, sDepartment=sDepartment, 
        sMajor=sMajor, smarried=smarried, sID=sID, sSCourseIDs=sSCourseIDs, sLIDs=sLIDs
    )
    db.add(new_student)
    db.commit()
    return RedirectResponse(url=app.url_path_for("students_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addstu")
async def add_student_form(request: Request , db: Session = Depends(get_db)):
    professors = db.query(Professor).all()
    courses = db.query(Course).all()
    return templates.TemplateResponse("addstu.html", {"request": request, "professors": professors,  "courses": courses})

@app.get("/editstu/{user_id}")
async def edit_student(request: Request, user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == user_id).first()
    return templates.TemplateResponse("editstu.html", {"request": request, "user": student})

@app.post("/update_student/{user_id}")
async def update_student(request: Request, user_id: int, sSTID: str = Form(...), sFName: str = Form(...), sLName: str = Form(...), sFather: str = Form(...), sBirth: str = Form(...), sIDS: str = Form(...), sBornCity: str = Form(...), sAddress: str = Form(...), sPostalCode: int = Form(...), sCPhone: int = Form(...), sHPhone: int = Form(...), sDepartment: str = Form(...), sMajor: str = Form(...), smarried: str = Form(...), sID: int = Form(...), sSCourseIDs: str = Form(...), sLIDs: str = Form(...), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == user_id).first()
    student.sSTID = sSTID
    student.sFName = sFName
    student.sLName = sLName
    student.sFather = sFather
    student.sBirth = sBirth
    student.sIDS = sIDS
    student.sBornCity = sBornCity
    student.sAddress = sAddress
    student.sPostalCode = sPostalCode
    student.sCPhone = sCPhone
    student.sHPhone = sHPhone
    student.sDepartment = sDepartment
    student.sMajor = sMajor
    student.smarried = smarried
    student.sID = sID
    student.sSCourseIDs = sSCourseIDs
    student.sLIDs = sLIDs
    db.commit()
    return RedirectResponse(url=app.url_path_for("students_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete_student/{user_id}")
async def delete_student(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.id == user_id).first()
    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("students_info"), status_code=status.HTTP_303_SEE_OTHER)

# Courses routes
@app.get("/showcourse")
async def courses_info(request: Request, db: Session = Depends(get_db)):
    courses = db.query(Course).order_by(Course.id.desc()).all()
    return templates.TemplateResponse("showcourse.html", {"request": request, "courses": courses})

@app.post("/add_course")
async def add_course(request: Request, cCID: int = Form(...), cCName: str = Form(...), cDepartment: str = Form(...), cCredit: int = Form(...), db: Session = Depends(get_db)):
    course = Course(cCID=cCID, cCName=cCName, cDepartment=cDepartment, cCredit=cCredit)
    db.add(course)
    db.commit()
    return RedirectResponse(url=app.url_path_for("courses_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addcourse")
async def add_course_form(request: Request):
    return templates.TemplateResponse("addcourse.html", {"request": request})

@app.get("/edit_course/{user_id}")
async def edit_course(request: Request, user_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == user_id).first()
    return templates.TemplateResponse("editcourse.html", {"request": request, "user": course})

@app.post("/update_course/{user_id}")
async def update_course(request: Request, user_id: int, cCID: int = Form(...), cCName: str = Form(...), cDepartment: str = Form(...), cCredit: str = Form(...), db: Session = Depends(get_db)):
    other_user = db.query(Course).filter(Course.id == user_id).first()
    other_user.cCID = cCID
    other_user.cCName = cCName
    other_user.cDepartment = cDepartment
    other_user.cCredit = cCredit
    db.commit()
    return RedirectResponse(url=app.url_path_for("courses_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete_course/{user_id}")
async def delete_course(request: Request, user_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == user_id).first()
    db.delete(course)
    db.commit()
    return RedirectResponse(url=app.url_path_for("courses_info"), status_code=status.HTTP_303_SEE_OTHER)

# Professors routes
@app.get("/showprofessor")
async def professors_info(request: Request, db: Session = Depends(get_db)):
    professors = db.query(Professor).order_by(Professor.id.desc()).all()
    return templates.TemplateResponse("showprofessor.html", {"request": request, "professors": professors})

@app.post("/add_professor") 
async def add_professor(request: Request, 
                        pPID: int = Form(...), pFName: str = Form(...), pLName: str = Form(...), 
                        pBirth: str = Form(...), pBornCity: str = Form(...), pAddress: str = Form(...), 
                        pPostalCode: int = Form(...), pCPhone: int = Form(...), pHPhone: int = Form(...), 
                        pDepartment: str = Form(...), pMajor: str = Form(...), pID: int = Form(...), 
                        pPCourseIDs: str = Form(...), db: Session = Depends(get_db)):
    new_professor = Professor(
        pPID=pPID, pFName=pFName, pLName=pLName, pBirth=pBirth, pBornCity=pBornCity, pAddress=pAddress, 
        pPostalCode=pPostalCode, pCPhone=pCPhone, pHPhone=pHPhone, pDepartment=pDepartment, pMajor=pMajor, 
        pID=pID, pPCourseIDs=pPCourseIDs
    )
    db.add(new_professor)
    db.commit()
    return RedirectResponse(url=app.url_path_for("professors_info"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/addprofessor")
async def add_professor_form(request: Request):
    return templates.TemplateResponse("addprofessor.html", {"request": request})


@app.get("/edit_professor/{user_id}")
async def edit_professor(request: Request, user_id: int, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.id == user_id).first()
    return templates.TemplateResponse("editprofessor.html", {"request": request, "user": professor})

@app.post("/update_professor/{user_id}")
async def update_professor(request: Request, user_id: int, 
                           pPID: int = Form(...), pFName: str = Form(...), pLName: str = Form(...), 
                           pBirth: str = Form(...), pBornCity: str = Form(...), pAddress: str = Form(...), 
                           pPostalCode: int = Form(...), pCPhone: int = Form(...), pHPhone: int = Form(...), 
                           pDepartment: str = Form(...), pMajor: str = Form(...), pID: int = Form(...), 
                           pPCourseIDs: str = Form(...), db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.id == user_id).first()
    professor.pPID = pPID
    professor.pFName = pFName
    professor.pLName = pLName
    professor.pBirth = pBirth
    professor.pBornCity = pBornCity
    professor.pAddress = pAddress
    professor.pPostalCode = pPostalCode
    professor.pCPhone = pCPhone
    professor.pHPhone = pHPhone
    professor.pDepartment = pDepartment
    professor.pMajor = pMajor
    professor.pID = pID
    professor.pPCourseIDs = pPCourseIDs
    db.commit()
    return RedirectResponse(url=app.url_path_for("professors_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete_professor/{user_id}")
async def delete_professor(request: Request, user_id: int, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.id == user_id).first()
    db.delete(professor)
    db.commit()
    return RedirectResponse(url=app.url_path_for("professors_info"), status_code=status.HTTP_303_SEE_OTHER)






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)











