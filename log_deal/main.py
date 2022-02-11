# coding:utf-8

# 找到日志中的top 10，日志格式如下
# txt = '''100.116.167.9 - - [22/Oct/2017:03:55:53 +0800] "HEAD /check HTTP/1.0" 200 0 "-" "-" "-" ut = 0.001'''

# nodes = txt.split()
# print 'ip:%s, url:%s, code:%s' % (nodes[0],nodes[6],nodes[8])

# 统计ip,url,code的次数，并且生成字典
def log_analysis(log_file, top_num=10):
    path = log_file
    shandle = open(path, 'r')
    count = 1

    log_dict = {}

    while True:
        line = shandle.readline()
        if line == '':
            break
        nodes = line.split()

        # {(ip,url,code):count}当做字典的key
        # print 'ip:%s, url:%s, code:%s' % (nodes[0],nodes[6],nodes[8])

        # 拼凑字典，如果不存在赋值为1，如果存在则+1

        ip,a_time,a_method, url, code = nodes[0],nodes[3].replace('[',''), nodes[5],nodes[6], nodes[8]
        if (ip, url, code) not in log_dict:
            log_dict[(ip, url, code)] = 1
        else:
            log_dict[(ip, url, code)] = log_dict[(ip, url, code)] + 1
    # 关闭文件句柄
    shandle.close()
    # 对字典进行排序
    # print log_dict
    # ('111.37.21.148', '/index', '200'): 2
    rst_list = log_dict.items()
    for j in range(10):
        # 冒泡法根据rst_list中的count排序，找出访问量最大的10个IP
        for i in range(0, len(rst_list) - 1):
            if rst_list[i][1] > rst_list[i + 1][1]:
                temp = rst_list[i]
                rst_list[i] = rst_list[i + 1]
                rst_list[i + 1] = temp

    need_list = rst_list[-1:-top_num - 1:-1]
    # 打印出top 10访问日志
    print(need_list)


# 函数入口
if __name__ == '__main__':
    # nginx日志文件
    log_file = 'choumaomi.access.log'
    # top_num 表示去top多少个
    top_num = 10
    log_analysis(log_file, top_num)
