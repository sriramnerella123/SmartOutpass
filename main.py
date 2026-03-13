from fastapi import FastAPI, Depends,status,HTTPException,Form,File,UploadFile # type: ignore
from database.db import SessionLocal, engine
from sqlalchemy.orm import Session # type: ignore
from database import models, schemas
from auth.auth_utils import verify_password,hash_password,create_token
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Session=Depends(get_db)
@app.get("/products")
def get_products(db: Session=Depends(get_db)): # type: ignore
    try:
        products = db.query(models.Product).all()
        return products

    except Exception as e:
        print(e)   # prints error in terminal
        raise HTTPException(
            status_code=500,
            detail="Database error occurred"
        )
@app.post("/products",status_code = status.HTTP_201_CREATED)
async def enter(product: schemas.Product, db: Session=Depends(get_db)): # type: ignore
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.post("/Exit_details",status_code = status.HTTP_201_CREATED)
async def enter(exit: schemas.Exit_details, db: Session=Depends(get_db)): # type: ignore
    new = models.Exit_details(**exit.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.post("/Group_outpass_Approved_list",status_code = status.HTTP_201_CREATED)
async def enter(exit: schemas.Group_outpass_Approved_list, db: Session=Depends(get_db)): # type: ignore
    new = models.Group_outpass_Approved_list(**exit.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

#Student signup route
@app.post("/studentRegister")
async def register(student:schemas.StudentCreate,db:Session=Depends(get_db)):
    exist = db.query(models.Student).filter(models.Student.studentname == student.username).first()
    if exist:
        raise HTTPException(400,"Username already exist")
    new_student = models.Student(studentname = student.username,
                           email = student.email,
                           password = hash_password(student.password))
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


#Student Login route
@app.post("/studentLogin")
async def login(student:schemas.StudentLogin,db:Session=Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.studentname.lower()==student.studentname.lower()).first()
    
    if not db_student:
        raise HTTPException(400,"Invalid username")
    if not verify_password(student.password,db_student.password):
        raise HTTPException(400,"Invalid password")
    token = create_token({"sub":db_student.studentname})
    return {
        "access_token":token,
        "token_type":"bearer"
    }


'''
#warder signup route
@app.post("/wardenRegister")
async def register(warden:schemas.WardenCreate,db:Session=Depends(get_db)):
    exist = db.query(models.Warden).filter(models.Warden.wardenname == warden.wardenname).first()
    id = db.query(models.WardenId).filter(models.WardenId.wardenId != warden.wardenId).first()
    if exist:
        raise HTTPException(400,"Username already exist")
    elif id:
        raise HTTPException(400,"WardenId doesnot match")
    
    new_warden = models.Warden(wardenname = warden.wardenname,
                           wardenId = warden.wardenId,
                           password = hash_password(warden.password))
    db.add(new_warden)
    db.commit()
    db.refresh(new_warden)
    return new_warden
'''

#Warden Login route
@app.post("/wardenLogin")
async def login(warden:schemas.WardenLogin,db:Session=Depends(get_db)):
    db_user = db.query(models.Warden).filter(models.Warden.wardenname.lower()==warden.wardenname.lower() and models.Warden.wardenId == warden.wardenId).first()
    
    if not db_user:
        raise HTTPException(400,"Invalid username")
    if not verify_password(warden.password,db_user.password):
        raise HTTPException(400,"Invalid password")
    token = create_token({"sub":db_user.wardenname})
    return {
        "access_token":token,
        "token_type":"bearer"
    }

'''
#Security signup route
@app.post("/securityRegister")
async def register(user:schemas.UserCreate,db:Session=Depends(get_db)):
    exist = db.query(models.User).filter(models.User.username == user.username).first()
    if exist:
        raise HTTPException(400,"Username already exist")
    new_user = models.User(username = user.username,
                           email = user.email,
                           password = hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
'''

#Security Login route
@app.post("/securityLogin")
async def login(security:schemas.SecurityLogin,db:Session=Depends(get_db)):
    db_user = db.query(models.Security).filter(models.Security.securityname.lower()==security.securityname.lower() and models.Security.securityId == security.securityId).first()
    
    if not db_user:
        raise HTTPException(400,"Invalid username")
    if not verify_password(security.password,db_user.password):
        raise HTTPException(400,"Invalid password")
    token = create_token({"sub":db_user.securityname})
    return {
        "access_token":token,
        "token_type":"bearer"
    }





    