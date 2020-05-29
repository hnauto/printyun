# 自助云打印
&nbsp;&nbsp;&nbsp;&nbsp;现在的打印店，特别是学校的打印店普遍遇到的问题就是，顾客拿着U盘或者手机去打印店打印东西，需要先将东西传到打印店的电脑上才能打印，如果人多的情况下就需要排队。那么现在有一个网站顾客可以通过手机或者电脑提前将文件上传，然后选择打印份数、黑白参数、横/纵后，在线通过微信/支付宝付款，系统返回给一个订单号，打印店的打印机自动根据这些信息打印，顾客拿着订单号到店直接取文件就可以解决很多麻烦的事情。  
  自助云打印系统就是为了解决这个问题而诞生的。  
  系统刚在起步阶段，目前已经可用，有如下功能：  
  1、支持电脑/手机远程上传文件  
  2、支持pdf、word、excel、ppt等常见打印文件  
  3、支持微信/支付宝支付（需要自行开通相应服务，或者使用第三方）  
  4、支付是否排版，考虑到打印样式繁多，如果选择需要排版，可先上传文件到服务器，顾客去打印店后告知老板打印要求，老板再通过系统直接打印，避免了U盘传输等。  
  5、老板可后台查看所有历史订单及需要排版的订单，可以在线预览/下载打印等  
## 说明
系统分为两部分：Web服务器端（print）和打印服务端（print-try）

  **作业流程图**
![](http://pic.printyun.cn/printyun_overflow.png)
 
 ## 效果图
 ![](http://pic.printyun.cn/%E4%BA%91%E6%89%93%E5%8D%B0%E7%A4%BA%E4%BE%8B.gif)

## 部署
系统分为两部分，其中print为Web服务端，可以部署到任何一台有python环境的电脑；print-try为打印机服务端，运行在连接打印机的树莓派上。    

### 先行工作
Web服务端用到了mysql和redis
下载后在两个文件夹内搜索文本“自行配置”，将所有数据库配置改为自己的数据库  
配置支付密钥和阿里sms  
print/app/certs 支付密钥文件    
print/app/sms.py 阿里sms相关配置  

### 1、Web服务端 
修改完上述位置配置后  
```python
pip install -r requirements.txt
flask run 
python worker.py  #再开一个shell执行此命令，如果不使用支付系统则可以不开启
```  
### 2、Docker部署  
上述配置修改好后  
```
docker image build -it printyun .
docker container run -d -p 8001:8001 --name printyun pringyun
```
宿主主机打开http://127.0.0.1:8001 看到hello world成功  

### 3、打印机端部署
树莓派连接打印机并进入系统，运行
```python
cd print-try
pip install -r requirements.txt
./restart.sh
```
之后，程序自动监测Web服务端，一旦发现上传文件并成功支付就会发送命令至打印机打印


## 相关URL
/login/login 登录  

## 部分截图
![](http://pic.printyun.cn/printyun1.png)
![](http://pic.printyun.cn/printyun2.png)
![](http://pic.printyun.cn/printyun3.png)










