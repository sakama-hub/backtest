import numpy as np

def setup(df):



    order = [] #最終的に出力するリスト　　　

    df_ = df.values
    #過去のデータ数がシグナルを出すのに足るかどうか
    if len(df_)>1200:
        max_20h = np.amax(df_[-1-1200:-1,2])# 過去二十時間の最大値
        min_20h = np.amin(df_[-1-1200:-1,3])# 過去二十時間の最小値

        #過去20時間の最大値を超えるかどうか
        if df_[-1,2]>=max_20h:

            #longで注文
            order.append("yes")

            #入力データフレームからATRを求める一時間足を20時間分求める
            lis = []#一時間足のデータを格納するリスト
            for i in range(20):
                lis_ = []
                rousoku_1h = df_[-1-60*(20-i):-1-60*(20-i)+60]
                lis_.append(rousoku_1h[0,1])
                lis_.append(np.amax(rousoku_1h[:,2]))
                lis_.append(np.amin(rousoku_1h[:,3]))
                lis_.append(rousoku_1h[-1,4])

                lis.append(lis_)
            lis = np.array(lis,dtype='float64') #一時間足のリストをnumpy配列に変換する
            #一時間足からATRを求める
            lis_atr = []
            for i in range(20):
                lis_atr_ = []
                if i == 0:#前日の値はないので無視する
                    lis_atr.append(lis[i][1]-lis[i][2])#当日の高値-当日の安値
                else:
                    lis_atr_.append(lis[i][1]-lis[i][2])#当日の高値-当日の安値
                    lis_atr_.append(abs(lis[i][1]-lis[i-1][3]))#当日の高値-前日の終値
                    lis_atr_.append(abs(lis[i][2]-lis[i-1][3]))#当日の安値-前日の終値

                    lis_atr.append(np.amax(np.array(lis_atr_)))

            atr = np.mean(lis_atr)#ATR値

            #直近10時間の最安値を求める
            min_10h = np.amin(lis[-10:,2])




            order_ = {}
            order_['position_time'] = df_[-1,0]
            order_['position_type'] = 'long'
            order_['position'] = df_[-1,4]
            order_['position_size'] = 10000
            order_['stoploss_rate'] = min_10h
            order_['profitable_rate'] = df_[-1,4]+0.5

            order.append(order_)

        #過去20時間の最小値を下回るかどうか
        elif df_[-1,3] <= min_20h:

            #shortで注文
            order.append("yes")

            #入力データフレームからATRを求める一時間足を20時間分求める
            lis = []#一時間足のデータを格納するリスト
            for i in range(20):
                lis_ = []
                rousoku_1h = df_[-1-60*(20-i):-1-60*(20-i)+60]
                lis_.append(rousoku_1h[0,1])
                lis_.append(np.amax(rousoku_1h[:,2]))
                lis_.append(np.amin(rousoku_1h[:,3]))
                lis_.append(rousoku_1h[-1,4])

                lis.append(lis_)
            lis = np.array(lis) #一時間足のリストをnumpy配列に変換する
            #一時間足からATRを求める
            lis_atr = []
            for i in range(20):
                lis_atr_ = []
                if i == 0:#前日の値はないので無視する
                    lis_atr.append(lis[i][1]-lis[i][2])#当日の高値-当日の安値
                else:
                    lis_atr_.append(lis[i][1]-lis[i][2])#当日の高値-当日の安値
                    lis_atr_.append(abs(lis[i][1]-lis[i-1][3]))#当日の高値-前日の終値
                    lis_atr_.append(abs(lis[i][2]-lis[i-1][3]))#当日の安値-前日の終値

                    lis_atr.append(np.amax(np.array(lis_atr_)))

            atr = np.mean(lis_atr)#ATR値

            #直近10時間の最安値を求める
            max_10h = np.amax(lis[-10:,2])




            order_ = {}
            order_['position_time'] = df_[-1,0]
            order_['position_type'] = 'short'
            order_['position'] = df_[-1,4]
            order_['position_size'] = 10000
            order_['stoploss_rate'] = max_10h
            order_['profitable_rate'] = df_[-1,4]-0.5

            order.append(order_)

        else:
            order.append('no')

    else:
        order.append('no')

    return order
