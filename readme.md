
# FX_backtest

pythonで書いたFX自動売買アルゴリズムのバックテストをツール
 
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
 
 
# 各種ファイル・フォルダ

 * framework:検証に用いるクラスモジュール
 * profitable_update：利確の指値更新関数を入れるためのフォルダ．デフォルトとしてはreadmeファイルのみ
 * stoploss_update：損切の逆指値更新関数を入れるためのフォルダ．デフォルトとしてはreadmeファイルのみ
 * backtest_result：検証結果データを保存するためのフォルダ
 * trade_algorithm：売買ルール，資金管理を組み込むためのフォルダ
 * backtest_data：検証データを入れるためのフォルダ
 * backtest.py：実行スクリプト
 
# 使い方
1. gs
2. dfa
# メモ
 
バックテストデータの取得方法は別サイトを参考のこと
 
# Author
 
* 作成者　さかま　
* 所属　とある日本の大学
* E-mail 1604338t@gmail.com
 
