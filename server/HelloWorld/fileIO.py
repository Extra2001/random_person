from django.http import HttpResponse
import json


def hello(request):
    return HttpResponse("Hello world ! ")
def filei(request):
    request.encoding = 'utf-8'
    filer = open("namelist.txt", "r",encoding="utf8")
    idlist = []
    for i in filer:
        if i.startswith('-/~'):
            idlist.append(int(i.split('-/~')[1].split('\n')[0]))
    filer.close()
    file = open("namelist.txt", "a+")
    file.write("-/~"+str(idlist.__len__())+'\n')
    file.write('.:~'+str(request.POST['namename'])+'\n')
    file.write(str(request.POST['namelist'])+'\n')
    file.close()
    result={"id":idlist.__len__()}
    response = HttpResponse(json.dumps(result), content_type="application/json", charset='utf-8')
    response['Access-Control-Allow-Origin']='*'
    return response
def getlistname(request):
    filer = open("namelist.txt", "r",encoding="utf8")
    idlist = []
    namelist = []
    for i in filer:
        if i.startswith('-/~'):
            idlist.append(int(i.split('-/~')[1].split('\n')[0]))
        if i.startswith('.:~'):
            namelist.append(i.split('.:~')[1].split('\n')[0])
    filer.close()
    result={"array":list(zip(idlist,namelist))}
    response = HttpResponse(json.dumps(result), content_type="application/json", charset='utf-8')
    response["Access-Control-Allow-Origin"] = "*"
    return response
def getlist(request):
    request.encoding = 'utf-8'
    id = int(request.POST['id'])
    filer = open("namelist.txt", "r",encoding="utf8")
    namelist = []
    name = ''
    flag = 0
    for i in filer:
        if flag==1:
            break
        if i.startswith('-/~'):
            if int(i.split('-/~')[1].split('\n')[0]) == id:
                count = 0
                for j in filer:
                    if count == 0:
                        name = j.split('.:~')[1].split('\n')[0]
                        count += 1
                        continue
                    else:
                        if j.startswith('-/~'):
                            flag = 1
                            break
                        namelist.append(j.split('\n')[0])
    filer.close()
    result = {
        "id": id,
        "name": name,
        "list": namelist
    }
    response = HttpResponse(json.dumps(result), content_type="application/json", charset='utf-8')
    response["Access-Control-Allow-Origin"] = "*"
    return response
def deletefile(request):
    request.encoding = 'utf-8'
    id = int(request.POST['id'])
    import os
    filer = open("namelist.txt", "r", encoding="utf8")
    filew = open("namelist_tmp.txt", "w", encoding="utf8")
    flag = 0
    flag1 = 0
    count = 0
    for i in filer:
        if i.startswith('-/~'):
            if int(i.split('-/~')[1]) == id:
                flag = 1
                flag1 = 1
                count += 1
                continue
            else:
                if flag1 == 1:
                    filew.write('-/~' + str(count - 1) + '\n')
                else:
                    filew.write(i)
                flag = 0
                count += 1
                continue
        else:
            if flag == 0:
                filew.write(i)
            else:
                continue
    filer.close()
    filew.close()
    filer = open("namelist_tmp.txt", "r", encoding="utf8")
    filew = open("namelist.txt", "w", encoding="utf8")
    for i in filer:
        filew.write(i)
    filer.close()
    filew.close()
    os.remove("namelist_tmp.txt")
    result = {"Done": "Done!"}
    response = HttpResponse(json.dumps(result), content_type="application/json", charset='utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    return response