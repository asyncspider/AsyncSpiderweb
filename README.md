# Asw 简介

AsyncSpiderWeb(Asw) 是一个适合企业爬虫部门或团队使用的高性能爬虫调度与管理平台。Asw 基于Tornado 和 Tortoise-ORM，这使得它拥有 "轻" 和 "快" 两个优点。

Asw 借鉴了 Scrapyd 的部分设计，并继承 Python3 中 Asyncio 库以及异步框架 Tornado 的优点。

![image](https://github.com/asyncins/Asw/blob/master/AsyncSpiderweb.jpg)


Asw 可以同时兼容 Scrapy 项目和符合目录结构设定的任何 Python 项目，这意味着你使用 Requests 库和 Aiohttp 库或者其他 Python 框架所编写的项目，都可以部署到 Asw，以实现
对项目的调度和管理。除了项目的部署和调度以外，它还具备用户注册、登录以及权限功能，这使得它很适合团队使用。

### 关于定时调度
由于集成了 Apscheduler，定时调度功能比之前更好用。现在它不仅支持周期性的定时任务，还支持一次性的即时任务或一次性的定时任务，为此我重写了 Apschduler 的部分代码，确保参数传递更简单和方便。
定时任务的时间格式分为 'date','interval' 和 'cron'，具体信息及详细时间格式参考 Apscheduler 文档。

### 关于用户权限和 API 访问记录
你可能会问"为什么不用 RBAC 权限管理模型？它可是公认最灵活的 Web 权限模型！"。实际上爬虫部门或爬虫团队的关系很简单，通常只有以下几种角色：

* 匿名用户 Anonymous
* 不懂技术的领导 Observer
* 爬虫工程师 Developer
* 懂技术的领导 Superuser

![image](https://github.com/asyncins/Asw/blob/master/images/%E6%B5%85%E6%B5%B7%E6%98%8C%E8%93%9D.png)

我将不懂技术的领导称之为观察者（Observer），因为他只需要查看 Index 页面展示的统计数据和漂亮的图标即可。爬虫工程师们通常会互相协作，帮助修改项目参数或修改定时
任务的时间及状态，所以没有必要将他们的访问权以用户身份进行隔离，这样他们才能够访问到其他同事部署的项目和添加的调度任务。懂技术的领导，那显然就是 Superuser 了，
相比爬虫工程师，Superuser 对于全局的掌控权限会更大，他对用户注册以及用户状态有着绝对的控制权。同时由于管理需要，Superuser 还可以查看 API 访问记录。
记录类似这样：

![image](https://github.com/asyncins/Asw/blob/master/images/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE_%E9%80%89%E6%8B%A9%E5%8C%BA%E5%9F%9F_20190218074724.png)

详细的记录着每个 API 的访问时间、访问者信息、请求方式、传递的参数以及 API 相应状态。

### 关于数据存储
经过多方面综合考虑，我认为使用 Sqlite 更适合项目 "轻" 和 "快" 的特点。使用者无需安装太多的依赖和配置，这很符合中国互联网产品 "开箱即用" 的优秀思维。
Tortoise-ORM 与 Tornado 相结合，确保项目的高性能，整个项目遵循了 Python 异步的思想，尽可能的使用官方提供的异步库，或者使用多线程、多进程
来避免阻塞（Tornado 和 aiofiles 也是这么做的）。

### 关于用户注册验证
通常来讲，用户注册验证码一般通过邮件或手机短信的方式发送。我认为这属于开放型的 Web 平台的选择，对于 Asw 这种企业内部或团队内部使用的平台，我更倾向与由
Superuser 授权。当用户注册后，Superuser 可以在平台上看到用户列表以及对应的验证码，只有 Superuser 将验证码告诉注册用户，注册用户才能够通过登录验证
（新用户只需要验证一次，以后无需再次验证）。这样的验证设计，是为了将更多的控制权交给 Supuser，同时省去了邮件发送或短信发送的配置。

### 关于测试
在项目发布之前，我们对所有的 Handler 和大部分方法进行了测试（我们希望 Asw 更稳定，同时也希望通过测试减少问题的产生）。你可以使用 Asw 项目中提供的测试
用例，也可以根据自己的需求增加新的测试代码。

