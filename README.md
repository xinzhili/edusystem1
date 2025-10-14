manage.py: ​项目管理命令行工具。这是您与项目交互最常用的工具，用于启动开发服务器 (python manage.py runserver)、创建数据库迁移文件 (makemigrations)、执行迁移 (migrate)、创建超级用户等。
​settings.py: ​项目的核心配置文件。所有关键设置都在这里，包括：
          数据库配置（默认使用SQLite）
          已安装的应用程序列表 (INSTALLED_APPS)
          中间件配置 (MIDDLEWARE)
          模板 (Templates) 配置
          静态文件（CSS, JS, 图片）和媒体文件（用户上传）的路径设置
          国际化设置（语言、时区）
​urls.py: ​项目的总URL路由表（入口）​。它定义了URL地址（如 /admin/, /home/) 与对应的处理函数（视图）之间的映射关系。它通常会将不同App的URL包含进来，实现模块化管理。
wsgi.py: ​Web服务器网关接口配置文件。当您需要将项目部署到生产环境（如使用Apache、Nginx）时，这个文件是项目与WSGI兼容的Web服务器之间的接口。
asgi.py: ​异步服务器网关接口配置文件。与wsgi.py类似，但用于支持异步Web服务器（如Daphne），常用于需要处理WebSocket等异步功能的项目。
​admin.py: ​Django自带的后台管理站点配置。在这里，您可以将自己定义的数据模型（Models）注册到Django admin后台，从而拥有一个强大的图形化界面来增删改查数据。
​apps.py: ​当前应用程序的配置信息。主要用于配置应用本身，例如定义应用的名称。
​forms.py: ​定义表单。用于创建HTML表单，处理用户输入的数据验证。通常与数据模型关联，快速生成表单（ModelForm）。
​models.py: ​定义数据模型（Models）​。这是Django最重要的部分之一。您在这里用Python类来定义数据库的表结构。每个类对应一张数据库表，类的属性对应表的字段。Django的ORM（对象关系映射）会根据这些类自动生成数据库SQL命令。
​migrations/: ​数据库迁移文件目录。当您修改了models.py后，需要运行命令生成迁移文件（记录模型的变更），然后运行迁移命令来同步数据库结构。​此目录下的文件由Django自动生成，切勿手动修改。​
views/: ​视图函数/类的文件目录。视图是处理Web请求的核心，它接收请求（Request），处理业务逻辑（如查询数据库），然后返回响应（Response，如渲染一个HTML页面或返回JSON数据）。
templates/: ​HTML模板文件目录。Django使用模板来动态生成HTML页面。
​media/: ​媒体文件目录。用来存储上传的学情分析源文件。
corecode/: AI应用程序目录。
