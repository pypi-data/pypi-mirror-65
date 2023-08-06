# -*- coding: utf-8 -*-

import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base64 import b64encode
from functools import wraps
from ywkd_tools.auth import Auth


@Auth.inner
def token_required(view_func):
    """检查用户是否有某权限"""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        basic_auth = request.META.get('HTTP_AUTHORIZATION')

        # 兼容老接口认证规则
        if not basic_auth and type(request.POST) != type([]):
            user_id = request.POST.get('user', request.GET.get('user'))
            token = request.POST.get('token', request.GET.get('token'))
            basic_auth = 'basic ' + b64encode('{}:{}'.format(user_id, token).encode('utf-8')).decode('utf-8')
            request.META['HTTP_AUTHORIZATION'] = basic_auth

        user = None
        try:
            user = Auth.RSTFBasciAuthentication().authenticate(request)[0]
        except Exception as e:
            # 兼容老接口认证规则
            traceback.print_exc()
            result = {"data": []}
            result.update({"code": 500102, "codemsg": u"token解析错误/权限限制"})
            return JsonResponse(result)

        request.user = user
        return view_func(request, *args, **kwargs)

    return _wrapped_view
