[toc]

# coolmovie

酷影（coolmovie）专注为用户提供免费观影体验，基于Python从0到1项目的开发web站点。

## 版本描述

当前版本```version1.0```

后续上线版本：```version2.0``` 预计完成会员信息更改，会员电影收藏，站点电影立即播放，关键字搜索、详细分类查询等功能。

## 说明

主要完成登录，注册功能，注销；获取电影首页，热度查询，最新查询，分页；电影详细信息，播放地址、下载地址等；热度推荐等。

## 技术栈

* 前端：JavaScript、HTML、CSS、Bootstrap。
* 后端：Python、Flask、sqlalchemy、MySQL、Crontab + 自定义Job框架+爬虫，Cookie+Session、 Uwsgi 多进程多线程管理服务。

## 如何使用

### 获取代码

```bash
git clone https://github.com/iceymoss/coolmovie.git
```



### 进入目录

```bash
cd coolmovie
```



### 建库建表

```sql
create database coolmovie
    DEFAULT CHARACTER SET = 'utf8mb4';

use coolmovie;

create table users(
    id int(11) unsigned primary key auto_increment,
    nickname varchar(30) not null,
    login_name varchar(20) not null,
    login_pwd varchar(32) not null ,
    login_salt varchar(32) not null comment '登录密码随机数',
    status    tinyint(3) default 1 not null comment '状态 0：无效， 1：有效',
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

alter table users add unique index uk_login_name (login_name);


create table movies(
    id int(11) unsigned primary key auto_increment comment '主键',
    name varchar (200) not null comment '电影名称',
    classify varchar(100) not null  comment '类别',
    actor varchar (500) not null comment '主演',
    cover_pic varchar(300) not null comment '封面',
    pics varchar (1000) comment '图片地址json',
    url varchar(300) comment '电影详细地址',
    play_url varchar(300) default null comment '播放地址',
    download_url varchar(300) default null comment '下载地址',
    description text default null comment '电影描述',
    magnet_url varchar(5000)  comment '磁力下载地址',
    hash  varchar(32) not null comment '唯一值',
    pub_date varchar(10) default null comment '发布日期',
    source varchar(20) default null comment '来源',
    view_counter int(11) default 0 comment '阅览量',
    country varchar(20) default null comment '国家',
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

alter table movies add unique index uk_hash (hash);
```



### 修改配置

将```application.py```中的MySQL配置修改为您的MySQL相关配置；修改```uwsgi.ini```配置，工具需求修改即可，Uwsgi 是多进程多线程管理服务。



### 拉取依赖(库)

获取所有依赖，包括：

```
flask
flask-sqlalchemy
pymysql
flask-script
flask_debugtoolbar
apscheduler
Flask-APScheduler
requests
BeautifulSoup4
uwsgi
```

直接使用命令获取所以依赖：

```bash
pip3 install -r requirement.txt
```

**注意：requirement.txt在项目目录下**

### 启动服务

```bash
uwsgi --ini uwsgi.ini
```

可以在```coolmovie/tmp/logs/movie.log```中查看服务是否启动成功。



## 数据来源

服务启动成功后，并没有任何数据，需要开启爬虫任务，直接使用命令：

```bash
python3 manager.py runjob -m movie
```

等待数据任务完成，任务默认获取3也内容，可自行修改。

**数据来源标注：https://www.bttian.com/ **



## 如何调试

在配置文件中将```base_setting.py```中改为：```DEBUG = True```即可，同样是启动服务，这里调试推荐命令：

```bash
python3 manager.py runserver 
```

