from itertools import count
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import Admin, Instructor, Department, Takes, Teaches, Course, Student
from django.template import loader
from polls.models import *
from django.db import connection
from django.db.models import Avg, Max, Min
from django.urls import reverse
from .forms import courseForm




def index(request):
    return render(request,'login.html')


def login(request):
    if request.method == "POST":
        login_as = request.POST.get("login_as", "")
        admin_name = request.POST.get("admin_name","")  
        admin_password = request.POST.get("password","")

        if login_as == 'admin':
            try:
                admin = Admin.objects.get(username=admin_name)
                if admin.password == admin_password:
                    request.session["login_as"] = login_as
                    request.session["admin_name"] = admin_name
                    print("matches: ",admin.username,admin.password)
                    return redirect('/admin')
                else:
                    print("does not match")
                    return render(request, 'login.html', {"error": "Invalid username or password"})
            except Admin.DoesNotExist:
                print("not dmin")
                return render(request, 'login.html', {"error": "Invalid username or password"})
        elif login_as == 'instructor':
            try:
                instructor = Instructor.objects.get(name=admin_name)
                print("password typed is ",admin_password)
                print("login_as : "+login_as)
                print("user name is "+admin_name)
                if instructor.password == admin_password and login_as=="instructor":
                    request.session["login_as"] = login_as
                    request.session["username"] = admin_name
                    request.session["teacher_id"] = instructor.id  # Set the teacher_id in the session
                
                    print("matches: ",instructor.name,instructor.password)
                    user_id= Instructor.objects.raw('select id from Credentials where user_type=$s and username=$s',[login_as,admin_name])
                    return redirect('/instructor')
                else:
                    print("does not match")
                    return render(request, 'login.html', {"error": "Invalid username or password"})
            except Instructor.DoesNotExist:
                print("not instructor")
                return render(request, 'login.html', {"error": "Invalid username or password"})
        elif login_as == 'student':
            try:
                student_obj = Student.objects.get(name=admin_name)
                if student_obj.password == admin_password:
                    request.session["login_as"] = login_as
                    request.session["username"] = admin_name
                    print("matches: ",  student_obj.name,student_obj.password)
                    return redirect('/student')
                else:
                    print("does not match")
                    return render(request, 'login.html', {"error": "Invalid username or password"})
            except Student.DoesNotExist:
                print("not student")
                return render(request, 'login.html', {"error": "Not a student"})
    return render(request, 'login.html')

def logout(request):
    request.session.delete("login_as")
    request.session.delete("admin_name")
    
    return redirect('/login')

def admin(request):
    print("Accessing admin dashboard")
    if not request.session.get("admin_name") or request.session.get("login_as") != 'admin':
        return redirect('/login')
    
    return render(request, 'admin/admin.html')

def instructor(request):
    print("Accessing Instructor dashboard")
    if not request.session.get("username") or request.session.get("login_as") != 'instructor':
        return redirect('/login')
    
    return render(request, 'instructor/instructor.html')

def student(request):
    print("Accessing Student dashboard")
    if not request.session.get("username") or request.session.get("login_as") != 'student':
        return redirect('/login')
    
    return render(request, 'student/student.html')


def course_section(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        semester = request.POST.get('semester')
        sec_id = request.POST.get('sec_id')

        query = """
                 SELECT T.course_id, C.title, T.student_id, S.name 
                 FROM takes T 
                 JOIN Student S ON T.student_id = S.student_id 
                 JOIN Course C ON T.course_id = C.course_id 
                 JOIN teaches Tch ON T.course_id = Tch.course_id AND T.sec_id = Tch.sec_id AND T.semester = Tch.semester 
                 WHERE T.semester = %s AND T.sec_id = %s AND Tch.teacher_id = %s
                """
        params = [semester, sec_id, teacher_id]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({
                'course_id': row[0],
                'title': row[1],
                'student_id': row[2],
                'name': row[3]
            })

        print(results)  # For debugging

        if not results:
            results = [{
                'course_id': 0,
                'title': 0,
                'student_id': 0,
                'name': 0
            }]

        return render(request, "instructor/f4.html", {'results': results})

    return render(request, "instructor/f4.html")




#student_enrolled_curses is called in urls.py
def student_enrolled_courses(request):
    
    if request.method == 'GET':
        teacher_id = request.session.get('teacher_id')
        semester = request.GET.get('semester')
        course_id=request.GET.get('course_id')
        #year = request.GET.get('year')

        '''
                        <th>student_id</th>
                        <th>name</th>
                        <th>course_id</th>
                        <th>semester</th>
                        <th>teacher_id</th>
        '''
        results = Takes.objects.raw("SELECT T.student_id, S2.name, S.course_id, S.semester, Tch.teacher_id FROM takes T JOIN section S ON T.course_id = S.course_id  AND T.semester = S.semester JOIN student S2 ON T.student_id = S2.student_id  JOIN teaches Tch ON S.course_id = Tch.course_id AND  S.semester = Tch.semester WHERE Tch.teacher_id = %s AND S.semester = %s AND S.course_id = %s", [teacher_id, semester, course_id])

        return render(request, "instructor/f5.html", {'results': results})

    return render(request, "instructor/f5.html")
   
def admin_roaster(request):
    sort_by = request.GET.get('sort','id') #default sort

    if sort_by == 'name':
        professors = Instructor.objects.all().order_by('name')
    elif sort_by == 'salary':
        professors = Instructor.objects.all().order_by('salary')
    elif sort_by == 'dept_name':
        professors = Instructor.objects.all().order_by('dept_name')
    elif sort_by == 'id':
        professors = Instructor.objects.all().order_by('id')  # Assuming 'id' is the field name
    else:
        # Fallback to a default sort if sort_by contains an unexpected value
        professors = Instructor.objects.all().order_by('id')

    #pass info fron the view to template
    context = {
        'professors' : professors,
        'sort_by' : sort_by
    }

    return render(request,"admin/admin_roaster.html",context)



def add_instructor(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        dept_name = request.POST.get('dept_name')
        salary = request.POST.get('salary')
        
        # You might want to add some validation and error handling here
        
        #department, created = Department.objects.get_or_create(dept_name=dept_name)
        Instructor.objects.create(id=id,name=name, dept_name=dept_name, salary=salary)
        
        return redirect('admin_roaster')
    else:
        # If not POST, redirect to the roster page or show an error
        return redirect('admin_roaster')
    
def admin_salary(request):
    # Aggregate the salaries by department
    salary_data = Instructor.objects.values('dept_name').annotate(
        min_salary=Min('salary'),
        max_salary=Max('salary'),
        avg_salary=Avg('salary')
    ).order_by('dept_name')

    context = {
        'salary_data': salary_data,
    }
    
    return render(request, 'admin/admin_salary.html', context)


def display_course_sections(request):
    # Retrieve all rows from the Course and Section tables using SQL
    query = """
        SELECT c.*, s.*
        FROM course c
        INNER JOIN section s ON c.course_id = s.course_id
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Convert the raw SQL query results into a list of dictionaries
    course_sections = []
    for row in rows:
        course_section = {
            'course_id': row[0],
            'title': row[1],
            'dept_name': row[2],
            'credits': row[3],
            'sec_id': row[4],
            'semester': row[5],
            'year': row[6],
            'building': row[7],
            'room': row[8],
            'capacity': row[9]
        }
        course_sections.append(course_section)

    # Pass the retrieved data to the template for rendering
    return render(request, 'student/display_courseSectionsList.html', {'course_sections': course_sections})


def query_course_sections(request):
    if request.method == 'POST':
        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')
        year = request.POST.get('year')

        # Define sql 
        query = """
            SELECT c.course_id, c.title, c.dept_name, c.credits, s.sec_id, s.semester, s.year, s.building, s.room, s.capacity
            FROM course c
            INNER JOIN section s ON c.course_id = s.course_id
            WHERE c.dept_name = %s AND s.semester = %s AND s.year = %s
        """
        params = [dept_name, semester, year]

        # Executing sql
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        # Transforming sql results into a list of dictionaries
        course_sections = []
        for row in rows:
            course_sections.append({
                'course_id': row[0],
                'title': row[1],
                'dept_name': row[2],
                'credits': row[3],
                'sec_id': row[4],
                'semester': row[5],
                'year': row[6],
                'building': row[7],
                'room': row[8],
                'capacity': row[9]
            })

            print(course_sections)

        return render(request, 'student/courseSection_list.html', {'course_sections': course_sections})
    else:
        form = courseForm()
    return render(request, 'student/course_section.html', {'form': form})



def admin_performance(request):
    if request.method == 'POST':
        name = request.POST.get('professor_name')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        
        # Define SQL query
        query = """
            SELECT 
                COUNT(T.course_id) AS courses_taught, 
                SUM(S.capacity) AS total_students_taught, 
                SUM(R.amount) AS total_funding_saved, 
                COUNT(P.publication_id) AS papers_published 
            FROM 
                Teaches AS T 
                INNER JOIN Section AS S ON T.course_id = S.course_id AND T.sec_id = S.sec_id AND T.semester = S.semester AND T.year = S.year 
                INNER JOIN Instructor AS I ON T.teacher_id = I.id 
                LEFT JOIN Research AS R ON I.id = R.pid 
                LEFT JOIN Publications AS P ON I.id = P.Authors_id 
            WHERE 
                I.name = %s AND 
                S.year = %s AND 
                S.semester = %s 
            GROUP BY 
                I.name, S.year, S.semester
        """
        
        # Execute the SQL query
        with connection.cursor() as cursor:
            cursor.execute(query, [name, year, semester])
            row = cursor.fetchone()
        
        # Transform SQL result into a dictionary
        if row:
            results = {
                'courses_taught': row[0],
                'total_students_taught': row[1],
                'total_funding_saved': row[2],
                'papers_published': row[3]
            }
        else:
            results = {
                'courses_taught': 0,
                'total_students_taught': 0,
                'total_funding_saved': 0,
                'papers_published': 0
            }
        
        print(results)  # For debugging
        
        return render(request, "admin/f3.html", {'results': results})

    return render(request, "admin/f3.html")