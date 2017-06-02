# osu-qqbot
一个用于查询osu信息和统计增长的qqbot</br>

环境: python3.5 + mysql5.7</br>
运行环境：Windows</br>
python模块: requests,pymysql</br>

qq命令:</br>
!stats osu_username</br>
qqbot只支持发送群信息</br>


目录说明：</br>
login.py: 主程序(不存在命名规则,后续版本引入插件模块)</br>
login.txt: 自动保存登录信息(包括cookies等,小心安全)</br>
qrcode.png: 登录用的二维码,会自动生成</br>
start.bat: 执行脚本</br></br>

Web QQ协议登录参考资料</br>
https://www.fkgeek.com/archives/59</br>
Web QQ协议收发消息参考资料</br>
http://www.scienjus.com/webqq-analysis-3/
