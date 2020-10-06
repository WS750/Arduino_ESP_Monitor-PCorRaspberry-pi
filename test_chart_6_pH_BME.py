"""
参考URL：https://toptechboy.com/python-with-arduino-lesson-11-plotting-and-graphing-live-data-from-arduino-with-matplotlib/
ESP32, 中華パチモンUNOで動作確認
マイコンから受け取ったデータ4種をグラフ化
4つのサブプロットで描画
"""
import serial 
import numpy
import matplotlib.pyplot as plt 
from drawnow import * #リアルタイムプロットのライブラリ
import os
import datetime

data_A= []
data_B=[]
data_C= []
data_D=[]

#マイコン，PCの設定を反映
Cerial_Port='COM4'#シリアルポート　ラズパイの場合（"/dev/ttyUSB0"）ターミナルで”dmesg”コマンドからマイコンの接続先がわかる
baudrate=9600#ボーレート

#データを保存するファイル名
file_name= 'data.txt'

micro_data = serial.Serial(Cerial_Port, baudrate)#シリアル通信の設定
plt.ion() #matplotlibをインタラクティブモードに
cnt=0

#カレントディレクトリの確認
print(os.getcwd())

#グラフの設定
def makeFig():
    plt.suptitle('Streaming Data')
    plt.style.use('bmh') #全体のスタイル
    plt.tight_layout()
    
    plt.subplot(221)
    plt.grid(True)
    
    
    plt.ylabel('A, -')
    plt.plot(data_A, 'mediumvioletred', label='A')
    #plt.ylim(xx,xx)
    plt.legend(loc='upper left')
    
    plt.subplot(222)
    plt.ylabel('B, -')
    plt.plot(data_B, 'deepskyblue', label='B')
    #plt.ylim(xx,xx)
    plt.ticklabel_format(useOffset=False) 
    plt.legend(loc='upper left')
    
    plt.subplot(223)    
    plt.ylabel('C, -')
    plt.plot(data_C, 'goldenrod', label='C')
    #plt.ylim(xx,xx)
    plt.legend(loc='upper left')
    
    plt.subplot(224)
    plt.ylabel('D, -')
    plt.plot(data_D, 'springgreen', label='D')
    #plt.ylim(xx,xx)
    plt.ticklabel_format(useOffset=False) 
    plt.legend(loc='upper left')

#ファイルの有無確認
try:
    #ファイルが存在しない場合 mode=x:新規作成専用引数
    with open(file_name, mode='x') as f:
        print("Make_newfile")
        pass
#ファイルが存在する場合
except FileExistsError:
    print("Add_file")

try: 
    while True:
        while (micro_data.inWaiting()==0):
            pass #do nothing

        #decodeで行先頭のbを消去（バイト型を文字列型に変換する。逆はencode）    
        arduinoString = micro_data.readline().decode('utf-8')  
        print(arduinoString )
    
        #ファイルが存在する場合，mode=aで追記
        with open(file_name, mode='a') as f:
            #先頭に日付を加えてデータをテキストファイルに保存
            f.write(str(datetime.datetime.now())+','+arduinoString)
        #マイコンからのデータを’，’で分割（＝マイコンが送信するデータはCSVである必要）
        dataArray = arduinoString.split(',') 
        slave_data_A = float( dataArray[0])
        slave_data_B = float( dataArray[1])
        slave_data_C = float( dataArray[2])
        slave_data_D = float( dataArray[3])
        
        data_A.append(slave_data_A)
        data_B.append(slave_data_B) 
        data_C.append(slave_data_C)
        data_D.append(slave_data_D)
        
        drawnow(makeFig)   #グラフ描画の関数呼び出し
        plt.pause(0.00001) #描画間隔
        cnt=cnt+1
        plt.cla() 
        if(cnt>300):       #何点のデータをグラフ上に保持するか
            data_A.pop(0)                       
            data_B.pop(0)
            data_C.pop(0)                       
            data_D.pop(0)

#コンソール上でCTRL＋C長押しで処理中止
except KeyboardInterrupt:
    micro_data.close()
    sys.exit() 