import urllib2
import json
import datetime
import os.path, time
from os.path import expanduser
 
#market options: en-US, zh-CN, ja-JP, en-AU, en-UK, de-DE, en-NZ
market = 'en-US'
resolution = '1920x1080'
BingDirectory= 'output/'
WallpaperName = 'bing.jpg'
 
loop_value = 1
while (loop_value == 1):
    try:
        urllib2.urlopen("http://google.com")
    except urllib2.URLError, e:
        time.sleep( 10 )
    else:
        loop_value = 0
 
        response = urllib2.urlopen("http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=" + market)
        obj = json.load(response)
        url = (obj['images'][0]['urlbase'])
        url = 'http://www.bing.com' + url + '_' + resolution + '.jpg'
 
        if not os.path.exists(BingDirectory): 
            os.makedirs(BingDirectory)
        path = BingDirectory + WallpaperName
 
        if os.path.exists(path):
            todayDate = datetime.datetime.now().strftime("%m/%d/%Y")
            fileDate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(path)))
            if todayDate == fileDate:
                print "You already have today's Bing image"
            else:
                print ("Downloading Bing wallpaper to %s" % (path))
                f = open(path, 'w')
                bingpic = urllib2.urlopen(url)
                f.write(bingpic.read())
        else:
            print ("Downloading Bing wallpaper to %s" % (path))
            f = open(path, 'w')
            bingpic = urllib2.urlopen(url)
            f.write(bingpic.read())
