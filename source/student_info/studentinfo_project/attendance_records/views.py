from django.shortcuts import render
from . forms import LoginForm
from . models import Attendance,Student
# Create your views here.

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect(reverse("attendance_records:index"))

    return render(request,"attendance_records/login.html",{'title':'Login','form':form,'style':'forms'})


def index(request):
    attendance_data = Attendance.objects.all()
    return render(request,"attendance_records/index.html",{'title':'Home',"attendance_data":attendance_data})