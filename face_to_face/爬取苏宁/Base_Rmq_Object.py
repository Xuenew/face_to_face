# 若能避开猛烈的欢喜,自然也不会有悲痛的来袭,
# 迎着风雨走 孤独且自由,
# Author: xyy, time:2019/9/29

# 修改记录 2019 12 3
# 修改了心跳检测问题 heartbeat=0, 文章链接 http://www.bubuko.com/infodetail-3206758.html
# 队列持久化的意思 是 队列生成后及时服务重新启动 队列还在 但是东西没了
import time

import pika

from Config_Of_Rmq import config
class Base_Mq():# 一个基础的mq类
    """
    初始化 用户名和密码
    创建链接对象 / 也可以创建多个对象
    函数：
    1  ： 发起链接
    2  ： 获取队列信息
    3  ： 关闭队列信息
    4  ： 以后的心跳检测之类的函数扩展 。。。。
    """
    def __init__(self,que_name:str=""):#初始化 用户名和密码 用户名密码之类的应该放在配置文件里面
        self.que_name = que_name
        self.begain_check()
        self.username = config["username"]#用户名
        self.pwd = config["userpwd"]#用户密码
        self.user_pwd = pika.PlainCredentials(self.username, self.pwd)
        self.s_conn = pika.BlockingConnection(
                                pika.ConnectionParameters(host=config["host"], heartbeat=0,port=5672, credentials=self.user_pwd))
        self.chan = self.s_conn.channel()
    def begain_check(self)->"if not get que_name":
        if self.que_name=="":
            raise RuntimeError("please input the name of the que in the class Base_Mq")


    def get_mq(self,)->"获取队列里面的数据":
        que_name =self.que_name
        chan = self.chan
        method_frame, header_frame, body = chan.basic_get(queue=que_name, auto_ack=True)  # no_ack
        if not body:
            time.sleep(2)
            print("get-mq time.sleep")
            # self.s_conn.close()
            return 0
        else:
            # print(body)
            return body.decode("utf-8")

    def save_mq(self,url="")->"存东西进队列":
        que_name = self.que_name
        chan = self.chan
        chan.queue_declare(queue=que_name, auto_delete=False, durable=True)
        chan.basic_publish(exchange='', routing_key=que_name, body=url)
        return 0
    def close_mq(self)->"关闭队列的链接":#  此处应该还有心跳检测之类的函数
        print("get-mq time.sleep")
        self.s_conn.close()
        return 0

    # def isempty(self):
    #     que_name = self.que_name
    #     chan = self.chan
    #     chan.queue_declare(queue=que_name, auto_delete=False, durable=True)
    #     print(bool(chan.))
if __name__ == '__main__':
    p = Base_Mq(que_name="hai_z_w")
#     p.connect_mq()
# #     p.save_mq(que_name="hai_z_w",url="test 1234567")
# #     p.close_mq()
#     print(p.get_mq())
#     p.save_mq(url="testtttttt")
#     print(p.begain_check.__annotations__)