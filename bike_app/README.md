# 寻路算法DEMO

因安全问题不公开本人使用的百度地图API密钥. 使用前请自行申请,申请后将./app/router.py中"你的百度api密钥"部分替换成自己的密钥

安装依赖库:

`pip install -r requirements.txt`

部分系统需要使用pip3代替pip

Windows 下运行flask环境(Linux和mac请参考flask官方文档):

`venv\Scripts\activate`(如果你使用了虚拟环境并命名为venv.如果没有请忽略这条)
`set FLASK_APP=run.py`
`set FLASK_DEBUG=1`
`flask run`

点控制台中显示的链接进入即可(一般是本机5000端口).

需要注意的是百度地图URI和百度地图API的寻路数据并不统一(百度地图API只有行走寻路,而百度地图URI只有骑行寻路)所以会导致前端显示距离和实际需要行走的距离并不一致.在商业上可以找百度公司公司商讨解决方案,这个demo代码和界面都比较粗糙, 仅起示范寻路算法逻辑作用.
为了展示效果,我们没有做在排序之前移除车辆当前所属围栏的操作,如果需要请自行添加
