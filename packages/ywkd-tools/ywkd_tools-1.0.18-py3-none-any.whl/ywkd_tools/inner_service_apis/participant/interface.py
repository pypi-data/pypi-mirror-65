from ywkd_tools.inner_service_apis.inner_service_apis import InnerServices, InnerService
from ywkd_tools.inner_service_apis.errors import InnerAPIError


@InnerServices.inner
class Participant(InnerService):
    """用户中心"""

    url = '/cperm/rpc/'

    def get_participant(self, participant_type, participant_id):
        """
        获取参与利润分配的公司/团体详情
                @param: participant_type: 类型
                    KTV: ktv
                    VOD: vod
                    代理商: agentibus
                    行业协会(机构): industry_association
                    垫付方: advance_party
                    音乐著作协会: music_copyright_society
                    权力方: copyright_party
                    平台: platform
                @param: id
                @out: {     // 返回内容参考: http://yapi.yuwangkedao.com/project/251/interface/api/6233
                    id: [id],
                    participant_type: 类型,
                    name: 名称,
                    area_code_list: 区域列表,
                    ...
                }
        """
        return self.rpc_client.get_participant(participant_type, participant_id)

    def filter_agentibus(self, id__in=None, name__contains=None, serial_number=None, pingpp_user_account_id=None,
            agency_area_code=None, enabled=None, page_index=1, page_size=100):
        """
        过滤代理商:
                例:
                    # 过滤 代理区域为"00420000", 启用状态为True 的代理商
                    filter_agentibus(None, None, None, None, "00420000", True)

                @param: id__in: 代理商id
                @param: name__contains: 代理商名称
                @param: serial_number: 代理商编号
                @param: pingpp_user_account_id: ping++账户
                @param: agency_area_code: 代理区域(code)
                @param: enabled: 是否启用
                @out:{
                    'data': [
                        # 参考: http://yapi.yuwangkedao.com/project/251/interface/api/6233 返回值
                        {
                            'id': 1092,
                            'name': '代理商名称',
                            'address': '西溪壹号24',
                            'agency_area_code': '00360000',
                            'enabled': True,
                            ...
                        }
                    ],
                    'page_index': 1,
                    'page_size': 100,
                    'total': 1
                }
        """
        return self.rpc_client.filter_agentibus(id__in, name__contains, serial_number, pingpp_user_account_id,
                                                agency_area_code, enabled, page_index, page_size)
