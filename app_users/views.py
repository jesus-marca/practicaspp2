
# principales
from django.shortcuts import render,redirect
from app_users.forms import UserForm, UserProfileInfoForm,UserProfileUpdateInfoForm,UserUpdateForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from niveles.models import Standard
from .models import UserProfileInfo, Contact
from django.views.generic import CreateView

# para enviar correo

from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

def contact(request):
    if request.method=="POST":

        asunto="consulta"
        subject= asunto+" de "+request.POST["name"]+" "
        message=request.POST["message"]+" de "+request.POST["email"]
        email_from=settings.EMAIL_HOST_USER
        recipient_list=["jesusmarca47@gmail.com"]
        send_mail(subject,message,email_from,recipient_list)

        return render(request ,'app_users/contact.html')
  
    return render(request ,'app_users/contact.html')

def contactdd(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        subject=request.POST["subject"]
        message=request.POST["message"]
        
        template=render_to_string("email_temmplate_html",{
            "name":name,
            "email":email,
            "message":message            
        })
        emial=EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ["raigor370@gmail.com"]            
        )
        email.fail_silently=False
        email.send()
        
        messages.success(request,"se ha enviado tu correo")
        return redirect('index')
    

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("cuenta es desactivada")
        else:
            
            # return HttpResponse("ingrese datos correctamente")
            # return HttpResponseRedirect(reverse('register'))
            return render(request, 'app_users/login.html')

    else:
        return render(request, 'app_users/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def profile(request):
    u_form=UserUpdateForm
    p_form=UserProfileUpdateInfoForm
    
    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'app/profile.html',context)

def register(request):

    registered = False
    
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        profile_pic=request.FILES['profile_pic']
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.profile_pic=profile_pic
            profile.user = user
            profile.save()

            registered = True
            
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        next = request.POST.get('next', '/')
    
        return render(request, 'app_users/registration.html',
                            {'registered':registered,
                             'user_form':user_form,
                             'profile_form':profile_form})

class HomeView(TemplateView):
    template_name = 'app_users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        context['standards'] = standards
        context['teachers'] = teachers
        return context

class ContactView(CreateView):
    model = Contact
    fields = '__all__'
    template_name = 'app_users/contact.html'
