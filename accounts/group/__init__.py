from django.contrib.auth.models import Group
from django.views.generic import ListView,View
from django.http import JsonResponse
from django.db import IntegrityError


class GroupListView(ListView):
    model = Group
    template_name = "user/grouplist.html"

class GroupCreateView(View):
    def post(self,request):
        group_name = request.POST.get("name","")
        ret = {"status":0}
        if not group_name:
            ret["status"] = 1
            ret["errmsg"] = "用户不能为空"
            return JsonResponse(ret)
        try:
            g = Group(name=group_name)
            g.save()
        except IntegrityError:
            ret["status"] = 1
            ret["errmsg"] = "用户已存在"
        return JsonResponse(ret)


class ModofyUserGroupView(View):
    def get(self,request):
        uid = request.GET.get('uid','')
        group_objs = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNoteExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list('id'))
        return JsonResponse(list(groups_objs.values("id","name")),safe=False)

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
 
