from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer
from .models import Student
from django.shortcuts import get_object_or_404  # ✅ Add this line
from rest_framework.exceptions import NotFound
from rest_framework import viewsets
@api_view(['GET'])
def student_list(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)  # ← this part is key!
    return Response(serializer.data)
class StudentViewSet(viewsets.GenericViewSet):
    queryset =Student.objects.all()
    serializer_class=StudentSerializer
    
    def list(self,request):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        try:
            student = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            raise NotFound("Student not found")