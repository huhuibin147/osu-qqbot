# osu-qqbot 
已经停止开发,迁移到interbot</br></br>
一个用于查询osu信息和统计增长的qqbot(~~现在用途只是被inter拿来同步代码~~） </br>
基于webQQ协议实现的最简单版本Bot,有兴趣了解协议的可阅读主程序</br>


环境: python3.5 + mysql5.7</br>
运行环境：Windows/~~Linux(二维码图片可能无法打开)~~</br>
python模块: requests,pymysql</br>

qq命令:</br>
!stats osu_username</br>
qqbot只支持发送群信息</br>

~~停止更新主程序,理由是太懒了!~~

目录说明：</br>
login.py: 主程序(不存在命名规则,后续版本引入插件模块)</br>
login.txt: 自动保存登录信息(包括cookies等,小心安全)</br>
qrcode.png: 登录用的二维码,会自动生成</br>
start.bat: 执行脚本</br></br>

~~曾经的版本计划:多线程引入,昵称引入,插件模块化~~

ps:很多无用文件夹,有些甚至是无关的!


Web QQ协议收发消息参考资料</br>
http://www.scienjus.com/webqq-analysis-3/
