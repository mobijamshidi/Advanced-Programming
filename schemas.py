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
    