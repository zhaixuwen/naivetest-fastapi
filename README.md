## NaiveTest接口测试平台介绍
NaiveTest接口测试平台是一个基于Python语言FastAPI框架开发的后端服务，配合hello-naive前端项目使用（[在线体验](http://zhaixuwen.top/login)）。

## 现有功能
NaiveTest接口现在提供的功能如下：
1. 测试用例中对接口状态码和响应json的校验
2. 测试集定时任务的执行
3. 测试集报告生成
4. 基于业务的token自动刷新

## 后续功能迭代
1. 测试用例中预执行脚本和变量设置
2. 增加用例执行前后SQL查询校验
3. 增加对响应中单独字段类型和内容的校验
4. 测试集报告的邮件发送和企业微信消息提醒

## 部署使用
1. 开发环境基于Python3.8.6
2. 导入requirements.txt文件中的包
3. 修改config.py文件下的MySQL和Redis地址
4. 修改apitest/task.py文件中的get_token方法为实际业务的token方式 
5. 在根路径下启动服务
```shell
uvicorn main:app --host:0.0.0.0 --port: 8000
```
