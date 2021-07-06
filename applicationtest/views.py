import threading
from applicationtest.api.VideoToFrame import VideoToFrame
from applicationtest.api.Utils import Utils
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
    url = obj.files.url
    url = "applicationtest/"+url
    vf = VideoToFrame()
    dir = "applicationtest/static/images/"
    listpath = os.listdir(dir)
    listpath = natsort.natsorted(listpath, reverse=False)
    if len(listpath) > 0:
        context = {
            "listpath": listpath
        }
        return render(request, "convert.html", context)
    else:
        capture = vf.readVideo(url)
        tr = threading.Thread(target=vf.toFrame, args=(capture,))
        tr.start()
        tr.join()
        context = {
            "obj": obj,
            "len": len(listpath)
        }
        return render(request, "convert.html", context)


def deleteAll(request):
    vf = VideoToFrame()
    vf.deleteAll("applicationtest/static/images/")
    return HttpResponse("Images deleted <a href='/applicationtest/show/'>go back</a>")


def processing(request):
    util = Utils()
    dirs = util.getDirFiles()
    context = []
    for dir in dirs:
        scale = 1
        paper_width = 210*scale
        paper_heaight = 297*scale
        path = "applicationtest/static/images/"+dir
        util.getDirFiles
        img = cv.imread(path)
        resized = cv.resize(img, (500, 500), fx=0.5, fy=0.5)
        img, gcontour = util.getCountours(
            resized, showCanny=True, draw=False, minArea=0, filter=4)
        if len(gcontour) != 0:
            biggest = gcontour[0][2]
            area = gcontour[0][1]
            warp_image = util.warpImage(
                img, biggest, paper_width, paper_heaight)
            img2, gcontour2 = util.getCountours(
                warp_image, showCanny=False, draw=False, minArea=0, filter=12)
            print("Gcontours2 ", len(gcontour2))
            if len(gcontour2) != 0:
                biggest2 = gcontour2[0][2]
                area2 = gcontour2[0][1]
                color = gcontour2[0][5]
                # print("Area biggest ", area2)
                # print("circle biggest", biggest2)
                # print("Color biggest", color)
        subdata = {
            "biggest2": biggest2,
            "area2": area2,
            "color": color,
            "img": dir
        }
        context.append(subdata)
    context2={
        "data":context
    }
    return render(request, "result.html", context2)
