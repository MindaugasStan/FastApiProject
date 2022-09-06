from pydantic import BaseModel
from typing import Optional, List
import datetime


class Company(BaseModel):
    Name: str


class SeniorityLevel(BaseModel):
    level: str
    multiplier: float
    time_needed: float
    company_id: int

    class Config:
        orm_mode = True


class ShowSeniorityLevel(BaseModel):
    level: str
    multiplier: float
    time_needed: float

    class Config:
        orm_mode = True


class Employee(BaseModel):
    Name: str
    LastName: str
    JobStartDate: datetime.date
    JobEndDate: Optional[datetime.date]
    Experience: float
    HourlyRate: float
    Company_id: int

    class Config:
        orm_mode = True


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    jobstartdate: Optional[datetime.date] = None
    jobenddate: Optional[datetime.date] = None
    experience: Optional[float]
    hourlyrate: Optional[float]


class ShowEmployee(BaseModel):
    name: str
    lastname: str
    jobstartdate: datetime.date
    jobenddate: Optional[datetime.date]
    experience: float
    hourlyrate: float
    experience: float
    seniorityLevel: ShowSeniorityLevel

    class Config:
        orm_mode = True


class ShowEmployeeWithFullName(BaseModel):
    fullname: str
    email: str
    annualSalary: float


class UpdateSeniorityLevel(BaseModel):
    level: str
    multiplier: float
    time_needed: float


class ShowCompany(BaseModel):
    id: int
    name: str
    levels: List[ShowSeniorityLevel]
    employees: List[ShowEmployee]

    class Config:
        orm_mode = True
