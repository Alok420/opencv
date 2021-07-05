from django.shortcuts import render
from .forms import MyFileUploadForm
from .models import FileUpload
from django.http import HttpResponse
# Create your views here.
def hiHello(request):
    return render(request,"hi.html",{"name":"anupam"})
def index(request):
    if request.method=='POST':
        form=MyFileUploadForm(request.POST,request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            files=form.cleaned_data['files']
            FileUpload(name=name,files=files).save()
            return HttpResponse("File uploaded")
        else:
            return HttpResponse("Error occured")
    context={
        'form':MyFileUploadForm()
    }
    return render(request, "form.html", context)
def showAll(request):
    alldata=FileUpload.objects.all()
    context={
        'data':alldata
    }
    return render(request,'show.html',context)