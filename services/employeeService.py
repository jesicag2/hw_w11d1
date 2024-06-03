from sqlalchemy.orm import Session
from database import db
from models.employee import Employee

    
def save(employee_data):
    with Session(db.engine) as session:
        with session.begin():
            new_employee = Employee(name=employee_data['name'], position=employee_data['position'])
            session.add(new_employee)
            session.commit()
        session.refresh(new_employee)
        return new_employee
    

def find_all():
    query = db.select(Employee)
    employees = db.session.execute(query).scalars().all()
    return employees