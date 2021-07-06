import threading
from applicationtest.api.VideoToFrame import VideoToFrame
from django.shortcuts import render
from .forms import MyFileUploadForm
from .models import FileUpload
from django.http import HttpResponse
import cv2 as cv
import os
import natsort 

# Create your views here.


def hiHello(request):
    return render(request, "hi.html", {"name": "anupam"})


def index(request):
    if request.method == 'POST':
        form = MyFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            files = form.cleaned_data['files']
            FileUpload(name=name, files=files).save()
            return HttpResponse("File uploaded")
        else:
            return HttpResponse("Error occured")
    context = {
        'form': MyFileUploadForm()
    }
    return render(request, "form.html", context)


def showAll(request):

    alldata = FileUpload.objects.all()
    context = {
        'data': alldata
    }
    return render(request, 'show.html', context)


def convert(request, id):
    obj = FileUpload.objects.get(ids=id)
    url=obj.files.url
    url="applicationtest/"+url
    vf=VideoToFrame()
    dir="applicationtest/static/images/"
    listpath= os.listdir(dir)
    listpath=natsort.natsorted(listpath,reverse=False)
    if len(listpath)>0:
        context = {
            "listpath": listpath
        }
        return render(request,"convert.html",context)
    else:
        capture=vf.readVideo(url)
        tr=threading.Thread(target=vf.toFrame,args=(capture,))
        tr.start()
        tr.join()
        context = {
            "obj": obj,
            "len":len(listpath)
        }
        return render(request,"convert.html",context)
def deleteAll(request):
     vf=VideoToFrame()
     vf.deleteAll("applicationtest/static/images/")
     return HttpResponse("Images deleted <a href='/applicationtest/show/'>go back</a>")
