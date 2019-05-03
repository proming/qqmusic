# Download music from qqmusic

## 简介
感谢[douqq.com](http://www.douqq.com)、[MoreSound](http://moresound.tk)提供的QQ音乐无损接口api，实现从[QQ音乐](https://y.qq.com/)中下载高品质的音乐。
目前已实现功能：
- 按歌手下载音乐
- 按专辑(单张、多张)下载音乐
- 按榜单下载音乐
- 按歌单下载音乐

## 依赖
python版本为`3.6`
```
$ pip install requests mutagen
```

## 使用
运行程序前需要修改`qqmusic.py`中`basepath`，设置音乐下载路径。修改程序下载功能选项，找到对应功能，将方法前的注释去掉，如`#querySong(songmid)`，另外建议将已启用的功能注释。
1. 榜单歌曲下载，功能方法名称`parseTopList`
  ```
    #https://y.qq.com/n/yqq/  toplist/26.html#t1=2019&t2=17&t3=song&t4=0&t5=1
    date = '2019_17'
    topid = 26
    songbegin = 0
    songnum = 200
    #parseTopList(date, topid, songbegin, songnum)
  ```
2. 单曲下载，功能方法名称`querySong`
  ```
    #songurl="https://y.qq.com/n/yqq/song/004377vA0rh3h3.html"
    songmid='001IltNp2K0tGr'
    #querySong(songmid)
  ```
3. 歌手热歌下载，功能方法名称`parseSinger`
  ```
    #https://y.qq.com/n/yqq/singer/004V53Ga0bV65j.html
    singermid = '003ArN8Z0WpjTz'
    #parseSinger(singermid)
  ```
4. 单张专辑下载，功能方法名称`parseAlbum`
  ```
    #https://y.qq.com/n/yqq/album/004JoMGA19g7aV.html
    albummid = '003xIVLL0yHX94'
    #parseAlbum(albummid)
  ```
5. 多张专辑下载，功能方法名称`parseAlbumList`
  ```
    albummlist=[
        '004aYDgO0un78W',
        '0003hrx91JovyH',
        '000Wsu871b8zVy'
    ]
    #parseAlbumList(albummlist)	
  ```
6. 歌单下载，功能方法名称`parsePlayList`
  ```
    #https://y.qq.com/n/yqq/playsquare/6938020960.html
    disstid = '4264151345'
    #parsePlayList(disstid)
  ```

## 声明
本程序只是个人研究学习python所编写，所下载音乐文件请勿发布传播并在24小时内删除。