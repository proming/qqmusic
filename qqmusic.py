#-*-coding:utf-8-*-
import os, json, requests, urllib, time, mutagen.id3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TPOS, TRCK
import random

def parseTopList(date, topid, songbegin = 0, songnum = 30):
    """
    解析QQ音乐榜单地址
    :param date: 榜单日期
    :param topid:
    :param songbegin:
    :param songnum:
    :return:
    """
    listurl = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3" \
              "&page=detail&date=%s&topid=%d&type=top&song_begin=%d&song_num=%d" \
              "&g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8" \
              "&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0" % (date, topid, songbegin, songnum)
    count = 0
    referer = 'https://y.qq.com/n/yqq/toplist/4.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0',
        'Cache-Control' : 'max-age=0, no-cache',
        'Host': 'y.qq.com',
        'Referer': referer,
        'Cookie' : 'tvfe_boss_uuid=98e6d0438f59d241; pgv_pvid=3498392328; pgv_pvi=728714240; RK=mJaoyjuQNu; ptcz=86b030b0ca4eabd39308eb0a4c6c589a89721d8e01bfc00d2e2e1d822a2d3612; ts_refer=music.qq.com/; ts_uid=3018036214; yq_index=1; yqq_stat=0; pgv_info=ssid=s9657074716; pgv_si=s5655964672; yplayer_open=0; player_exist=1; qqmusic_fromtag=66; yq_playschange=0; yq_playdata=; ts_last=y.qq.com/n/yqq/toplist/4.html'
    }
    response = requests.get(listurl, headers=headers)
    songlist = response.json()['songlist']
    for song in songlist:
        count = count + 1
        songmid = song['data']['songmid']
        songurl = "https://y.qq.com/n/yqq/song/%s.html" % songmid
        print('%d : %s' % (count, songurl))
        querySong(songmid)
        time.sleep(2)

def parseSinger(singermid, begin=0, num=20):
    count = 0
    singerurl = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?' \
                'g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8' \
                '&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0' \
                '&singermid=%s&order=listen' \
                '&begin=%d&num=%d&songstatus=1' % (singermid, begin, num)
    referer = 'https://y.qq.com/n/yqq/singer/%s.html' % singermid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0',
        'Cache-Control' : 'max-age=0, no-cache',
        'Host': 'y.qq.com',
        'Referer': referer,
        'Cookie' : 'tvfe_boss_uuid=98e6d0438f59d241; pgv_pvid=3498392328; pgv_pvi=728714240; RK=mJaoyjuQNu; ptcz=86b030b0ca4eabd39308eb0a4c6c589a89721d8e01bfc00d2e2e1d822a2d3612; ts_refer=music.qq.com/; ts_uid=3018036214; yq_index=1; yqq_stat=0; pgv_info=ssid=s9657074716; pgv_si=s5655964672; yplayer_open=0; player_exist=1; qqmusic_fromtag=66; yq_playschange=0; yq_playdata=; ts_last=y.qq.com/n/yqq/toplist/4.html'
    }
    response = requests.get(singerurl, headers=headers)
    songlist = response.json()['data']['list']
    for song in songlist:
        count = count + 1
        songmid = song['musicData']['songmid']
        songurl = "https://y.qq.com/n/yqq/song/%s.html" % songmid
        print('%d : %s' % (count, songurl))
        querySong(songmid)
        time.sleep(2)

def parseAlbumList(albummlist):
    for albummid in albummlist:
        parseAlbum(albummid)

def parseAlbum(albummid):
    global musicpath
    count = 0
    albumurl = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?' \
               'albummid=%s&g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8' \
               '&notice=0&platform=yqq&needNewCode=0' % albummid
    referer = 'https://y.qq.com/n/yqq/album/%s.html' % albummid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0',
        'Cache-Control' : 'max-age=0, no-cache',
        'Host': 'y.qq.com',
        'Referer': referer,
        'Cookie' : 'tvfe_boss_uuid=98e6d0438f59d241; pgv_pvid=3498392328; pgv_pvi=728714240; RK=mJaoyjuQNu; ptcz=86b030b0ca4eabd39308eb0a4c6c589a89721d8e01bfc00d2e2e1d822a2d3612; ts_refer=music.qq.com/; ts_uid=3018036214; yq_index=1; yqq_stat=0; pgv_info=ssid=s9657074716; pgv_si=s5655964672; yplayer_open=0; player_exist=1; qqmusic_fromtag=66; yq_playschange=0; yq_playdata=; ts_last=y.qq.com/n/yqq/toplist/4.html'
    }
    response = requests.get(albumurl, headers=headers)
    songlist = response.json()['data']['list']
    albumdate = response.json()['data']['aDate'][0:4]
    albumname = response.json()['data']['name']
    musicpath = '%s/%s %s' % (basepath, albumdate, albumname)
    if not os.path.exists(musicpath):
        os.mkdir(musicpath)

    dicsnum = findMaxCdidx(songlist)
    for song in songlist:
        count = count + 1
        songmid = song['songmid']
        belongcd = '%02d' % song['belongCD']
        cdidx = song['cdIdx'] + 1
        songurl = "https://y.qq.com/n/yqq/song/%s.html" % songmid
        print('%d : %s' % (count, songurl))
        querySong(songmid, True, albumdate, belongcd, cdidx, dicsnum)
        time.sleep(2)

    # write album description
    albumdesc = response.json()['data']['desc']
    descpath = "%s/%s - 简介.txt" % (musicpath, albumname)
    with open(descpath, "w+", encoding="utf-8") as f:
        f.writelines(albumdesc)
        f.close()

def findMaxCdidx(songlist):
    maxcdidx = 1
    for song in songlist:
        cdidx = song['cdIdx'] + 1
        if cdidx > maxcdidx:
            maxcdidx = cdidx

    return maxcdidx

def parsePlayList(disstid):
    count = 0
    listurl = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0' \
              '&disstid=%s&g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8' \
              '&notice=0&platform=yqq&needNewCode=0' % disstid
    referer = 'https://y.qq.com/n/yqq/playlist/%s.html' % disstid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0',
        'Cache-Control' : 'max-age=0, no-cache',
        'Host': 'y.qq.com',
        'Referer': referer,
        'Cookie' : 'tvfe_boss_uuid=98e6d0438f59d241; pgv_pvid=3498392328; pgv_pvi=728714240; RK=mJaoyjuQNu; ptcz=86b030b0ca4eabd39308eb0a4c6c589a89721d8e01bfc00d2e2e1d822a2d3612; ts_refer=music.qq.com/; ts_uid=3018036214; yq_index=1; yqq_stat=0; pgv_info=ssid=s9657074716; pgv_si=s5655964672; yplayer_open=0; player_exist=1; qqmusic_fromtag=66; yq_playschange=0; yq_playdata=; ts_last=y.qq.com/n/yqq/toplist/4.html'
    }
    response = requests.get(listurl, headers=headers)
    songlist = json.loads(response.text[13:-1])['cdlist'][0]['songlist']
    for song in songlist:
        count = count + 1
        songmid = song['songmid']
        songurl = "https://y.qq.com/n/yqq/song/%s.html" % songmid
        print('%d : %s' % (count, songurl))
        querySong(songmid)
        time.sleep(2)

def moreSound(songmid, songname):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0',
        'Cache-Control': 'max-age=0, no-cache',
        'Host': 'moresound.tk',
        'Cookie': 'sign=BmXrZ2BrZ%s%s; ddos=1; XLA_CI=ae611fa29193d2e627e93ad9ba70981a' % (getRandomChar(6),'%3D%3D')
    }
    queryurl = 'http://moresound.tk/music/api.php?search=qq'
    try:
        params = {
            'mid':'%s/0' % songmid
        }
        response = requests.post('http://moresound.tk/music/api.php?get_song=qq', data = params, headers=headers)
        songurl = response.json()['url']['320MP3']

        response = requests.get('http://moresound.tk/music/%s' % songurl, headers=headers)
        songurl = response.json()['url']
        return songurl

    except (Exception):
        print("MoreSound: No 320MP3 %s(%s)" % (songname, songmid))
        return ''

char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z']

def getRandomChar(num):
    return "".join(random.sample(char, num))

def querySong(songmid, isalbum=False, albumdate='', belongcd='', cdidx=1, dicsnum=1):
    songurl = "https://y.qq.com/n/yqq/song/%s.html" % songmid
    response = requests.get("http://www.douqq.com/qqmusic/qqapi.php", params={'mid':songurl})
    filelist = json.loads(response.json())
    mp3_h = filelist['mp3_h']
    songname = filelist['songname']
    singername = filelist['singername']
    albumname = filelist['albumname']

    mp3_h = moreSound(songmid, songname)

    #mp3_h = mp3_h.replace('dl.stream.qqmusic.qq.com', 'streamoc.music.tc.qq.com')
    #mp3_h = mp3_h.replace('https', 'http')

    if singername.count('/') > 4:
        singername = '群星'
    singername = singername.replace('/', ',')

    if mp3_h == '':
        print("No 320mp3 File: %s - %s.mp3" % (singername, songname))
        return

    songpath = "%s/%s - %s.mp3"%(musicpath, singername, songname)
    if os.path.exists(songpath) :
        print("File Exists: %s - %s.mp3" % (singername, songname))
        return

    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0'),
                             ('Cache-Control', 'max-age=0, no-cache'),
                             ('Host', 'y.qq.com'),
                             ('Referer', songurl),
                             ('Cookie', 'tvfe_boss_uuid=98e6d0438f59d241; pgv_pvid=3498392328; pgv_pvi=728714240; RK=mJaoyjuQNu; ptcz=86b030b0ca4eabd39308eb0a4c6c589a89721d8e01bfc00d2e2e1d822a2d3612; ts_refer=music.qq.com/; ts_uid=3018036214; yq_index=1; yqq_stat=0; pgv_info=ssid=s9657074716; pgv_si=s5655964672; yplayer_open=0; player_exist=1; qqmusic_fromtag=66; yq_playschange=0; yq_playdata=; ts_last=y.qq.com/n/yqq/toplist/4.html')
                             ]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(mp3_h, songpath)
    except (urllib.error.HTTPError, urllib.error.ContentTooShortError):
        print("Download 320mp3 Error: %s - %s.mp3, try 128mp3..." % (singername, songname))
        try:
            mp3_l = filelist['mp3_l']
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0'),
                                 ('Cache-Control', 'max-age=0, no-cache'),
                                 ('Host', 'y.qq.com'),
                                 ('Referer', songurl),
                                 ('Cookie',
                                  'tvfe_boss_uuid=98e6d0438f59d241; pgv_pvid=3498392328; pgv_pvi=728714240; RK=mJaoyjuQNu; ptcz=86b030b0ca4eabd39308eb0a4c6c589a89721d8e01bfc00d2e2e1d822a2d3612; ts_refer=music.qq.com/; ts_uid=3018036214; yq_index=1; yqq_stat=0; pgv_info=ssid=s9657074716; pgv_si=s5655964672; yplayer_open=0; player_exist=1; qqmusic_fromtag=66; yq_playschange=0; yq_playdata=; ts_last=y.qq.com/n/yqq/toplist/4.html')
                                 ]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(mp3_l, songpath)
        except (urllib.error.HTTPError, urllib.error.ContentTooShortError):
            print("Download 128mp3 Error: %s - %s.mp3" % (singername, songname))
            return

    pic = filelist['pic']
    modifyTags(songpath, pic, singername, songname, albumname, isalbum, albumdate, belongcd, cdidx, dicsnum)

    # download the album picture
    coverpath = "%s/%s - cover.jpg" % (musicpath, albumname)
    if isalbum and not os.path.exists(coverpath) :
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0'),
                             ('Cache-Control', 'max-age=0, no-cache'),
                             ('Host', 'y.qq.com'),
                             ('Referer', songurl),
                             ('Cookie',
                              'tvfe_boss_uuid=98e6d0438f59d241; pgv_pvid=3498392328; pgv_pvi=728714240; RK=mJaoyjuQNu; ptcz=86b030b0ca4eabd39308eb0a4c6c589a89721d8e01bfc00d2e2e1d822a2d3612; ts_refer=music.qq.com/; ts_uid=3018036214; yq_index=1; yqq_stat=0; pgv_info=ssid=s9657074716; pgv_si=s5655964672; yplayer_open=0; player_exist=1; qqmusic_fromtag=66; yq_playschange=0; yq_playdata=; ts_last=y.qq.com/n/yqq/toplist/4.html')
                             ]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(pic, coverpath)


def modifyTags(songpath, pic, singername, songname, albumname, isalbum=False, albumdate='', belongcd='', cdidx=1, dicsnum=1):
    coverpath = "%s/%s - cover.jpg" % (musicpath, albumname)
    img = None
    if isalbum and os.path.exists(coverpath):
        img = open(coverpath, "rb")
    else:
        request = urllib.request.Request(pic)
        request.add_header('User-agent', 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/63.0')
        request.add_header('Cache-Control', 'max-age=0, no-cache')
        request.add_header('Host', 'y.qq.com')
        request.add_header('Referer', 'https://y.qq.com/n/yqq/toplist/4.html')
        img = urllib.request.urlopen(request)

    meta = None
    try:
        meta = mutagen.File(songpath)
    except (FileNotFoundError, mutagen.MutagenError):
        print('mutagen.MutagenError: ''%s'''% songpath)
        return

    try:
        meta.add_tags()
    except mutagen.MutagenError:
        None

    meta['TIT2'] = TIT2(  # 插入歌名
       encoding=1,
       text=[songname]
    )
    meta['TPE1'] = TPE1(  # 插入第一演奏家、歌手、等
       encoding=1,
       text=[singername]
    )
    meta['TALB'] = TALB(  # 插入专辑
       encoding=1,
       text=[albumname]
    )
    meta['APIC'] = APIC(  # 插入图片
        encoding=1,
        mime='image/jpeg',
        type=3,
        desc=u'Cover',
        data=img.read()
    )

    # write addition mp3 tag
    if isalbum :
        meta['TDRC'] = TDRC(  # 插入专辑年份
            encoding=1,
            text=[albumdate]
        )
        meta['TRCK'] = TRCK(  # 插入曲目编号
            encoding=1,
            text=[belongcd]
        )
        if dicsnum != 1:
            meta['TPOS'] = TPOS(  # 碟片编号
                encoding=1,
                text=['%02d/%d'% (cdidx, dicsnum)]
            )
    meta.save()

if __name__ == '__main__':
    basepath = "/Users/xxx/Downloads/Music"
    musicpath = basepath

    #https://y.qq.com/n/yqq/toplist/26.html#t1=2019&t2=17&t3=song&t4=0&t5=1
    date = '2019_17'
    topid = 26
    songbegin = 0
    songnum = 200
    #parseTopList(date, topid, songbegin, songnum)

    #songurl="https://y.qq.com/n/yqq/song/004377vA0rh3h3.html"
    songmid='001IltNp2K0tGr'
    #querySong(songmid)

    #songpath = '张信哲 - 不要对他说.mp3'
    songpath = '/Users/fulongming/Downloads/Music/王琪 - 站着等你三千年.mp3'
    pic = 'https://y.gtimg.cn/music/photo_new/T002R300x300M000004CqsM73IMs7y.jpg?max_age=2592000'
    singername = '王琪'
    songname = '站着等你三千年'
    albumname = '站着等你三千年'
    #modifyTags(songpath, pic, singername, songname, albumname)

    #https://y.qq.com/n/yqq/singer/004V53Ga0bV65j.html
    singermid = '003ArN8Z0WpjTz'
    #parseSinger(singermid)

    #https://y.qq.com/n/yqq/playsquare/6938020960.html
    disstid = '4264151345'
    #parsePlayList(disstid)

    #https://y.qq.com/n/yqq/album/004JoMGA19g7aV.html
    albummid = '003xIVLL0yHX94'
    #parseAlbum(albummid)

    albummlist=[
        '004aYDgO0un78W',
        '0003hrx91JovyH',
        '000Wsu871b8zVy'
    ]
    #parseAlbumList(albummlist)