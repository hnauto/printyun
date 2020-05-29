from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# 自行配置
engine = create_engine('mysql+mysqlconnector://connect:XXX@XXX.XXX.XXX.XXX:3306/print?charset=utf8') 
DBSession =sessionmaker(bind=engine)  # 将数据库关系映射为Python中的对象，不用直接写SQL ，缺点是性能略差
