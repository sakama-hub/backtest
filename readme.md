・概要：このディレクトリには検証するために必要なフォルダ，ファイルがまとめれている
・各ファイルの説明
framework:検証に用いるクラスモジュールがはいいている．
profitable_update：利確の指値更新関数を入れるためのフォルダ．デフォルトとしてはreadmeファイルのみ
backtest_result：検証結果データを保存するためのフォルダ
trade_algorithm：売買ルール，資金管理を組み込むためのフォルダ
stoploss_update：損切の逆指値更新関数を入れるためのフォルダ．デフォルトとしてはreadmeファイルのみ
backtest_data：検証データを入れるためのフォルダ
backtest.py：実行スクリプト

4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
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
 

 
# Note
 
バックテストデータの取得方法は別サイトを参考のこと
 
# Author
 
* 作成者　さかま　
* 所属　とある日本の大学
* E-mail 1604338t@gmail.com
 
