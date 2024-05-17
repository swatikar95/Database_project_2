from django.db import models



class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=255,blank=True,null=True)
    username = models.CharField(max_length=255,blank=True,null=True)
    password = models.CharField(max_length=255,default='1234')

    class Meta:
        managed = False
        db_table = 'admin'



class Department(models.Model):
    dept_name = models.CharField(primary_key=True,max_length=20)
    building = models.CharField(max_length=255, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)

    # def __str__(self):
    #     return self.dept_name

    class Meta:
        managed = False
        db_table = 'department'

class Instructor(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    dept_name = models.CharField(max_length=10, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=32, null=False)

    class Meta:
        managed = False
        db_table = 'instructor'
'''
class Instructor(models.Model):
    id = models.CharField(primary_key=True, max_length=25)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'instructor'
'''
'''
    Student table acts as place holder for student_enrolled_course
'''


class Student(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.CharField(max_length=32, blank=True, null=True)
    total_credits = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=32,null=False)

    class Meta:
        managed = False
        db_table = 'student'

class Course(models.Model):
    course_id = models.CharField(max_length=8, primary_key=True)
    title = models.CharField(max_length=64, blank=True, null=True)
    dept_name = models.CharField(max_length=32, blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'


class Section(models.Model):
    #course = models.ForeignKey(course, on_delete=models.CASCADE, primary_key=True, db_column='course_id')
    
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    building = models.CharField(max_length=32, blank=True, null=True)
    room = models.CharField(max_length=8, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section'
        unique_together = (('course_id', 'sec_id', 'semester', 'year'),)


class Takes(models.Model):
    student_id = models.CharField(max_length=8,primary_key=True)
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        unique_together = (('student_id', 'course_id', 'sec_id', 'semester', 'year'),)


class Teaches(models.Model):
    course_id = models.CharField(max_length=8,primary_key=True)
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    teacher_id = models.CharField(max_length=5)

    class Meta:
        managed = False
        unique_together = (('course_id', 'sec_id', 'semester', 'year', 'teacher_id'),)
