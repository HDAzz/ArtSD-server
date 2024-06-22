# ArtSD-Server

## stable-diffusion-webui部署

https://github.com/AUTOMATIC1111/stable-diffusion-webui

按照官网的说明根据不同的操作系统安装stable-diffusion-webui

将想要使用的模型的safetensors格式文件(或其他类型)拷贝至`./models/Stable-diffusion/`目录下(当前目录为项目文件根目录)

在项目文件根目录下输入

`./webui.sh --disable-model-loading-ram-optimization --api`

即可启动服务，注意要带上`--api`选项，否则无法调用相关api

## minio对象存储部署

https://min.io/download?license=agpl&platform=windows

按照指示根据不同的操作系统进行minio的安装

以windows操作系统为例，在powershell中输入以下命令，指定minio可执行文件的路径，指定数据存储的路径，服务运行的端口号即可

`PS> C:\minio.exe server F:\Data --console-address ":9001"`

默认配置下，minio api调用的端口号为9000，minio ui界面的访问端口号为9001，默认的用户名minioadmin，密码minioadmin

进入webui界面后，新建存储桶artsd，进入存储桶后，会有三个文件夹以及子目录结构分别为

- productions(上传的图片经过stablediffusion新生成的图片保存途径，可以通过程序自动生成)
  - year
    - month
      - Day
- uploads(客户端上传的图片，可以通过程序自动生成)
  - year
    - month
      - Day
- static(样例图保存路径，分为男女，注意路径要与picture集合中的相关字段保持一致，需要手动添加)
  - man
    - xxx.jpg
  - woman
    - xxx.jpg

## MongoDB部署

https://www.mongodb.com/docs/manual/installation/

按照说明根据不同的操作系统进行安装并启动服务

一共有四个集合(在RDBMS中的表)分别为

- picture
- device
- style
- behavior

数据库的数据实例已保存在`./db/xxx.json`文件中，可选择查看

## flask服务部署

首先，在启动flask服务之前，需要在项目根目录下的config.ini文件中填写相关的配置信息，包括

- mongodb的连接字符串
- minio的主机以及端口，用户名密码，存储桶名
- stablediffusion服务的主机以及端口号
- flask服务的主机以及端口号

安装好anaconda（推荐） https://www.anaconda.com/download/

在项目根目录下输入`conda env create --file environment.yml`创建虚拟环境

输入`conda activate ArtSD-server`激活环境

输入`python app.py`即可启动服务

