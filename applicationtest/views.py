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
        paper_width = 600
        paper_heaight = 800
        path = "applicationtest/static/images/"+dir
        util.getDirFiles
        img = cv.imread(path)
        resized = cv.resize(img, (img.shape[1],img.shape[0]))
        img, gcontour = util.getCountours(resized, showCanny=False, draw=True, minArea=0, filter=4)
        if len(gcontour) != 0:
            biggest = gcontour[0][2]
            area = gcontour[0][1]
            print("first ",area)
            warp_image=util.warpImage(img,biggest,img.shape[1],img.shape[0])
            img2, gcontour2 = util.getCountours(warp_image, showCanny=False, draw=True, minArea=0, filter=12,isSecondRound=True,isSorted=True)
            screenshot_name = 'applicationtest/static/drawn_img/'+dir    
            cv.imwrite(screenshot_name, img2)
            if len(gcontour2) != 0:
                a=0
                biggest2 = gcontour2[1][2]
                area2 = gcontour2[1][1]
                color=gcontour2[1][5]
                peri=gcontour2[1][6]
                dia=peri/3.14
                for gc in gcontour2:
                    a+=1
                    biggest2 = gc[2]
                    # area2 = str(gc[0])+", "+str(gc[1])+", "+str(gc[3])
                    # color=str(gc[5][0])+str(gc[5][1]),str(gc[5][1])
                    # col=','.join(color)
                    # col="_"+str(a)+"_\t\t\t"+col
                    # print(util.colored(color[0],color[1],color[2],area2))
                    # print(util.colored(color[0],color[1],color[2],col))
            subdata = {
                "biggest2": biggest2,
                "area2": area2,
                "peri": peri,
                "dia": dia,
                "color": color,
                "img": dir
            }
            context.append(subdata)
    context2 = {
        "data": context
    }
    return render(request, "result.html", context2)
