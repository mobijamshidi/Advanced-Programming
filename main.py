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
