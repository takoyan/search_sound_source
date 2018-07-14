#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import threading
import numpy as np
import threading
import pyaudio
import threading
import socket
import re
#from challe10.py import julius

import matplotlib.pyplot as plt


def search(CHANNELS):
    chunk = 8192
    FORMAT = pyaudio.paInt16
    #サンプリングレート、マイク性能に依存
    RATE = 16000
    RECORD_SECONDS = 1
    #pyaudio
    audio = pyaudio.PyAudio()
    #plot time
    plottime = 100
    loopcounter = 0
    data_rms = []

    while True:

        #マイクからデータ取得#機器の設定
        stream = audio.open(  format = FORMAT,
                                    channels = CHANNELS,
                                    rate = RATE,
                                    input = True,
                                    input_device_index=0,
                                    frames_per_buffer = chunk)
"""
open関数によって機器への録音が始まる.
使用する際に注意することは,引数channelsに使用したいマイクのチャンネル番号,引数input_device_indexに使用したいマイクの
番号を代入する.それぞれの値に関しては,PyAudioクラス内のget_device_info_by_index関数に適当なindex値を入力し,
表示されたパラメータの名前を見て確認してほしい.(たまご型マイクなら,TAMAGO-03, index': 0, maxInputChannels': 8L,
のように表示されるはず.)
"""


        all = []
        for i in range(0, RATE / chunk * RECORD_SECONDS):
            data = stream.read(chunk)#read():マイクが取得するデータを読み込み(read)ながらdataに収納
            all.append(data)#上のdataを配列allに収納していく.

        data = ''.join(all)#allをキレイにしてdataに詰め直す
        data=np.frombuffer(data, dtype="int16")#上のdataはそのままでは型がおかしいのでint16型に変換

        #converting numpy-type-array
        np_data=np.array(data, dtype = np.float64)#上のdataをfloat64型に変換

        #downsampling#ダウンサンプリングなるものをする(何かは知らん)
        overhang = len(np_data) % 100
        down_data=np_data[:-overhang]
        down_data=np.reshape(down_data, (len(down_data)/100,100))
        down_data=np.average(down_data, 1)

        #RMS calculation#音量(出力量)に変換
        rms=np.sqrt(np.mean(np.square(down_data)))
        print "ch:" + str(ch)+ ": "+ str(rms)
        audio.close(stream)
        """
        ここで注意したいことが,1chを使用後にclose関数で録音を切らないまま,さらにopen関数を使用しようとすると
        エラーが出てしまうので,必ずclose関数で録音を停止した後に次のチャンネル等の録音を開始してほしい.
        """
        return rms


        data_rms.append(rms)

        stream.close()
        loopcounter = loopcounter + 1
        if loopcounter == plottime : break

"""
        plt.subplot(2,1,1)
        plt.plot(data_rms)
        plt.subplot(2,1,2)
        plt.plot(down_data)
        plt.show()
"""

if __name__ == '__main__':
    count=0
    data1=[0]
    data2=[0]
    data3=[0]
    data4=[0]
    data6=[0]
    data7=[0]
    data8=[0]
    data9=[0]
    while(count<=5):

        data1.append(search(1))#0
        data2.append(search(2))#45
        data3.append(search(3))#90
        data4.append(search(4))#135
        data6.append(search(5))#180
        data7.append(search(6))#225
        data8.append(search(7))#280
        data9.append(search(8))#325

        count+=count+1

    data=[np.average(data1),
    np.average(data2), np.average(data3), np.average(data4),
    np.average(data6), np.average(data7), np.average(data8), np.average(data9)]
    if(np.argmax(data)==0):
        print str(0)+"度"
    elif(np.argmax(data)==1):
        print str(45)+"度"
    elif(np.argmax(data)==2):
        print str(90)+"度"
    elif(np.argmax(data)==3):
        print str(135)+"度"
    elif(np.argmax(data)==4):
        print str(180)+"度"
    elif(np.argmax(data)==5):
        print str(225)+"度"
    elif(np.argmax(data)==6):
        print str(280)+"度"
    elif(np.argmax(data)==7):
        print str(325)+"度"
