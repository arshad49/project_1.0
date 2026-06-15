from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from database import get_db, engine, Base
from models import Customer

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Follow-up API")

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schemas
class CustomerCreate(BaseModel):
    name: str
    phone: str
    last_visit: Optional[date] = None
    next_followup: Optional[date] = None
    template_name: str

class CustomerUpdate(BaseModel):
    status: Optional[str] = None
    retry_count: Optional[int] = None

# Response schema
class CustomerResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    last_visit: Optional[date]
    next_followup: Optional[date]
    template_name: str
    status: str
    retry_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 1. Add customer
@app.post("/customer", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    print("🔥 Incoming request:", customer.dict())   # ADD THIS

    # existing = db.query(Customer).filter(Customer.phone == customer.phone).first()
    # if existing:
    #     raise HTTPException(status_code=400, detail="Phone number already exists")

    db_customer = Customer(
        **customer.model_dump(),
        status="pending",
        retry_count=0
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    print("✅ Saved to DB:", db_customer.phone)   # ADD THIS

    return db_customer

# 2. Get all customers
@app.get("/customers", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).order_by(Customer.next_followup).all()

# 3. Get today's follow-ups

@app.get("/today-followups", response_model=list[CustomerResponse])
def get_today_followups(db: Session = Depends(get_db)):
    today = date.today()
    return db.query(Customer).filter(
        Customer.next_followup == today,
        Customer.status == "pending"
    ).order_by(Customer.next_followup).all()
    
# 4. Update customer
@app.patch("/customer/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, update: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if update.status:
        customer.status = update.status
    if update.retry_count is not None:
        customer.retry_count = update.retry_count
    
    db.commit()
    db.refresh(customer)
    return customer

@app.get("/")
def root():
    return {"message": "API is running"}
