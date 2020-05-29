from weixin.pay import WeixinPay, WeixinPayError
from app.models import Order
from flask import Blueprint, request
#将 字典 转为 xml 格式
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import requests



vx_pay = Blueprint('vxpay',__name__)


# 参考网址   https://blog.csdn.net/lm_is_dc/article/details/83312706

# 使用 weixin-python 处理字典可能会更简单一点

@vx_pay.route("/vxcreat",methods=['POST'])
def vxcreat():
    data = request.form
    tradeid = data['tradeid']
    dati = Order.query.filter(Order.Trade_Number == tradeid).first()
    cost = dati.Print_Money
    new_filename = dati.File_Name
    parse_pay = {
        'appid'         :       '公众账号ID',
        'mch_id'        :       '商户号',
        'nonce_str'     :       '随机字符串:随机字符串，长度要求在32位以内。推荐随机数生成算法',
        'sign'          :       '签名',
        'body'          :       '商品描述',
        'out_trade_no'  :       '商户订单号',
        'total_fee'     :       '订单总金额',
        'spbill_create_ip' :    '终端IP:支持IPV4和IPV6两种格式的IP地址。用户的客户端IP',
        'notify_url'    :       '异步通知地址',
        'trade_type'    :       '交易类型:JSAPI -JSAPI支付,NATIVE -Native支付,APP -APP支付',
        'openid'        :       '当交易类型为JSAPI时，此参数必传'
    }

    # 这里 没有使用 weixin-python , 因为 无法完成初始化，所以先使用了第三方转化
    books = Element('books')
    xml = tostring(books)

    # 在这里查看一下 是否转换成功
    print(xml)

    # 进行支付 需要以post的方法
    to_vx = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder',xml=xml)

    # 查看返回的数据类型格式， 如需转换， 可能需要用到 BS4 的 beautiful4库 进行页面信息整理抽取出 xml 中的内容
    print(to_vx.text)






@vx_pay.route("/notify",methods=['POST'])
def pay_notify():
    """
    微信异步通知
    """
    data = wx_pay.to_dict(request.data)
    if not wx_pay.check(data):
        return wx_pay.reply("签名验证失败", False)
    # 处理业务逻辑
    return wx_pay.reply("OK", True)