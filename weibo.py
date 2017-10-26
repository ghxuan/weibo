import xlrd
import xlwt
import random
import requests
from UA import UA
from IP import thre
from time import time
from time import sleep
from json import loads
from xlutils.copy import copy


def post_user(data, password):
    # 模拟登录，获取账号id和关注数及cookies,并写入自己信息
    url = 'https://passport.weibo.cn/sso/login'
    referer = 'https://passport.weibo.cn/signin/login?entry=mweibo'
    hea['Referer'] = referer
    FROM_DATA = {
        'username': data,
        'password': password}
    resp = requests.post(url, headers=hea, data=FROM_DATA, allow_redirects=False)
    resp = loads(resp.text)
    uid = resp['data']['uid']
    url1 = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000012&lfid=100505{}_-_FOLLOWERS&featurecode=20000320&type=uid&value={}&containerid=100505{}'.format(uid, uid, uid, uid)
    htm = requests.get(url1, headers=hea)
    htm = loads(htm.text)
    htm = htm['userInfo']
    frc = htm['follow_count']
    # 关注数
    fsc = htm['followers_count']
    # 粉丝数
    ssc = htm['statuses_count']
    # 微博数
    name = htm['screen_name']
    # 姓名
    uid = int(uid)
    # 号
    q = [uid, name, ssc, fsc, frc, 0]
    p = [['id号', '姓名', '微博数', '粉丝数', '关注数', '是否已下载其关注者']]
    p.append(q)
    yield p


def get_info(hea, I, id, frc):
    # 得到全部被自己关注的人的信息
    hea['Referer'] = 'https://m.weibo.cn/p/second?containerid=100505{}_-_FOLLOWERS'.format(id)
    n = int(frc // 10)
    print(n)
    p = []
    for w in range(n+1):
        url = 'https://m.weibo.cn/api/container/getSecond?containerid=100505{}_-_FOLLOWERS'.format(id)+'&page='+str(w+1)
        print(url)
        html = requests.get(url, headers=hea, proxies=I).text
        html = loads(html)
        try:
            html = html['cards']
        except Exception as e:
            print(e)
            continue
        x = len(html)
        for i in range(x):
            sleep(0.2)
            fid = html[i]['user']['id']
            url1 = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000012&lfid=100505{}_-_FOLLOWERS&featurecode=20000320&type=uid&value={}&containerid=100505{}'.format(fid, id, fid, fid)
            htm = requests.get(url1, headers=hea, proxies=I).text
            htm = loads(htm)
            htm = htm['userInfo']
            frc = htm['follow_count']
            # 关注数
            fsc = htm['followers_count']
            # 粉丝数
            ssc = htm['statuses_count']
            # 微博数
            name = htm['screen_name']
            # 姓名
            fid = int(fid)
            # 号
            p.append([fid, name, ssc, fsc, frc, 0])
            print(name)
            # '0'是指其关注的账号未获取
    yield p


def loop(UA , IP):
    # 运行一次，则循环下载数据一次
    data = xlrd.open_workbook('weibo.xls')
    table = data.sheet_by_name('sheet 1')
    uid = table.col_values(0)
    frc = table.col_values(4)
    yon = table.col_values(5)
    b = len(uid)
    w = copy(data)
    wg = w.get_sheet(0)
    for i in range(b - 1):
        data = xlrd.open_workbook('weibo.xls')
        table = data.sheet_by_name('sheet 1')
        u = table.col_values(0)
        if yon[i + 1] == 0:
            U = random.choice(UA)
            hea['User-Agent'] = U
            I = random.choice(IP)
            a = get_info(hea, I, int(uid[i + 1]), frc[i+1])
            wg.write(i+1, 5, 1)
            p = next(a)
            c = len(p)
            b = len(u)
            for j in range(c):
                for k in range(6):
                    wg.write(b + j, k, p[j][k])
            w.save('weibo.xls')


def the_first():
    # 找到自己的信息并保存
    data = ''
    # data为账号
    password = ''
    # password为密码
    a = post_user(data, password)
    p = next(a)
    wk = xlwt.Workbook(encoding='utf-8')
    bst = wk.add_sheet('sheet 1', cell_overwrite_ok=True)
    for i in range(len(p)):
        for j in range(6):
            bst.write(i, j, p[i][j])
    wk.save('weibo.xls')


if __name__ == '__main__':
    start = time()
    IP = thre()
    print(IP)
    UA = UA
    hea = {
    'Referer': '',
    'User-Agent': UA[0], }
    the_first()
    # the_first()第一次运行不需要注释，第二次及以后运行都要注释，否则之前保存的文件就不存在了
    n = 2
    for i in range(n):
        loop(UA, IP)
    stop = time()
    print(stop-start)
