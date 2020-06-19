from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from todolist_app.models import tasklist
from todolist_app.forms import taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from todolist_app.serializers import todolistSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators  import api_view
from rest_framework.response import Response
from rest_framework import status
@login_required
def todolist(request):
    if request.method=="POST":
        form=taskform(request.POST or None)
        #print(form)
        if form.is_valid:
            form.save(commit=False).manage=request.user
            form.save()
            messages.success(request,("New Task Added"))
        return redirect('todolist')
    else:
        all_tasks=tasklist.objects.filter(manage=request.user)
        paginator=Paginator(all_tasks,12)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})
@login_required
def delete_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    if task.manage==request.user:
        task.delete()
    else:
        messages.success(request,("Access Restricted ,You are Not Allowed!"))
    return redirect('todolist')
@login_required
def edit_task(request,task_id):
    if request.method=="POST":
        task=tasklist.objects.get(pk=task_id)
        form=taskform(request.POST or None,instance=task)
        if form.is_valid():
            form.save()
            messages.success(request,(" Task Updated Successfully!"))
        return redirect('todolist')
    else:    
        task_obj=tasklist.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})
@login_required
def complete_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    if task.manage==request.user:
        task.done=True
        task.save()
    else:
         messages.success(request,("Access Restricted ,You are Not Allowed!"))

    return redirect('todolist')

@login_required
def pending_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    if task.manage==request.user:
        task.done=False
        task.save()
    else:
        messages.success(request,("Access Restricted ,You are Not Allowed!"))
    
    return redirect('todolist')
      
def contact(request):
    context={
        'contact_text':"Welcome to contact page",
    }
    return render(request,'contact.html',context)
def about(request):
    context={
        'about_text':"Welcome to about us page",
    }
    return render(request,'about.html',context)
def index(request):
    context={
        'index_text':"Welcome to Home page",
    }
    return render(request,'index.html',context)

from django.core.mail import EmailMessage
def email(request):
    
    if request.method=="POST":
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        if subject and message and email:
            try:
                msg=EmailMessage(subject, message, to=[email])
                msg.send()
            except BadHeaderError :
                return HttpResponse('Invalid header found.')
            return redirect('index')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    else:
        return render(request,'email.html')

def listview(request,task_id):
    print(tasklist.objects.values_list('id'))
    if request.method == 'GET':
        tasks =tasklist.objects.get(id=task_id)
        serializer = todolistSerializer(tasks)
        return JsonResponse(serializer.data)

    ''' l=(task_id,)
            if l not in tasklist.objects.values_list('id'):
                return Response(status=status.HTTP_404_NOT_FOUND)'''
    '''elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = todolistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
'''