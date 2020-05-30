・クラスメソッドの定義
　　・formattimg()
　　　　　・説明：口座資金などの初期化
　　　　　・引数
　　　　　　　　fund 　　型：整数型，説明：初期化口座資金
　　　　　　　　systemstop_rate 　　型：整数型，説明：システムを止める額，デフォルト：None
・クラス変数の定義
　　・__fund
　　　　・説明：口座資金を保存する．初期化関数formattimg()で初期化する
　　・__systemstop_rate
　　　　・説明：口座資金がこの値以下になったら破産として認め，検証をストップする
　　・__fund_stream
　　　　・説明：各時間の口座資金金額のリスト
　　・__PaL
　　　　・各時間の損益のリスト
・メソッド属性の定義
　　・init()　説明：データ属性の初期化
　　　　・引数
　　　　　　・position_type →型：文字型，指定：'long','short',説明：買いか売りを指定，初期値：None
　　　　　　・position →型：浮動小数点型，説明：ポジションをとったレート，初期値：None
　　　　　　・position_size →型：整数型，説明：取引通貨量，初期値：None
　　　　　　・stoploss_rate →型：浮動小数点型，説明：損切の逆指値を置くレート,初期値：None
　　　　　　・profitable_rate →型：浮動小数点型，説明：利確の指値を置くレート，初期値：None
　　　　　　・state →型：文字列型，指定：'off','on'，説明：取引している状況かそうでないか，初期値：'off'
　　　　　　・stoploss_update →型：関数，説明：損切の逆指値を更新（順行方向に）する関数，デフォルト値：None
　　　　　　・profitable_update →型：関数，説明：利確の指値を更新する関数，デフォルト値：None
　　　　　　・spread →型：浮動小数点型，説明：トレードを行うペアのスプレッド(単位pipsとする)

