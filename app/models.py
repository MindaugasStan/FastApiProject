from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lastname = Column(String)
    email = Column(String)
    jobstartdate = Column(DateTime)
    jobenddate = Column(DateTime)
    hourlyrate = Column(Float)
    experience = Column(Float)
    company_id = Column(Integer(), ForeignKey('companies.id'))
    employeecompany = relationship('Company', back_populates='employees')
    senioritylevel_id = Column(Integer(), ForeignKey('senioritylevels.id'))
    seniorityLevel = relationship('SeniorityLevel')

class SeniorityLevel(Base):
    __tablename__ = "senioritylevels"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    multiplier = Column(Float)
    time_needed = Column(Float)
    company_id = Column(Integer(), ForeignKey('companies.id'))
    company = relationship('Company', back_populates='levels')


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    levels = relationship('SeniorityLevel', back_populates='company')
    employees = relationship('Employee', back_populates='employeecompany')
