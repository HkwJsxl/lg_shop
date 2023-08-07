from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
# from django.core.cache import cache
from django.core.cache import caches

from areas.models import Areas
from response_code import RETCODE, err_msg
from logger import log
from constants import AREAS_EXPIRES


class AreasView(View):
    """省市区三级联动"""

    def get(self, request):
        area_id = request.GET.get("area_id")
        cache = caches['areas']
        try:
            if not area_id:
                province_list = cache.get("province_list")
                if not province_list:
                    province_queryset = Areas.objects.filter(pid__isnull=True)
                    province_list = [{"id": province_obj.id, "name": province_obj.name} for province_obj in
                                     province_queryset]
                    cache.set("province_list", province_list, AREAS_EXPIRES)
                return JsonResponse({"code": RETCODE.OK, "msg": "成功", "province_list": province_list})
            else:
                subs_list = cache.get("subs_list_%s" % area_id)
                if not subs_list:
                    subs_queryset = Areas.objects.filter(pid=area_id)
                    subs = []
                    for subs_obj in subs_queryset:
                        subs.append({
                            "id": subs_obj.id, "name": subs_obj.name,
                        })
                    subs_list = {
                        "id": area_id,
                        "name": subs_obj.pid.name,
                        "subs": subs
                    }
                    cache.set("subs_list_%s" % area_id, subs_list, AREAS_EXPIRES)
                return JsonResponse({"code": RETCODE.OK, "msg": "成功", "sub_data": subs_list})
        except Exception as e:
            log.error(str(e))
            return JsonResponse({"code": RETCODE.DBERR, "msg": "数据查询错误."})
