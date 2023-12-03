import urllib.request
import urllib.error
import json
import datetime
import os
import time

# Market options: en-US, zh-CN, ja-JP, en-AU, en-UK, de-DE, en-NZ
market = 'en-US'
resolution = '1920x1080'
image_directory = '/tmp/'
wallpaper_name = 'image.jpg'

loop_value = 1
while loop_value == 1:
    try:
        urllib.request.urlopen("http://google.com")
    except urllib.error.URLError as e:
        time.sleep(10)
    else:
        loop_value = 0

        response = urllib.request.urlopen("http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=" + market)

        obj = json.load(response)
        url = 'http://www.bing.com' + obj['images'][0]['urlbase'] + '_' + resolution + '.jpg'

        if not os.path.exists(image_directory):
            os.makedirs(image_directory)
        path = os.path.join(image_directory, wallpaper_name)

        if os.path.exists(path):
            today_date = datetime.datetime.now().strftime("%m/%d/%Y")
            file_date = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(path)))
            if today_date == file_date:
                print("You already have today's Bing image")
            else:
                print(f"Downloading Bing wallpaper to {path}")
                with open(path, 'wb') as f:
                    bingpic = urllib.request.urlopen(url)
                    f.write(bingpic.read())
        else:
            print(f"Downloading Bing wallpaper to {path}")
            with open(path, 'wb') as f:
                bingpic = urllib.request.urlopen(url)
                f.write(bingpic.read())
