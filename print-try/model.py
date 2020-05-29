#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/10/15 16:29
author:    peak
description:
            数据库模型
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer, DateTime, Float, ForeignKey,Date
from sqlalchemy.orm import relationship
import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'  #表名字默认是类名字的小写版本(如果没有此语句)

    Id = Column(Integer(), primary_key=True)
    Tel_Number = Column(String(255), nullable=False)
    Password_Hash = Column(String(128))
    Register_Date = Column(Date, default=datetime.date.today())
    Role = Column(String(128), default='guest', nullable=False)
    Orders =relationship('Order', backref='User', lazy='dynamic')

class Order(Base):
    __tablename__ = "Order"

    Id = Column(Integer(), primary_key=True)
    File_Dir = Column(String(255), nullable=False)
    File_Name = Column(String(255))  # 文件原始名字
    Born_Date = Column(DateTime, default=datetime.datetime.now, nullable=False)  # 创建时间
    Born_Date_Day = Column(Date, default=datetime.date.today())  # 创建日期
    Time_Way = Column(Integer())  # 打印时间规划方式，自由排队
    Print_Date = Column(DateTime)  # 打印时间点 *
    Print_Place = Column(String(255), nullable=False)
    Print_pages = Column(Integer())  # 每份页数  *
    Print_Copies = Column(Integer())  # 份数
    Print_Direction = Column(String(255), nullable=False)  # 横向，纵向 +
    Print_Colour = Column(String(255), nullable=False)  # +
    Print_size = Column(String(255), nullable=False)
    Print_way = Column(String(255), nullable=False)  # 打印的方式，单面或双面
    Print_Money = Column(Float())  # 订单价格
    Print_Status = Column(Integer(), default=0)  # 订单状态，0:已提交文件但未支付, 1:已经支付但未打印, 2:已经加入下载队列, 3:已打印
    Trade_Number = Column(String(255))  # 支付订单号

    User_Id = Column(Integer(), ForeignKey('User.Id'), nullable=False)