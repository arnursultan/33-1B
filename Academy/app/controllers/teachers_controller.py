from core.repository import TeachersRepo

class TeachersController:
    def get_all(self):
        return TeachersRepo.all()

    def add(self, fn, subj, email, phone, exp, status):
        if not fn.strip():
            return "Full name is required"
        if not subj.strip():
            return "Subject is required"

        if not exp.isdigit():
            return "Experience must be a number"

        TeachersRepo.add(fn, subj, email, phone, int(exp), status)
        return "ok"

    def update(self, tid, fn, subj, email, phone, exp, status):
        if not tid:
            return "No teacher selected"

        TeachersRepo.update(tid, fn, subj, email, phone, int(exp), status)
        return "ok"

    def delete(self, tid):
        if not tid:
            return "No teacher selected"
        TeachersRepo.delete(tid)
        return "ok"
