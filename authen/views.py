from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistration, TeacherRegistration, StudentLogin, TeacherLogin, UpdateUserForm
from .models import FoundationalModel, StudentExtended, TeacherExtended, Student


def home(request):
  print(request.user.is_authenticated)
  return render(request, template_name="authen/home.html")


# This is an example of LISTVIEW in Django.
# It is helpful in extracting out all the records from a model,
# without explicitly writing every code.
# For more info on ListView: https://www.youtube.com/watch?v=SMZLAphM4Ik&list=PLbGui_ZYuhigchy8DTw4pX4duTTpvqlh6&index=112&pp=iAQB
class UserListView(ListView):
  # model from which we want the records
  model =  FoundationalModel
  
  # the template name
  template_name = 'authen/display_all_users.html'
  
  # it is something like: all_users = FoundationModel.objects.all()
  context_object_name = 'all_users'
  
  # we can also define our custom queryset api.
  def get_queryset(self):
     return super().get_queryset().filter(type = "STUDENT")
   
  # we can also define conditional templates for different users.
  def get_template_names(self):
    if self.request.user.is_anonymous:
      template_name = 'authen/anonymous_user.html'
    else:
      template_name = self.template_name
    return template_name


# this is a Function View equivalent of the ListView mentioned above.
# BUT, not much FLEXIBLE.
def userListView(request):
  all_users = FoundationalModel.objects.all()
  return render(request, template_name='authen/display_all_users.html', context={'all_users': all_users})



def create_student(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == "POST":
      form = StudentRegistration(request.POST)
      if form.is_valid():
          student = form.save(commit=True)
          StudentExtended.objects.create(user=student, standard=form.cleaned_data["standard"])
          return redirect('login_student')
  else:
      form = StudentRegistration()
  return render(request, template_name='authen/create_student.html', context={'form': form})


class CreateStudent(View):
  
  def get(self, request):
    form = StudentRegistration()
    return render(request, template_name='authen/create_student.html', context={'form': form})
  
  def post(self, request):
    form = StudentRegistration(request.POST)
    if form.is_valid():
        student = form.save(commit=True)
        StudentExtended.objects.create(user=student, standard=form.cleaned_data["standard"])
        return redirect('login_student')


def create_teacher(request):
    if request.method == "POST":
        form = TeacherRegistration(request.POST)
        if form.is_valid():
            teacher = form.save(commit=True)
            TeacherExtended.objects.create(user=teacher, subject=form.cleaned_data["subject"])
            return redirect('login_teacher')
    else:
        form = TeacherRegistration()
    return render(request, template_name='authen/create_student.html', context={'form': form})


def login_student(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  message = ''
  if request.method == "POST":
    form = StudentLogin(request.POST)
    if form.is_valid():
      student = authenticate(email = form.cleaned_data["email"], password = form.cleaned_data["password"])
      if student is not None:
        login(request, student)
        message = f"{student.type} {student.email} is now logged in!"
        messages.success(request, message)
        return redirect("home")
      else:
        messages.error(request, "Oops! Something Went Wrong! Please check your credentials.")
  else:
    form = StudentLogin()
    
  context = {'form': form, 'message': message}
  return render(request, template_name='authen/login.html', context=context)



@login_required
def update_user(request):
  student = get_object_or_404(Student, id=request.user.id)
  
  if request.method == 'POST':
      form = UpdateUserForm(request.POST, instance=student)
      if form.is_valid():
        form.save()
        return redirect('home')  # Redirect to appropriate page
  else:
    form = UpdateUserForm(instance=student)
  return render(request, 'authen/login.html', {'form': form})



def log_out(request):
  logout(request)
  return redirect('home')

def login_teacher(request):
  message = ''
  if request.method == "POST":
    form = TeacherLogin(request.POST)
    if form.is_valid():
      teacher = authenticate(email = form.cleaned_data["email"], password = form.cleaned_data["password"])
      if teacher is not None:
        login(request, teacher)
        message = f"{teacher.type} {teacher.email} is now logged in!"
      else:
        message = "Oops!"
  else:
    form = TeacherLogin()
    
  context = {'form': form, 'message': message}
  return render(request, template_name='authen/login.html', context=context)








def create_session(request):
  request.session["name"] = "Dev"
  request.session["age"] = 20
  request.session["is_student"] = True
  request.session.set_expiry(0)
  return render(request, template_name="authen/create_session.html")


def get_session(request):
  session = request.session
  print(session.get_session_cookie_age())
  print(session.get_expiry_age())
  print(session.get_expiry_date())
  print(session.get_expire_at_browser_close())
  return render(request, template_name="authen/get_session.html", context={'session': session})
# Create your views here.
