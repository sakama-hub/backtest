import pandas as pd
import numpy as np

class settlement:

    __fund = 0 #口座資金
    __systemstop_rate = 0 #システムステップ額


    __fund_stream = [] #各時間の口座資金額のリスト
    __PaL = [] #各時間の損益額リスト



    #クラス変数の初期化（シミュレーション開始時に呼び出す必要がある）
    @classmethod
    def formattimg(cls,fund,systemstop_rate=None):

        cls.__fund = fund
        cls.__systemstop_rate = systemstop_rate

        return 0

    #インスタンスの初期化関数（インスタンス定義時自動に行われる）
    def __init__(self,currency_pair,setup,stoploss_update=None,profitable_update=None,spread=0):

        self.__currency_pair = currency_pair #取引通貨のペア

        self.__position_time = None #ポジションをとった時間
        self.__position_type = None #ポジションタイプ
        self.__position = None #ポジションレート
        self.__position_size = None #取引通貨量
        self.__stoploss_rate = None #損切の逆指値
        self.__profitable_rate = None #利確の指値値

        self.__rate_df = None #現時点までのレートデータ

        self.__state = 'off' #取引状況

        self.__setup = setup #売買ルール関数
        self.__stoploss_update = stoploss_update #損切の逆指値更新関数
        self.__profitable_update = profitable_update #利確の指値更新関数

        self.__spread = spread #スプレッド額

        self.__trade_record = [] #この売買ルールの取引履歴

        self.__trade = 0 #累計トレード回数
        self.__win_trade = 0 #累積勝ちトレード回数
        self.__loss_trade = 0 #累積負けトレード回数
        self.__profit = [] #利益が出たトレードの利益額リスト
        self.__loss = [] #損失が出たトレードの損失額リスト


    #現時点のレートデータを更新する関数
    def rate_update(self,df):

        self.__rate_df  = df

        return 0



    def setup(self):

        return self.__setup(self.__rate_df)


    #セットアップが無いときのデータ更新関数
    def data_update1(self):

        settlement.__fund_stream.append(settlement.__fund) #その時点の口座資金の保存
        settlement.__PaL.append(0) #その時の利益を保存

        return 0

    #セットアップがある時のデータ更新関数
    def data_update2(self,order:dict):

        settlement.__fund_stream.append(settlement.__fund) #その時点の口座資金の保存
        settlement.__PaL.append(0) #その時の利益を保存

        self.__state = 'on'#取引状況を取引中に更新する

        self.__position_time = order['position_time'] #ポジション時間を時間　
        self.__position_type = order['position_type'] #ポジションタイプを保存
        self.__position = order['position'] #ポジションレートを保存
        self.__position_size = order['position_size'] #取引通貨量を保存
        self.__stoploss_rate = order['stoploss_rate'] #損切の逆指値のレート値の保存
        self.__profitable_rate = order['profitable_rate'] #利確の指値のレート値の保存

        return 0

    #決済しないときのデータの更新関数
    def data_update3(self):

        #損切の更新関数が入力されているときに損切の逆指値を更新する
        if self.__stoploss_update is not None:

            self.__stoploss_rate = self.__stoploss_update(position_type = self.__position_type,stoploss_rate = self.__stoploss_rate,df = self.__rate_df)

        #利確の更新関数が入力させているときに利確の指値を更新する
        if self.__profitable_update is not None:

            self.__profitable_rate = self.__profitable_update(position_type = self.__position_type,profitable_rate = self.__profitable_rate,df = self.__rate_df)

        settlement.__fund_stream.append(settlement.__fund) #その時点の口座資金の保存
        settlement.__PaL.append(0) #その時の利益を保存

        return 0

    #決済するときのデータの更新関数
    def data_update4(self):

        pip = (self.__rate_df.iloc[-1,4] - self.__position)*100#獲得pipsの計算

        #ポジションタイプが売りである時は正負を逆にする
        if self.__position_type == 'short':
            pip = -pip

        PaL = int((pip-self.__spread)/100*self.__position_size)   #損益額（スプレッド込み）

        settlement.__fund += PaL #損益を口座資金に反映
        self.__trade += 1 #トレード回数をカウント

        #勝ちもしくは負けトレードの回数，値を保存
        if PaL > 0:
            self.__win_trade += 1
            self.__profit.append(PaL)

        else:
            self.__loss_trade += 1
            self.__loss.append(PaL)

        #口座資金と損益の時系列データを保存
        settlement.__fund_stream.append(settlement.__fund) #その時点の口座資金の保存
        settlement.__PaL.append(PaL) #その時の利益を保存

        #この取引履歴listとして保存する
        lis = []

        lis.append(self.__currency_pair)
        lis.append(self.__position_time)
        lis.append(self.__position_type)
        lis.append(self.__position)
        lis.append(self.__position_size)
        lis.append(self.__rate_df.iloc[-1,0])
        lis.append(self.__rate_df.iloc[-1,4])
        lis.append(PaL)

        self.__trade_record.append(lis)



        #データ属性の注文内容データを初期化

        self.__position_time = None #ポジションタイム
        self.__position_type = None #ポジションタイプ
        self.__position = None #ポジションレート
        self.__position_size = None #取引通貨量
        self.__stoploss_rate = None #損切の逆指値
        self.__profitable_rate = None #利確の指値値
        self.__state = 'off' #取引状況

        return 0

    #決済するかの判断を行う関数
    def settle_distinction(self):

        judge = 'no'

        #ポジションタイプがロングの時
        if self.__position_type == 'long':
            if (self.__rate_df.iloc[-1,4] > self.__profitable_rate) or (self.__rate_df.iloc[-1,4] < self.__stoploss_rate):
                judge = 'yes'
        elif self.__position_type == 'short':
            if (self.__rate_df.iloc[-1,4] < self.__profitable_rate) or (self.__rate_df.iloc[-1,4] > self.__stoploss_rate):
                judge = 'yes'

        return judge

    #トレード状況を判断する関数
    def trade_judge(self):
        if self.__state == 'on':
            return 'yes'
        else :
            return 'no'


    #トレード結果を返す関数
    def test_result(self):
        result = []

        result.append(settlement.__fund)
        result.append(settlement.__trade)
        result.append(settlement.__win_trade)
        result.append(settlement.__loss_trade)
        result.append(settlement.__profit)
        result.append(settlement.__loss)
        result.append(settlement.__fund_stream)
        result.append(settlement.__PaL)

        return print(result)

    #トレード履歴を返す関数
    def trade_record(self):

        return pd.DataFrame(self.__trade_record,columns=['通貨ペア','注文日時','ポジションタイプ','注文レート','ポジションサイズ（通貨量）','決済日時','決済レート','損益'])

    #トレード結果の概要を返す関数
    def trade_overview(self):

        #破産確率を求める関数の定義
        def ded_per(funds,risk,payoff,win_per):
            def equation(x):

                p = win_per
                k = payoff
                return p * x**(k+1) + (1-p) - x

            def solve_equation():

                R = 0
                while equation(R)>0:
                    R += 1e-4
                if R>=1:
                    R=1
                return R

            def calculate_ruin_rate(R):
                e = funds / risk
                return R ** e

            return calculate_ruin_rate(solve_equation())

        #最大ドローダウンを求める関数
        def max_drawdown():

            drawdown_lis = []#ドローダウンを格納するリスト

            max_fund = settlement.__fund_stream[0]#その時点までの最大口座資金

            for fund in settlement.__fund_stream:

                #今の口座資金が過去の最大口座資金と比べて少なくなっているとき
                if max_fund > fund:

                    drawdown_lis.append((max_fund-fund)/max_fund*100)#ドローダウンを追加

                #今の口座資金が過去の最大資金以上時
                else:

                    drawdown_lis.append(0)

                    max_fund = fund#口座資金の最大値を更新

            return np.amax(drawdown_lis)







        win_per = self.__win_trade/self.__trade#勝率
        loss_per = self.__loss_trade/self.__trade#敗率
        win_ave = np.mean(self.__profit)#平均利益
        loss_ave = np.mean(self.__loss)#平均損失
        PL = win_ave/loss_ave*-1#ペイオフレシオ




        #関数として返すリストの初期化
        lis = []

        lis.append(self.__trade) #トレード回数
        lis.append(win_per) # 勝率
        lis.append(loss_per) #敗率
        lis.append(np.amax(self.__profit)) #最大利益
        lis.append(np.amin(self.__loss)) #最大損益
        lis.append(win_ave) #平均利益
        lis.append(loss_ave) #平均損失
        lis.append(PL) #ペイオフレシオ
        lis.append(max_drawdown()) #最大ドローダウン
        lis.append(win_per*PL-loss_per) #期待値
        lis.append(ded_per(settlement.__fund_stream[0],-1*loss_ave,PL,win_per)) #この売買ルールの破産確率

        return pd.DataFrame(lis,index=['トレード回数','勝率','敗率','最大利益','最大損益','平均利益','平均損失','ペイオフレシオ','最大ドローダウン（％）','期待値（％）','破産確率（％）'])
