
from sqlalchemy import Column,Integer,String,Float,Boolean # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
Base = declarative_base()
class Product(Base):
    __tablename__ = "product"
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String(255))


class Exit_details(Base):
    __tablename__="Exit_details"
    Sno=Column(Integer,unique=True,index=True)
    Id=Column(Integer,primary_key=True,index=True)
    Student_name=Column(String(255))
    Year=Column(Integer)
    Branch=Column(String(75))
    Parent_name=Column(String(255))
    Student_Phone_number=Column(Integer)
    Parent_phone_number=Column(Integer)
    # Out_time=Column(String(50))


class Group_outpass_Approved_list(Base):
    __tablename__="Group_outpass_Approved_list"
    Sno=Column(Integer,unique=True,index=True)
    Id=Column(Integer,primary_key=True,index=True)
    Student_name=Column(String(255))
    Year=Column(Integer)
    Branch=Column(String(75))
    Address=Column(String(255))
    Teamid=Column(String(50))
    Student_Phone_number=Column(Integer)
    Parent_phone_number=Column(Integer)
    Parent_id_photo=Column(String(255))
    Parent_photo=Column(String(255))


class Student(Base):
    __tablename__="students"
    id =Column(Integer,primary_key=True,index = True)
    username = Column(String(50),unique =True)
    email = Column(String(100))
    password = Column(String(255))
   

class Warden(Base):
    __tablename__="wardens"
    id =Column(Integer,primary_key=True,index = True)
    wardenname = Column(String(50),unique =True)
    wardenId = Column(String(100),unique = True)
    password = Column(String(255))

    
   
class Security(Base):
    __tablename__="security"
    id =Column(Integer,primary_key=True,index = True)
    securityname = Column(String(50),unique =True)
    securityId = Column(String(100),unique = True)
    password = Column(String(255))

    



    
