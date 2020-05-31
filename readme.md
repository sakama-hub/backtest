
# FX_backtest

pythonで書いたFX自動売買アルゴリズムのバックテストツール
 
# インストール方法
　※windows10環境を想定
 
 1)python3.6をインストール
 
 2)コマンドプロンプトからgitリポジトリをクローン
 
 ```bash
git clone https://github.com/sakama-hub/backtest.git
```

3)フォルダに移動し，必要なパッケージをインストール

```bash
cd backtest
pip install -U -r requirements.txt
```
 
# 使い方
 1. trade_algolithm.py内に自分の考えた売買アルゴリズムを記載（仕様はtrade_algolithm_sample.pyを参照）
 
 2. backtest_data内に検証データを入れる（データ形式はsample_data.csvを参照）
 
 3. 適宜，フォルダprofitable_update，stoploss_update内に各種プログラムを入れる
 
 4. コマンドプロンプト上でbacktest.pyを実行
 
# 各種ファイル・フォルダ

 * framework:検証に用いるクラスモジュール
 * profitable_update：利確の指値更新関数を入れるためのフォルダ．デフォルトとしてはreadmeファイルのみ
 * stoploss_update：損切の逆指値更新関数を入れるためのフォルダ．デフォルトとしてはreadmeファイルのみ
 * backtest_result：検証結果データを保存するためのフォルダ
 * trade_algorithm：売買ルール，資金管理を組み込むためのフォルダ
 * backtest_data：検証データを入れるためのフォルダ
 * backtest.py：実行スクリプト
 

# メモ
 
バックテストデータの取得方法は別サイトを参考のこと
 
# Author
 
* 作成者　さかま　
* 所属　とある日本の大学
* E-mail 1604338t@gmail.com
 
