from ywkd_tools.inner_service_apis.inner_service_apis import InnerServices, InnerService
from ywkd_tools.inner_service_apis.errors import InnerAPIError


@InnerServices.inner
class MSG(InnerService):
    """消息"""

    url = '/cperm/rpc/'

    def send_msg(self, user_ids, msg, redirect_url=None, ignore_err=True):
        """
        发送站内消息
            @parms user_ids: 接收message 的用户id (可以为list)
            @parms msg: 消息内容
            @parms redirect_url: 跳转链接
            @parms ignore_err: 是否忽略错误
        """
        return self.rpc_client.send_msg(user_ids, msg, redirect_url, ignore_err)

    def send_email(self, user_ids, mail_subject, mail_message, countdown=None, eta=None, ignore_err=True):
        """
        发送email
            @parms user_ids: 接收email 的用户id (可以为list)
            @parms mail_subject: 邮件主题
            @parms mail_message: 邮件内容
            @parms countdown: 是否延迟发送, 延时几秒, 例如: countdown=5
            @parms eta: 是否延迟发送, 延时几秒, 例如: eta=datetime.datetime.utcnow() + datetime.timedelta(seconds=5) 注意时间必须为 utc时间
            @parms ignore_err: 是否忽略错误


        例:
            import datetime
            eta = datetime.datetime.utcnow() + datetime.timedelta(seconds=3)
            InnerServices.MSG().send_email([57], 'Email Test A', 'test', None, eta)
        """
        return self.rpc_client.send_email(
            user_ids, mail_subject, mail_message, countdown, eta, ignore_err)

    def send_sms(self, user_ids, sms_code, sms_params, countdown=None, eta=None, ignore_err=True):
        """
        发送短信
            @parms user_ids: 接收短信的用户id (可以为list)
            @parms sms_code: sms_code (在阿里短信后台配置)
            @parms sms_params: 模板参数 (必须与配置的模板匹配)
            @parms countdown: 是否延迟发送, 延时几秒, 例如: countdown=5
            @parms eta: 是否延迟发送, 延时几秒, 例如: eta=datetime.datetime.utcnow() + datetime.timedelta(seconds=5) 注意时间必须为 utc时间
            @parms ignore_err: 是否忽略错误

        例:
            InnerServices.MSG().send_sms([57], 'SMS_177552091', {'username': 'tester','password': 'pwd12345'}, 3)
        """
        return self.rpc_client.send_sms(user_ids, sms_code, sms_params, countdown, eta, ignore_err)
