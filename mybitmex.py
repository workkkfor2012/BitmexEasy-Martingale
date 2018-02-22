import math

import datetime
from threading import Timer

from bitmex_websocket import Instrument
import asyncio
import websocket
import time
from bitmexClient import bitmexclient


class BitmexWS:
    def printlog(self, message):
        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('log.txt', 'a') as f:
            s = timestr + ":" + message + "\n"
            # s = str(s.encode("GBK"))
            print(s)
            f.write(s)

    def trigger(self):
        self.isInOrder = False

    def onMessage(self, message):
        # print(message)
        a1 = message["data"]
        # print(a1)
        # print(a1[0])
        b = 'lastPrice' in a1[0]
        c = 'timestamp' in a1[0]
        if b and c:
            lastprice = float(a1[0]['lastPrice'])
            #print("lastprice = "+str(lastprice))
            timestamp = a1[0]['timestamp']
            # pcj.on_last_price_update(str(lastprice))!!!!!!!!!!!!!!!!!
            gap = lastprice - self.bc.avgPrice
            if self.n % 10 == 0:
                self.printlog("lastprice = " + str(lastprice) + "self.bc.pos:" + str(self.prepos) + " gap = " + str(
                    gap) + " self.init_zhiying = " + str(self.init_zhiying) + " self.cengshu = " + str(self.cengshu))
            self.n = self.n+1
            if lastprice < self.lowcontrolPriceline:
                if self.bc.pos > 0 and self.cengshu >= 5:
                    # 关键点位上，持仓逆向，且层数过高，平仓避避风头
                    self.printlog(
                        "关键点位上，持仓逆向，且层数过高，平仓避避风头 self.bc.pos = " + str(self.bc.pos) + " self.cengshu = " + str(
                            self.cengshu))
                    self.orderClose()
            elif lastprice > self.highcontrolPriceline:
                if self.bc.pos < 0 and self.cengshu >= 5:
                    self.printlog(
                        "关键点位上，持仓逆向，且层数过高，平仓避避风头 self.bc.pos = " + str(self.bc.pos) + " self.cengshu = " + str(
                            self.cengshu))
                    self.orderClose()
            isshouldgo = self.isAfterOrderPosChange()
            if isshouldgo == False:
                return
                # 没有仓位，立刻开仓
            print("prepos", self.prepos)
            if self.prepos == 0:
                self.printlog("无仓位立刻开仓")
                self.order()
            else:
                if gap > 1000:
                    return
                # 当前持有多仓

                if self.prepos > 0:
                    # 大于止盈点数，平仓
                    if gap > self.zhiying():
                        self.printlog("持有多仓，超过盈利点数，平仓:" + str(gap))
                        self.orderClose()
                    # 处理多单亏损
                    else:
                        # 如果亏损超过初始设定，则加多仓
                        if gap < -self.init_jiacanggap:
                            self.printlog("持有多仓，亏损超过设定点数，加仓: " + str(gap))
                            self.order()
                        else:
                            pass
                            #print("持有多仓，不触发平仓和加仓 gap = "+str(gap))
                # 当前持有空仓
                elif self.prepos < 0:
                    # 价格下跌到空仓开仓价格100点，止盈
                    if gap < -self.zhiying():
                        self.printlog("持有空仓，超过盈利点数，平仓:" + str(gap))
                        self.orderClose()
                    # 处理空单亏损
                    else:
                        # 价格上升到空仓开仓价格超过初始设定，则加空仓
                        if gap > self.init_jiacanggap:
                            self.printlog("持有空仓，亏损超过设定点数，加仓" + str(gap))
                            self.order()
                        else:
                            pass
                            #print("持有空仓，不触发平仓和加仓 gap = " + str(gap))

    def orderClose(self):
        self.isInOrder = True
        self.bc.orderClose()
        self.cengshu = 0
        self.mypos = 0
        self.init_jiacanggap = 10
        self.isPosChange = True

    def order(self):
        self.isInOrder = True
        self.printlog("self.cengshu = " + str(self.cengshu))
        if self.prepos == 0:
            self.bc.orderauto(1)
        else:
            self.bc.orderauto(abs(self.prepos) * 2)
            # if self.bc.pos>self.mypos*3:
            #     self.bc.orderauto(self.mypos * 2)
            # else:
            #
            # #self.bc.orderauto(self.mypos*2)
            # self.mypos = self.mypos + self.mypos * 2
        self.cengshu = self.cengshu + 1
        if self.cengshu == 1:
            self.init_zhiying = 10
            self.init_jiacanggap = 10
        elif self.cengshu == 2:
            self.init_zhiying = 15
            self.init_jiacanggap = 15
        elif self.cengshu == 3:
            self.init_zhiying = 50
            self.init_jiacanggap = 70
        elif self.cengshu == 4:
            self.init_zhiying = 50
            self.init_jiacanggap = 70
        elif self.cengshu == 5:
            self.init_zhiying = 50
            self.init_jiacanggap = 70
        elif self.cengshu == 6:
            self.init_zhiying = 50
            self.init_jiacanggap = 70
        elif self.cengshu == 7:
            self.init_zhiying = 50
            self.init_jiacanggap = 70
        elif self.cengshu == 8:
            self.init_zhiying = 50
            self.init_jiacanggap = 70
        elif self.cengshu == 9:
            self.init_zhiying = 20
            self.init_jiacanggap = 160
        elif self.cengshu == 10:
            self.init_zhiying = 20
            self.init_jiacanggap = 160
        elif self.cengshu == 11:
            self.init_zhiying = 20
            self.init_jiacanggap = 160
        elif self.cengshu == 12:
            self.init_zhiying = 20
            self.init_jiacanggap = 160
        self.isPosChange = True

    def printlog(self, message):
        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('log1.txt', 'a') as f:
            s = timestr + ":" + message + "\n"
            # s = str(s.encode("GBK"))
            print(s)
            f.write(s)

    def isAfterOrderPosChange(self):
        # self.printlog(" isAfterOrderPosChange 仓位改变，等待"+str(self.isPosChange)+"self.prepos = "+str(self.prepos))
        if self.isPosChange == True:
            p = self.bc.getpos()
            if self.prepos == p:
                self.retryposchangetimes = self.retryposchangetimes + 1
                if self.retryposchangetimes >= 10:
                    self.retryposchangetimes = 0
                    self.isPosChange = False
                    return True
                self.printlog(" 仓位改变，等待")
                return False
            else:
                self.printlog(" 仓位改变完毕")
                self.prepos = p
                self.retryposchangetimes = 0
                self.isPosChange = False
                return True
        else:
            return True

    def zhiying(self):
        return self.init_zhiying

    def __init__(self):
        # 下限价格
        self.lowcontrolPriceline = 21000
        # 上限价格
        self.highcontrolPriceline = 9010
        # 赚了多少点就卖
        self.init_zhiying = 10
        # 每次加仓的价格间隔
        self.init_jiacanggap = 20
        # 初始仓位
        self.initorderPos = 1
        self.n = 0
        self.retryposchangetimes = 0

        self.isInOrder = False
        self.isPosChange = False
        self.cengshu = 0
        self.bc = bitmexclient()
        pos = self.bc.getpos()
        print("pos = ", pos)
        self.prepos = pos
        websocket.enableTrace(True)
        self.XBTH17 = Instrument(symbol='XBTUSD',
                                 # subscribes to all channels by default, here we
                                 # limit to just these two

                                 channels=['margin', 'instrument'],
                                 # you must set your environment variables to authenticate
                                 # see .env.example
                                 shouldAuth=True)

    def run(self):
        orderBook10 = self.XBTH17.get_table('instrument')
        self.XBTH17.on('action', self.onMessage)

# bws = BitmexWS()
# bws.run()


# 静态文件服务器
import http.server
import threading
httpd = http.server.HTTPServer(
    ('localhost', 8000),
    http.server.SimpleHTTPRequestHandler
)
threading.Thread(target=httpd.serve_forever).start()
# http://localhost:8000/web/app.html


# websocket
import asyncio
import websockets

async def hello(ws):
    print('on connect')
    while True:
        try:
            name = await ws.recv()
            print('on recv')
            await ws.send("Hello {}!".format(name))
        except:
            print('on close')
            break


asyncio.get_event_loop().run_until_complete(
    websockets.serve(hello, 'localhost', 3000)
)

asyncio.get_event_loop().run_forever()
