from ..inner_service_apis import InnerServices, InnerService
from ..errors import InnerAPIError


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
        return self.client.get_user(user_id)
