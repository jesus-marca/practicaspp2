from django import forms
from .models import Comment, Reply, Lesson, SlotSubject

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('lesson_id','name','position','video','ppt','Notes')
        
        labels = {
        'lesson_id':'id del capitulo',
        'name':"nombre del capitulo",
        'position':"numero de capitulo",
        # 'slug':"identificador",
        'video':"video sobre el capitulo",      
        'ppt':'pdf',
        'Notes':'anotacionesss'        
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        labels = {"body":""}

        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':70, 'placeholder':"Ingresa tu comentario"}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)

        widgets = {
            'reply_body': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols':10}),
        }
        labels = {
        'reply_body':"Escribe una respuesta",
  
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ReplyForm, self).__init__(*args, **kwargs)

class SlotSubjectForm(forms.ModelForm):
    class Meta:
        model = SlotSubject
        fields = ('day','slot')
        labels = {
            # 'standard':'Nivel',
            'day':"dia",
            'slot':"espacio",
            # 'slot_subject':"curso",                              
        }