# -*- coding: utf-8 -*-
# author: cgcel

import datetime

import requests
import win32api
import win32con
import win32gui
from bs4 import BeautifulSoup as bs

save_path = "E:/picture/BingWP/"

base_url = "https://www.bing.com"
main_url = "https://www.bing.com/?mkt=zh-CN"


def dateFormat(data):
    if len(data) == 1:
        return '0' + data
    else:
        return data


class BingWP(object):

    def __init__(self):
        self.get_img_url()
        self.save_img()
        self.set_WP(self.file_name)

    def get_img_url(self):
        r = requests.get(main_url)
        soup = bs(r.content, "html.parser")
        result = soup.head.link['href']
        self.url_img = base_url + result
        # print(self.url_img)

    def save_img(self):
        r = requests.get(self.url_img)
        time = datetime.datetime.now()
        self.file_name = save_path + \
            str(time.year) + dateFormat(str(time.month)) + \
            dateFormat(str(time.day)) + ".jpg"
        f = open(self.file_name, "wb")
        f.write(r.content)
        f.close()
        # set_WP(file_name)

    def set_WP(self, imagepath):
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                  "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0,
                               win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER, imagepath, 1+2)


if __name__ == "__main__":
    BingWP()
