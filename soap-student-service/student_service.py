from spyne import ServerBase, Unicode, Integer, rpc
from models import SessionLocal, StudentMetadata

class StudentService(ServerBase):
    
    @rpc(Unicode, Unicode, Integer, Unicode, _returns=Unicode)
    def add_student(ctx, name, email, age, department):
        session = SessionLocal()
        new_student = StudentMetadata(name=name, email=email, age=age, department=department)
        session.add(new_student)
        session.commit()
        return f"Student {name} added sucessfully with ID {new_student.id}"
    
    @rpc(Integer, _returns=Unicode)
    def get_student(ctx, student_id):
        session = SessionLocal()
        student = session.get(StudentMetadata, student_id)
        return f"{student.name}, {student.age}. {student.email}, {student.department}" if student else "Student not found"
    
    @rpc(Integer, Unicode, Unicode, Integer, Unicode, _returns=Unicode)
    def update_student(ctx, student_id, name, email, age, department):
        session = SessionLocal()
        student = session.get(StudentMetadata, student_id)
        if not student:
            return "Student not found."
        student.name = name
        student.email = email
        student.age = age
        student.department = department
        session.commit()
        return "Updated Successfully."
    
    @rpc(Integer, _returns=Unicode)
    def delete_student(ctx, student_id):
        session = SessionLocal()
        student = session.get(StudentMetadata, student_id)
        if not student:
            return "Student not found."
        session.delete(student)
        session.commit()
        return "Deleted Successfully."