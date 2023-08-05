from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    active = Column(Boolean, default=True)
    
    wallpapers = relationship("Wallpaper", back_populates='category', cascade="all", lazy='dynamic')

class Folder(Base):
    __tablename__ = 'folders'

    id = Column(Integer, primary_key=True)
    path = Column(String)

    wallpapers = relationship("Wallpaper", back_populates='folder', cascade="all, delete, delete-orphan", lazy='dynamic')

class Wallpaper(Base):
    __tablename__ = 'wallpapers'

    id = Column(Integer, primary_key=True)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    file_name = Column(String(255))
    name = Column(String(255), default="")
    category_id = Column(Integer, ForeignKey('categories.id'))
    current = Column(Boolean, default=False)
    last_time = Column(DateTime)
    times_used = Column(Integer, default=0)

    folder = relationship("Folder", back_populates='wallpapers', single_parent=True)
    category = relationship("Category", back_populates='wallpapers')
