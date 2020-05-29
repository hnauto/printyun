from config import DBSession
from model import Order, User
from PDF import pdf
import time, requests, os, subprocess, datetime


def Query():
    Session1 = DBSession()
    # 获取Order表中的符合要求列
    All_order = Session1.query(Order).filter(Order.Print_Status == 1).all()
    # 判断 如果存在
    if All_order:
        # 循环所有列，获取
        for one in range(len(All_order)):
            if All_order[one].Born_Date_Day == datetime.date.today():
                # if All_order[one].Print_Status == 1:
                try:
                    print('Datetime :' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\nId:' + str(
                        All_order[one].Id))  # 实例化当前时间

                    # 访问文件地址 进行下载与保存
                    # 自行配置
                    print_file = requests.get('http://XXX.XXX.XXX.XXX/static/Upload_Files/{}'.format(
                        All_order[one].File_Dir))  # 访问连接
                    if print_file.status_code != 200:  # 如果访问状态码不为零
                        print('No 200!')
                        raise IOError(
                            '{} {} {}'.format(print_file.status_code, print_file.reason,
                                              print_file.url))  # 自义定获取错误的信息
                    else:
                        with open('./static/go_print/' + All_order[one].File_Dir, 'wb') as f:
                            f.write(print_file.content)  # 下载文件

                    # 处理 报错
                except Exception as e:
                    print('no download!')
                    with open('./log/download_error_log', 'a') as f:
                        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + str(
                            All_order[one].Id) + ' ' + str(e) + '\n')
                else:
                    with open('./log/download_log', 'a') as f:
                        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + str(
                            All_order[one].Id) + ' sucessfully!' + '\n')
                    All_order[one].Print_Status = 2  # 做出标识，文件已下载成功
                finally:
                    Session1.commit()
                    print('>>>>>>>>>>>>>>><<<<<<<<<<<<<<<')
    else:
        pass


def Print():
    Session2 = DBSession()
    cmd = 'ls -t ./static/go_print > ./log/goprint_log'  # 将打印的文件名，转移至log文件中
    subprocess.call(cmd, shell=True)
    # 读取文件夹下的内容
    Goprint = open('./log/goprint_log', 'r+')
    for line in Goprint:
        print_order = Session2.query(Order).filter(Order.File_Dir == line[:-1]).first()  # 查询订单信息

        try:  # 开始打印
            print('----------------' + print_order.File_Dir + '----------------')
            # 打印订单的 信息

            # pdf(Session2.query(User).filter(User.Id == print_order.User_Id).first().Tel_Number,
            #     print_order.Trade_Number)
            # print_cmd1 = 'lp -o fitplot ./static/html/1.pdf'
            # go_mac = subprocess.call(print_cmd1, shell=True)
            # if go_mac != 0:
            #     error = subprocess.getoutput(print_cmd1)
            #     raise IOError(error)

            # 打印用户文件
            if print_order.Print_Direction == '4':
                if print_order.File_Dir[-3:] in ['pdf', 'jpg', 'png', 'peg', 'psd', 'pdd', 'pdf', 'svg']:
                    print('try to print >< 1 ><' + print_order.File_Dir[-3:])
                    # 打印份数      打印的方向     单双面                                        打印份数
                    print_cmd2 = 'lp -n {} -o fitplot -o landscape -o sides={} -o ColorModel={} ./static/go_print/{}'.format(
                        print_order.Print_Copies,
                        print_order.Print_way,
                        print_order.Print_Colour,
                        line[:-1])
                else:
                    print('try to print >< 2 ><' + print_order.File_Dir[-3:])
                    print_cmd2 = 'lp -n {} -o landscape -o sides={} -o ColorModel={} ./static/go_print/{}'.format(
                        print_order.Print_Copies,
                        print_order.Print_way,
                        print_order.Print_Colour,
                        line[:-1])
            else:
                if print_order.File_Dir[-3:] in ['pdf', 'jpg', 'png', 'peg', 'psd', 'pdd', 'pdf', 'svg']:
                    print('try to print >< 3 ><' + print_order.File_Dir[-3:])
                    print_cmd2 = 'lp -n {} -o fitplot -o sides={} -o ColorModel={}  ./static/go_print/{}'.format(
                        print_order.Print_Copies,
                        print_order.Print_way,
                        print_order.Print_Colour,
                        line[:-1])
                else:
                    print('try to print >< 4 ><' + print_order.File_Dir[-3:])
                    print_cmd2 = 'lp -n {} -o sides={} -o ColorModel={}  ./static/go_print/{}'.format(
                        print_order.Print_Copies,
                        print_order.Print_way,
                        print_order.Print_Colour,
                        line[:-1])
            go_lp = subprocess.call(print_cmd2, shell=True)
            print('>>>>>>>>>>>>>>>>>>>>>>one<<<<<<<<<<<<<<<<<<<<<<')
            if go_lp != 0:
                error = subprocess.getoutput(print_cmd2)
                raise IOError(error)
            print('----------------lp----------------')
        except Exception as e:
            print('----------------error----------------')
            with open('./log/print_error_log', 'a') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + line[:-1] + " " + str(e) + "\n")
        else:
            print('----------------ok----------------')
            # 将打印完成的文件删除
            subprocess.call('rm ./static/go_print/{}'.format(line[:-1]), shell=True)
            print_order.Print_Status = 3
            with open('./log/print_success_log', 'a') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + line[
                                                                                     :-1] + ' ' + 'Successfully!' + "\n")
        finally:
            Session2.commit()
            print('>>>>>>>>>>>>>>><<<<<<<<<<<<<<<')


while 1:
    Query()
    time.sleep(4)
    Print()
