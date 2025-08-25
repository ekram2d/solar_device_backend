from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Student # type: ignore
from .models import User
from django.db.models import Q
import base64
def user_details(request,id):
    object = Student.objects.get(id=id)
    binary_data = object.profile_pic.read()
    base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')
    return JsonResponse( data={ 
		    'id':object.id,
            'username':object.user.username,
            'firstname':object.user.first_name,
		    'lastname':object.user.last_name,
  	        'email':object.user.email,
            'roll_no':object.roll_no,
		    'address':object.address,
		    'dept':object.dept,
		    'profile_pic':base64_encoded_data
      }	)
def delete_student(request, id):
    if request.method == 'DELETE':
        try:
            obj = Student.objects.get(id=id)
            obj.delete()
            return JsonResponse({"status": "success", "message": "Student deleted successfully"}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Student not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
from django.db.models import Q
def filter_students_api(request):
    search = request.GET.get('search', '')
    print('search',search)
    students = Student.objects.filter(
        Q(user__first_name__icontains=search) |
        Q(user__last_name__icontains=search) |
        Q(user__username__icontains=search)
    )

    students_list = []
    for student in students:
        # Encode profile picture if exists
        if student.profile_pic and hasattr(student.profile_pic, 'read'):
            binary_data = student.profile_pic.read()
            base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')
        else:
            base64_encoded_data = None

        students_list.append({
            'id': student.id,
            'username': student.user.username,
            'firstname': student.user.first_name,
            'lastname': student.user.last_name,
            'email': student.user.email,
            'roll_no': student.roll_no,
            'address': student.address,
            'dept': student.dept,
            'profile_pic': student.profile_pic.url if student.profile_pic else None,
        })
    CONTEXT={
        "page_title": "single_student",
        "student": student
    }
    # return render(request, 'student_page.html', CONTEXT)
    return JsonResponse({"status":"success","Students":students_list})
