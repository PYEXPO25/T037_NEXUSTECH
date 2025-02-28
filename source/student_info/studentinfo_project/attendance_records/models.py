from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)

    def _str_(self):
        return f"{self.name} ({self.roll_number})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link Attendance to a Student
    date = models.DateField(auto_now_add=True)
    '''status = models.CharField(max_length=1, choices=[("P", "Present"), ("A", "Absent")], default="A")'''

    # Period-wise attendance tracking
    period1 = models.BooleanField(default=False)
    period2 = models.BooleanField(default=False)
    period3 = models.BooleanField(default=False)
    period4 = models.BooleanField(default=False)
    period5 = models.BooleanField(default=False)
    period6 = models.BooleanField(default=False)
    period7 = models.BooleanField(default=False)
    period8 = models.BooleanField(default=False)

    @property
    def total_present(self):
        return sum([
            self.period1, self.period2, self.period3, self.period4,
            self.period5, self.period6, self.period7, self.period8
        ])

    def _str_(self):
        return f"{self.student.name} - {self.date} - {self.total_present} periods attended"
