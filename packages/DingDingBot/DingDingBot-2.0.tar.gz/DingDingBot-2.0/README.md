# DingDingbot 

## 在线安装
> pip install DingDingBot

## 使用方法
```
from DDBOT import DingDing
dd = DingDing(webhook='https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxx')
print(dd.Send_Text_Msg(Content='test:测试数据'))
print(dd.Send_Link_Msg(Content='test',Title='测试数据',MsgUrl='https://www.baidu.com',PicUrl='https://cn.bing.com/images/search?q=outgoing%e6%9c%ba%e5%99%a8%e4%ba%ba&id=FEE700371845D9386738AAAA51DCC43DC54911AA&FORM=IQFRBA'))
print(dd.Send_MardDown_Msg(Content="# 测试数据\n" + "> testone", Title='测试数据'))
```

#### 希望各位多多指教