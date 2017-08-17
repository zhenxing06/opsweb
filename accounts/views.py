from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View,TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    else:
        username = request.POST.get("username", "")
        #userpass = request.POST.get("userpass", "")
        userpass = request.POST.get("password", "")
        print("username: ", username)
        print("userpass: ", userpass)
        user = authenticate(username=username, password=userpass)
        ret = {"status":0,"errormsg":""}
        print(user)
        if user is not None:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next",None) else "/"
        else:
            ret['status'] = 1
            ret['errormsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login")) 


def user_list_view(request):
    user_queryset = User.objects.all()
    for user in user_queryset:
        print(user.username,user.email)
    return render(request,"user/userlist.html",{"userlist":user_queryset})

class User_ListView(View):
    
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        user_queryset = User.objects.all()
        #return HttpResponse("HEllo world")
        return render(request,"user/userlist.html",{"userlist":user_queryset})

class UserListView(TemplateView):
    template_name = "user/userlist.html"
