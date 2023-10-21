from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Movie(Base):

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    name = Column(String(200), nullable=False, comment='电影名称')
    classify = Column(String(100), nullable=False, comment='类别')
    actor = Column(String(500), nullable=False, comment='主演')
    cover_pic = Column(String(300), nullable=False, comment='封面')
    pics = Column(String(1000), comment='图片地址json')
    url = Column(String(300), comment='电影详细地址')
    play_url = Column(String(300), comment='播放地址')
    download_url = Column(String(300), comment='下载地址')
    description = Column(Text, comment='电影描述')
    magnet_url = Column(String(5000), comment='磁力下载地址')
    hash = Column(String(32), nullable=False, comment='唯一值')
    pub_date = Column(DateTime, comment='发布日期')
    source = Column(String(20), comment='来源')
    view_counter = Column(Integer, default=0, comment='阅览量')
    country = Column(String(20), comment='国家')
    updated_time = Column(DateTime, default=func.now(), onupdate=func.current_timestamp())
    created = Column(DateTime, default=func.now(), onupdate=func.current_timestamp())

    def __str__(self):
        return (
            f"Movie(id={self.id}, name='{self.name}', classify='{self.classify}', "
            f"actor='{self.actor}', cover_pic='{self.cover_pic}', pics='{self.pics}', "
            f"url='{self.url}', play_url='{self.play_url}', download_url='{self.download_url}', "
            f"description='{self.description}', magnet_url='{self.magnet_url}', hash='{self.hash}', "
            f"pub_date='{self.pub_date}', source='{self.source}', view_counter={self.view_counter}, "
            f"updated_time='{self.updated_time}', created='{self.created}')"
        )
