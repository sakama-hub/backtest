import pandas as pd
import numpy as np
import glob
import chart_studio.plotly as py
import plotly.graph_objs as go
import datetime
import plotly.offline as offline

from framework.settlement import settlement
from trade_algorithm.trade_algorithm import trade_algolithm

fund = 100000 #初期口座資金（適宜変更）
sis = 200000 #システムストップ口座資金の定義（適宜変更）

df = pd.read_csv('backtest_data/○○') #検証データの読み込み

#損切のが逆指値更新関数が指定されているかどうか
if len(glob.glob("stoploss_update/**.py")) == 2:
    from stoploss_update.stoploss_update import stoploss_update

else:
    stoploss_update = None

if len(len(glob.glob("profitable_update/**.py")) == 2):
    from profitable_update.profitable_update import profitable_update

else:
    profitable_update = None


test = settlement('○○',trade_algolithm,stoploss_update=stoploss_update,profitable_update = profitable_update,spread=0.8) #○○は検証する通貨ペア名

settlement.formattimg(fund,sis)

df_len = len(df)
for i in range(df_len):
    test.rate_update(df.iloc[:1+i,1:]) #レートの更新

    #ポジションを持っているとき
    if  test.trade_judge() == 'yes':

        #ポジションを決済するとき
        if test.settle_distinction() == 'yes':

            test.data_update4()


        #ポジションを決済しないとき
        else:

            test.data_update3()


    #ポジションを持っていなとき
    else:

        order = test.setup()#注文内容を確定

        #トレードを注文するとき
        if order[0] == 'yes':

            test.data_update2(order[1])



        #トレードを注文しないとき
        else:

            test.data_update1()


date = df.iloc[:,1].values
trace0 = go.Scatter(x = date, y = settlement._settlement__fund_stream, mode = 'lines', name = 'X')
layout = go.Layout(xaxis = dict(title = 'date', type='date', dtick = 'D1'),  # dtick: 'M1'で１ヶ月ごとにラベル表示
              yaxis = dict(title = 'value'))
fig = dict(data =trace0, layout = layout)
offline.plot(fig, filename='result/funds_transition.html', image_filename='test', image='jpeg')

test.trade_record().to_csv('result/trade_record.csv',encoding='utf_8_sig')
test.trade_overview().to_csv('result/trade_overview.csv',encoding='utf_8_sig')
