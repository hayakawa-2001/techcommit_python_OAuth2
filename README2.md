# techcommit_python_OAuth2

# tech commitでの練習問題「OAuth認証の実装」を作成しました。
<https://www.tech-commit.jp/>

# 内容
Twitter APIを実行するためのTokenを取得する。  
OAuth2.0で認証後Tokenを取得する。

# 実行方法
コンソールでOAuth2.pyを実行する。

# 実行結果
実行後ブラウザが立ち上がりTwitterの認証連携画面に遷移する。  
コンソールに下記が出力される。

    http server start
    127.0.0.1 - - [dd/Sep/2021 HH:MM:SS] "GET /?oauth_token=xxxxxxxx&oauth_verifier=xxxxxxxx HTTP/1.1" 200 -
    oauth_token =  xxxxxxxx
    oauth_verifier =  xxxxxxxx
    http server shutdown
    access_token =  xxxxxxxx
    token_secret =  xxxxxxxx
