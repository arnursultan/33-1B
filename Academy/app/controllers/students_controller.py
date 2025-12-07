from core.repository import StudentsRepo

class StudentsController:
    def get_all(self):
        return StudentsRepo.all()

    def add(self, name, age, email):
        if not name.strip():
            return "Name is required"
        if not age.isdigit():
            return "Age must be a number"

        StudentsRepo.add(name, age, email)
        return "ok"

    def update(self, student_id, name, age, email):
        if not student_id:
            return "Select a student"
        StudentsRepo.update(student_id, name, age, email)
        return "ok"

    def delete(self, student_id):
        if not student_id:
            return "Select student first"
        StudentsRepo.delete(student_id)
        return "ok"
