from django.views.generic import ListView
from django.contrib.auth.models import User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponse,JsonResponse,QueryDict

class UserListView(LoginRequiredMixin,ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 10

class ModifyUserStatusView(View):
    def post(self,request):
        uid = request.POST.get("uid","")
        print(uid)
        ret = {"status":0}
        try:
            user_obj = User.objects.get(id=uid)
            if user_obj.is_active:
                user_obj.is_active = False
            else:
                user_obj.is_active = True
            user_obj.save()
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户名和密码错误"
        return JsonResponse(ret)

class ModifyUserGroupView(View):
    def get(self,request):
        uid = request.GET.get('uid','')
        group_objs = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNoteExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list('id'))
        return JsonResponse(list(group_objs.values("id","name")),safe=False)

    def put(self,request):
        ret = {"status":0}
        data = QueryDict(request.body)
        uid = data.get("uid","")
        gid = data.get("gid","")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNoteExist:
            ret["status"] = 1
            ret["errmsg"] = "yonghubucunzau"
            return JsonResponse(ret)
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNoteExist:
            ret["status"] = 1
            ret["errmsg"] = "user group exist!"
            return JsonResponse(ret)
        user_obj.groups.add(group_obj)
        return JsonResponse(ret)

