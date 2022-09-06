from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.database import engine, SessionLocal
from datetime import datetime
from typing import List
from app.services.services import generateEmployeeEmail, generateEmployeeExperience

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/company', status_code=status.HTTP_201_CREATED, tags=['Company'])
def create(request: schemas.Company, db: Session = Depends(get_db)):
    new_company = models.Company(name=request.Name)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


@app.get('/company', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowCompany], tags=['Company'])
def all(db: Session = Depends(get_db)):
    companies = db.query(models.Company).all()
    return companies


@app.get('/company/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowCompany, tags=['Company'])
def show(id, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Company with the id {id} is not available")
    return company


@app.delete('/company/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Company'])
def delete(id, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == id)
    if not company.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Company with id {id} not found")
    company.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


@app.put('/company/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Company'])
def update(id: int, request: schemas.Company, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == id)

    if not company.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Company with id {id} not found")

    company.update({"name": request.Name})
    db.commit()
    return 'updated'


@app.post('/seniorityLevel', status_code=status.HTTP_201_CREATED, tags=['SeniorityLevels'])
def create(request: schemas.SeniorityLevel, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == request.company_id).first()
    new_level = models.SeniorityLevel(level=request.level, multiplier=request.multiplier, company_id=request.company_id,
                                      time_needed=request.time_needed, company=company)
    db.add(new_level)
    db.commit()
    db.refresh(new_level)

    return new_level


@app.put('/seniorityLevel/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['SeniorityLevels'])
def update(id: int, request: schemas.UpdateSeniorityLevel, db: Session = Depends(get_db)):
    seniority_level = db.query(models.SeniorityLevel).filter(models.SeniorityLevel.id == id)

    if not seniority_level.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seniority Level with id {id} not found")

    seniority_level.update({"level": request.level, "multiplier": request.multiplier, "time_needed": request.time_needed})
    db.commit()
    return 'updated'


@app.post('/employee', status_code=status.HTTP_201_CREATED, tags=['Employees'])
def create(request: schemas.Employee, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == request.Company_id).first()
    email = generateEmployeeEmail(request.Name, request.LastName, company.name)
    seniority_levels = company.levels
    exp = {}
    time = generateEmployeeExperience(request.JobStartDate, request.Experience)
    for level in seniority_levels:
        if (time >= level.time_needed):
            exp = level
            continue
    employee = models.Employee(name=request.Name, lastname=request.LastName, jobstartdate=request.JobStartDate,
                                jobenddate=request.JobEndDate, hourlyrate=request.HourlyRate,
                                experience=request.Experience, email=email, company_id=request.Company_id,
                                employeecompany=company, senioritylevel_id=exp.id, seniorityLevel=exp)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@app.get('/employee', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowEmployee], tags=['Employees'])
def all(status: bool, date: str, db: Session = Depends(get_db)):
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')

    if status:
        employees = db.query(models.Employee).filter(models.Employee.jobstartdate < date_time_obj).filter(models.Employee.jobenddate == None).all()
    else:
        employees = db.query(models.Employee).filter(models.Employee.jobstartdate < date_time_obj).filter(models.Employee.jobenddate != None).all()
    return employees


@app.get('/employeeName', status_code=status.HTTP_200_OK, tags=['Employees'])
def getwithfullname(db: Session = Depends(get_db)):
    response = []
    employees = db.query(models.Employee).filter(models.Employee.jobenddate == None).all()

    for employee in employees:
        response.append({"fullname": employee.name + ' ' + employee.lastname, "email": employee.email, "annualSalary": (employee.seniorityLevel.multiplier * employee.hourlyrate) * 160 * 12})

    return response


@app.delete('/employee/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Employees'])
def delete(id, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == id)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with id {id} not found")

    employee.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


@app.put('/employee/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Employees'])
def update(id, request: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == id)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with id {id} not found")
    employee.update({"name": request.name, "lastname": request.lastname, "jobstartdate": request.jobstartdate, "jobenddate": request.jobenddate, "experience": request.experience, "hourlyrate": request.hourlyrate})
    db.commit()
    return 'updated'
