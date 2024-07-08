from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
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
