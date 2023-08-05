from ywkd_tools.inner_service_apis.inner_service_apis import InnerServices, InnerService
from ywkd_tools.inner_service_apis.errors import InnerAPIError


@InnerServices.inner
class Cperm(InnerService):
    """用户中心"""

    url = '/cperm/rpc/'

    def get_user(self, user_id):
        """
        获取用户详情
            @param: user_id 用户id
            @out: {     // 返回内容参考: http://yapi.yuwangkedao.com/project/251/interface/api/6341
                id: [用户id],
                user_type: 用户类型,
                avatar: 头像,
                belong_participant: {   // 所属公司
                    id: [公司id],
                    participant_type: [公司类型]
                    ...
                },
                ...
            }
        """
        return self.rpc_client.get_user(user_id)

    def check_api_operate_perms(self, user_id, token, service_name, api_name, operator_type):
        """
        检测当前token是否可以对当前 api 进行操作
            @param: user_id 用户id
            @param: token 用户token
            @param: service_name 服务名称 例如"KTV"
            @param: api_name api名
            @param: operator_type 操作类型 比如: GET, POST, PUT

            @out {"code": [返回码], "codemsg": [消息内容]}
                成功: {"code": 0, "codemsg": u"请求成功"}
                失败: {"code": 500104, "codemsg": u"用户被禁用或token值不对"}
                      {"code": 500102, "codemsg": u"用户无权限"}
                      {"code": 500016, "codemsg": u"用户被禁用/已删除"}
        """
        return self.rpc_client.check_api_operate_perms(
            user_id, token, service_name, api_name, operator_type)

    def filter_users(self, id__in=None, user_type__in=None, phone__in=None, nickname__contains=None,
                is_active=None, is_all_area=None, belong_participant_id__in=None,
                group_codes__in=None, permission_codes__in=None, page_index=1, page_size=100):
        """
        过滤用户:
            例:
                # 过滤 角色code 为 CEO,CTO 的用户
                filter_users(None, None, None, None, None, None, None, ['ceo', 'cto'])

            @out:
                {
                    "total": 2,     # 总数
                    "page_index": 1,    # 当前页 起始页 1
                    "page_size": 100,   # 每页大小
                    "data": [{
                        "id": 57,       # user_id
                        "user_type": "employee",    # 用户类型
                        "phone": "13644092",        # 手机号
                        "nickname": "昵称A",        # 昵称
                        "gender": 1,                # 性别
                        "is_all_area": False,       # 是否全国
                        "area_code_list": [],       # 区域codes
                        "serial_number": "000018",  # 序列号
                        "belong_participant": None, # 所属公司
                        "group_codes": ["ceo"]      # 所属组 codes
                    }, {
                        "id": 21,
                        "user_type": "agentibus",
                        "phone": "13644099810",
                        "nickname": "ABC",
                        "gender": 1,
                        "is_all_area": True,
                        "area_code_list": ["00320200", "00330100"],
                        "serial_number": "110007",
                        "belong_participant": {
                            "id": 1005,
                            "participant_type": "agentibus",
                            "area_code_list": ["00120000", "00120100", "00120101"],
                            "address": "西溪壹号",
                            "contact": "联系人A",
                            "telephone": "0411-84620027",
                            "comment": "备注B",
                            "serial_number": "DLS0005"
                        },
                        "group_codes": ["ceo"]
                    }]
                }
        """
        return self.rpc_client.filter_users(
                id__in, user_type__in, phone__in, nickname__contains,
                is_active, is_all_area, belong_participant_id__in,
                group_codes__in, permission_codes__in, page_index, page_size)
