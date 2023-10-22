from urllib import request
from django.shortcuts import render 
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)

#usuarios
from app_users.models import UserProfileInfo
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
        "usersAll":UserProfileInfo.objects.all(),
        "numeroNiveles":Standard.objects.all(),
        "numeroCursos":Subject.objects.all(),
        "numeroCapitulos":Lesson.objects.all(),
        "subjectsAll":SlotSubject.objects.all(),
        "numeroComentarios":Comment.objects.all(),
        
        #de prueba
        "subjectslot1":SlotSubject.objects.filter(standard=1),
        "subjectslot2":SlotSubject.objects.filter(standard=2),
        "subjectslot3":SlotSubject.objects.filter(standard=3),
        "subjectslot4":SlotSubject.objects.filter(standard=4),
        "subjectslot5":SlotSubject.objects.filter(standard=5),
        #--------------
        
        'cursos':Subject.objects.all(),
        'slots': TimeSlots.objects.all(),
        
        #de prueba
        'cursos1': Subject.objects.filter(standard=1),
        'cursos2': Subject.objects.filter(standard=2),
        'cursos3': Subject.objects.filter(standard=3),
        'cursos4': Subject.objects.filter(standard=4),
        'cursos5': Subject.objects.filter(standard=5),
        #-------------
        'lessonsAll':Lesson.objects.all(),
        
        #de prueba
        'lesson1':Lesson.objects.filter(Standard=1),
        'lesson2':Lesson.objects.filter(Standard=2),
        'lesson3':Lesson.objects.filter(Standard=3),
        'lesson4':Lesson.objects.filter(Standard=4),
        'lesson5':Lesson.objects.filter(Standard=5),
        #------------
    }
    model = Standard
    template_name = 'curriculum/standard_list_view.html'
 
class UsersListView(ListView):
    context_object_name = 'standards'
    extra_context = {
        "usersAll":UserProfileInfo.objects.all(),
    }
    model = Standard
    template_name = 'curriculum/user_list_view.html'
    
class SubjectListView(DetailView):
    context_object_name = 'standards'
    extra_context = {
        'slots': TimeSlots.objects.all()
    }
    model = Standard
    template_name = 'curriculum/subject_list_view.html'

class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'curriculum/lesson_list_view.html'

class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_detail_view.html'
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
        # print("the form name is : ", form)
        # print("form name: ", form_name)
        # print("form_class:",form_class)

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
        return reverse_lazy('curriculum:lesson_detail',kwargs={'standard':standard.slug,
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
    context_object_name = 'subject'
    model= Subject
    template_name = 'curriculum/lesson_create.html' 

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
  
  
        #regresar a la normalidad si no se puede
        # return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,
        #                                                      'slug':self.object.slug}) 
        return reverse_lazy('curriculum:lesson_detail', kwargs={'slug':self.slug, 'standard':self.Standard.slug,'subject':self.subject.slug})
 
 
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
    template_name = 'curriculum/lesson_update.html'
    context_object_name = 'lessons'
    

class LessonDeleteView(DeleteView):
    model= Lesson
    context_object_name = 'lessons'
    template_name = 'curriculum/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject
        #return antes de optimizar
        # return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,'slug':subject.slug})
        return reverse_lazy('curriculum:standard_list')

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
    template_name = 'curriculum/slot_list.html'
    
class SlotSubjectCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class =  SlotSubjectForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'curriculum/slot_subject_create.html' 

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
  
  
        #regresar a la normalidad si no se puede
        # return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,
        #                                                      'slug':self.object.slug}) 
        # return reverse_lazy('curriculum:slots_list', kwargs={'slug':self.slug, 'standard':self.Standard.slug,'subject':self.subject.slug})
        return reverse_lazy('curriculum:slots_list')
 
 
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.standard = self.object.standard
        fm.slot_subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
