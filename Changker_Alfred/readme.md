### 脚本说明

**功能：**

个人编写的第一个较复杂的 Alfred 插件，用于提升日常运营工作的效率（相当有帮助！！！）：

1. user.py 获取用户基本信息，并展现用户最新的发言
2. hotel.py 获取酒店基本信息，并展现用户对该酒店的最新点评
3. membership.py 展现用户的会籍信息，并实现向 CMS 后台的快速跳转
4. notify.py 获取全体用户发布的消息流，使用 Mac 通知系统进行推送，对特定关键词进行强调显示
5. changkeshuo.py 监测用户@ 或者 评论 @常客说 账号的内容，使用 Mac 通知系统进行推送
6. closefeed.py 关闭推送
7. Changer.workflow Alfred 可用的 Workflow 文件


**说明：**

1. 需要调用 Alfred 专用的 Python 库 [alfred-workflow](https://github.com/deanishe/alfred-workflow)
2. 需要调用 Mac 通知系统的第三方库 [pync](https://github.com/SeTeM/pync)
3. 需要调用获取网络数据的第三方库 [requests](https://github.com/kennethreitz/requests)
4. 需要使用特定账号对应的 Token 进行验证，此处的配置文件逻辑实现的不够友好和私密，待2.0版发布后进行优化
5. 由于常客 APP 2.0 对底层接口进行了全面改版，因此部分功能已失效，待2.0版发布后进行优化
