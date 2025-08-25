from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from app1.models import Student
from django.contrib import messages
from .models import Profile, Student  # Ensure you've imported your Student model
from django.shortcuts import redirect
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
from django.conf import settings
# Home page
def index(request):
    CONTEXT = {}
    CONTEXT['name'] = 'Django'
    return render(request, 'home.html', CONTEXT)

# About page
def about(request):
    return render(request, 'about.html')

# Student form submission and list display
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Student, User
import random,string
def generate_random_username(firstname, lastname):
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{firstname.lower()}_{lastname.lower()}_{random_part}"
def student(request):
    if request.method == 'POST':
        print(settings.EMAIL_HOST_USER)
        data = request.POST
        image = request.FILES

        username = data.get('username')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        phone = data.get('phone')  # Optional: add field in model if needed
        roll_no = data.get('roll_no')
        dept = data.get('dept')
        address = data.get('address')
        profile_pic = image.get('profile_pic')

        try:
            # ✅ Check for existing student with same roll number
            if Student.objects.filter(roll_no=roll_no).exists():
                messages.error(request, f"❌ Roll No '{roll_no}' already exists.")
            else:
                username = generate_random_username(firstname, lastname)
                # ✅ Create user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=firstname,
                    last_name=lastname,
                    email=email
                )

                # # ✅ Create student profile
                Student.objects.create(
                    user=user,
                    roll_no=roll_no,
                    dept=dept,
                    address=address,
                    profile_pic=profile_pic,
                    phone=phone
                )

                # ✅ Send welcome email
                subject = "Welcome to Our Platform"
                message = f"""
Hello {firstname},

🎉 Welcome to our platform!

✅ Username: {username}
✅ Password: {password}

Please keep your credentials safe.

Regards,
Admin
"""

                try:
                    send_status = send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    if send_status:
                        print("✅ Email sent successfully.")
                    else:
                        print("⚠️ Email not sent (returned 0).")

                except Exception as e:
                    print("❌ Email failed:", str(e))

                messages.success(request, "🎉 Student created and email sent successfully!")

        except Exception as e:
            print("Error occurred:", e)
            messages.error(request, f"❌ Error: {str(e)}")

        # Render student list again after POST
        students = Student.objects.all()
        return render(request, 'student_page.html', {
            "page_title": "Student Page",
            "students": students
        })

    else:
        # GET request: load the student list
        students = Student.objects.all()
        context = {
            "page_title": "Student Page",
            "students": students
        }
        return render(request, 'student_page.html', context)

def single_student(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        data=request.POST
        first_name=data.get('firstname')
        student.user.first_name=first_name
        student.user.save()
        messages.success(request, "Student data updated successfully!")
    CONTEXT={
        "page_title": "single_student",
        "student": student
    }
    return render(request, 'student_page.html', CONTEXT)
from django.db.models import Q


def filter_students(request):
    if request.method == "GET":
        data = request.GET.get('search', '')
        queryset = Student.objects.filter(
            Q(user__first_name__icontains=data) |
            Q(user__last_name__icontains=data) |
            Q(user__username__icontains=data) |
            Q(roll_no__icontains=data) |
            Q(dept__icontains=data)
        )
    else:
        queryset = Student.objects.all()

    context = {
            "page_title": "Filtered Students",
            "students": queryset
        }
    return render(request, 'student_page.html', context)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User  # if you're using a custom User model

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('home')  # ✅ use redirect instead of HttpResponse
            else:
                messages.error(request, 'Invalid credentials')

        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist')

        except Exception as e:
            messages.error(request, 'Something went wrong')
            print("Exception during login:", e)

    context = {
        'page_title': 'Login Page',
    }
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login_page')  # ✅ redirect instead of render
