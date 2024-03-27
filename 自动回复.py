"""
Author:Nxersty
"""
# !/usr/bin/python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from uiautomation import WindowControl
import time

wx = WindowControl(Name='微信', searchDepth=1)
wx.ListControl()
wx.SwitchToThisWindow()

hw = wx.ListControl(Name='会话')

df = pd.read_csv('回复数据.csv', encoding='utf-8')

running = True  # 设置主循环运行标志

while running:
    we = hw.TextControl(searchDepth=4)
    while not we.Exists():
        if not running:  # 检查退出标志
            break  # 如果退出标志为False，退出循环
        time.sleep(1)  # 在每次循环中添加适当的延时，以减少CPU占用

    if not running:  # 检查退出标志
        break  # 如果退出标志为False，退出循环

    if we.Name:
        we.Click(simulateMove=False)
        last_msg = wx.ListControl(Name='消息').GetChildren()[-1].Name
        msg = df.apply(lambda x: x['回复内容'] if x['关键词'] in last_msg else None, axis=1)
        print(msg)
        msg.dropna(axis=0, how='any', inplace=True)
        ar = np.array(msg).tolist()
        if ar:
            wx.SendKeys(ar[0].replace('{br}', '{Shift}{Enter}'), waitTime=1)
            wx.SendKeys('{Enter}', waitTime=1)
            wx.TextControl(SubName=ar[0][:5]).RightClick()
        else:
            wx.SendKeys('我不理解你什么意思', waitTime=1)
            wx.SendKeys('{Enter}', waitTime=1)
            wx.TextControl(SubName=last_msg[:5]).RightClick()

    time.sleep(1)  # 在主循环中添加适当的延时，以减少CPU占用
