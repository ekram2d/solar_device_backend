from django.db import models
DEPT_CHOICES = [
    ('CSE', 'Computer Science'),
    ('EEE', 'Electrical Engineering'),
    ('ME', 'Mechanical Engineering'),
]
class Teacher(models.Model):
    name = models.CharField(max_length=100, default='Unknown Name')
    subject = models.CharField(max_length=100, default='General')
    dept = models.CharField(max_length=100, choices=DEPT_CHOICES, default='CSE')

    def __str__(self):
        return self.name   
