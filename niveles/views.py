from urllib import request
from django.shortcuts import get_object_or_404, redirect, render 
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)
from app_users.forms import UserForm, UserProfileInfoForm

#usuarios
from app_users.models import UserProfileInfo, User
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from .models import Standard, Subject, Lesson, Comment, WorkingDays, TimeSlots,SlotSubject
from django.urls import reverse_lazy
from .forms import CommentForm,ReplyForm, LessonForm, SlotSubjectForm
from django.http import HttpResponseRedirect

# para enviar correo

from django.core.mail import EmailMessage
from django.template.loader import render_to_string



class StandardListView(ListView):
    context_object_name = 'standards'
    extra_context = {
        'slotsSubjectAll':SlotSubject.objects.all(),
        
        "usersAll":UserProfileInfo.objects.all(),
        "numeroNiveles":Standard.objects.all(),
        "numeroCursos":Subject.objects.all(),
        "numeroCapitulos":Lesson.objects.all(),
        "subjectsAll":SlotSubject.objects.all(),
        "numeroComentarios":Comment.objects.all(),
        
        #de prueba
        # "subjectslot1":SlotSubject.objects.filter(standard=1),
        # "subjectslot2":SlotSubject.objects.filter(standard=2),
        # "subjectslot3":SlotSubject.objects.filter(standard=3),
        # "subjectslot4":SlotSubject.objects.filter(standard=4),
        # "subjectslot5":SlotSubject.objects.filter(standard=5),
        #--------------
        
        'cursos':Subject.objects.all(),
        'slots': TimeSlots.objects.all(),
        
        #de prueba
        # 'cursos1': Subject.objects.filter(standard=1),
        # 'cursos2': Subject.objects.filter(standard=2),
        # 'cursos3': Subject.objects.filter(standard=3),
        # 'cursos4': Subject.objects.filter(standard=4),
        # 'cursos5': Subject.objects.filter(standard=5),
        #-------------
        'lessonsAll':Lesson.objects.all(),
        
        #de prueba
        # 'lesson1':Lesson.objects.filter(Standard=1),
        # 'lesson2':Lesson.objects.filter(Standard=2),
        # 'lesson3':Lesson.objects.filter(Standard=3),
        # 'lesson4':Lesson.objects.filter(Standard=4),
        # 'lesson5':Lesson.objects.filter(Standard=5),
        #------------
    }
    model = Standard
    template_name = 'niveles/standard_list_view.html'
 
class UsersListView(ListView):
    context_object_name = 'standards'
    extra_context = {
        "usersAll":UserProfileInfo.objects.all(),
    }
    model = Standard
    template_name = 'niveles/user_list_view.html'
    
class SubjectListView(DetailView):
    context_object_name = 'standards'
    extra_context = {
        'slots': TimeSlots.objects.all()
    }
    model = Standard
    template_name = 'niveles/subject_list_view.html'

class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'niveles/lesson_list_view.html'

class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'niveles/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm
    
    extra_context={
        "usuarios":UserProfileInfo.objects.all(),
        "total_usuarios": User.objects.all()
        
    }
    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name=='form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)


    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('niveles:lesson_detail',kwargs={'standard':standard.slug,
                                                             'subject':subject.slug,
                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = LessonForm
    context_object_name = 'subjects'
    model= Subject
    template_name = 'niveles/lesson_create.html' 

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
  
        return reverse_lazy('niveles:standard_list')
 
 
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object 
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonUpdateView(UpdateView):
    fields = ('name','position','video','ppt','Notes')
    model= Lesson
    template_name = 'niveles/lesson_update.html'
    context_object_name = 'lessons'
    

class LessonDeleteView(DeleteView):
    model= Lesson
    context_object_name = 'lessons'
    template_name = 'niveles/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject        
        return reverse_lazy('niveles:standard_list')

class SlotSubjectListView(ListView):
    context_object_name = 'standards'
    extra_context = {
        "total":Standard.objects.all(),
        'slotsAll': TimeSlots.objects.all(),
        "usersAll":UserProfileInfo.objects.all(),
        "numeroNiveles":Standard.objects.all(),
        "numeroCursos":Subject.objects.all(),
        "numeroCapitulos":Lesson.objects.all(),
        "subjectsAll":SlotSubject.objects.all(),
        "numeroComentarios":Comment.objects.all(),
                
        'cursos':Subject.objects.all(),
        'slots': TimeSlots.objects.all(),
        
        'lessonsAll':Lesson.objects.all(),        
    }
    model = Standard
    template_name = 'niveles/slot_list.html'
    
class SlotSubjectCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class =  SlotSubjectForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'niveles/slot_subject_create.html' 

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
  
        return reverse_lazy('niveles:slots_list')
 
 
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.standard = self.object.standard
        fm.slot_subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class SlotUpdateView(UpdateView):
    fields = ('day','slot')
    model= SlotSubject 
    template_name = 'niveles/slot_update.html'
    context_object_name = 'slotSubjects'


def user_update(request,id):
    userprofile = UserProfileInfo.objects.get(id= id)
    data = {
        
        'usuario':userprofile
    }
    return render(request,'niveles/user_update.html',data)


def edit_user(request):
 
    try :
        id = int(request.POST['id'])
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        bio = request.POST['bio']
        user_type= request.POST['user_type']
        
        userprofile = UserProfileInfo.objects.get(id = id)  
        
        us=User.objects.get(id=userprofile.user.id)
        try :
            profile_pic =request.FILES['profile_pic']
        except:
            

            profile_pic=request.FILES['profile_pic']
            profile_pic = userprofile.profile_pic 

                
        us.username = username
        us.first_name = first_name
        us.last_name = last_name
        us.email = email        
        us.save()
        userprofile.profile_pic =profile_pic
        userprofile.user=us
        userprofile.bio = bio
        userprofile.user_type = user_type        
        userprofile.save()
    except :
        pass
            
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


def user_delete(request,id):
    userprofile = UserProfileInfo.objects.get(id= id)
    data = {
        
        'usuario':userprofile
    }
    return render(request,'niveles/user_delete.html',data)

def delete_user(request):
    id = int(request.POST['id'])
    userprofile = UserProfileInfo.objects.get(id = id)    

    us=User.objects.get(id=userprofile.user.id)
    us.delete()            
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


def slot_subject_update(request,id):
    slotsubject = SlotSubject.objects.get(id= id)
    data = {
        
        'slotsSubjectt':slotsubject
    }
    return render(request,'niveles/slot_update.html',data)

def edit_slot_subject(request):
    
    id = int(request.POST['id'])
    day=int(request.POST['day'])
    slot=request.POST['slot']
    
    
    slotSubject = SlotSubject.objects.get(id = id) 
    
    slot_item = TimeSlots.objects.get(id=slot)

    day_item=WorkingDays.objects.get(id=day)
    
    slotSubject.slot=slot_item
    slotSubject.day=day_item
    
    slot_item.save()
    day_item.save()
    slotSubject.save()
                
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

# hora de inicio y final

def horaI(n):
    if(n == '1'): 
        return "08:00:00"
    if(n == '2'):
        return "09:00:00"
    if(n == '3'):
        return "10:00:00"
    if(n == '4'):
        return "11:00:00"
    if(n == '5'):
        return "12:00:00"
    if(n == '6'):
        return "13:00:00"
    if(n == '7'):
        return "14:00:00"
    
    
def horaF(n):
    if(n == '1'):
        return "09:00:00"
    if(n == '2'):
        return "10:00:00"
    if(n == '3'):
        return "11:00:00"
    if(n == '4'):
        return "12:00:00"
    if(n == '5'):
        return "13:00:00"
    if(n == '6'):
        return "14:00:00"
    if(n == '7'):
        return "15:00:00"
    

# ---------------------

def slot_subject_delete(request,id):
    slotsubject=SlotSubject.objects.get(id= id)
    data = {
        
        'slotsSubjectt':slotsubject
    }
    return render(request,'niveles/slot_delete.html',data)
    

def delete_slot_subject(request):
    id = int(request.POST['id'])
    slotsubject = SlotSubject.objects.get(id = id)    
    slotsubject.delete()
               
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)