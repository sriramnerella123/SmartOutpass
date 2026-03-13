

from pydantic import BaseModel #type:ignore

class Product(BaseModel):
    id:int
    name:str


    model_config = {
        "from_attributes": True
    }

class Exit_details(BaseModel):
    Sno:int
    Id:int
    Student_name:str
    Year:int
    Branch:str
    Parent_name:str
    Student_Phone_number:int
    Parent_phone_number:int
    # Out_time:str


    model_config={
        "from_attributes":True
    }


class Group_outpass_Approved_list(BaseModel):
    Sno:int
    Id:int
    Student_name:str
    Year:int
    Branch:str
    Address:str
    Teamid:str
    Student_Phone_number:int
    Parent_phone_number:int
    Parent_id_photo:str
    Parent_photo:str


    model_config={
        "from_attributes":True
    }

class StudentCreate(BaseModel):
    studentname:str
    email:str
    password:str

class StudentLogin(BaseModel):
    studentname:str
    password:str

# class WardenCreate(BaseModel):
#     wardenname:str
#     wardenId:str
#     password:str
    

class WardenLogin(BaseModel):
    wardenname:str
    wardenId:str
    password:str

class SecurityLogin(BaseModel):
    securityname:str
    securityId:str
    password:str