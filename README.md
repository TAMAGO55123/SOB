# SOB | Server Official BOT
サーバー管理のためのBOT

## セットアップ方法
> MacおよびLinuxのコマンドです。
- Pythonをインストールします。

    本環境は3.13.*で作成しています。
    ```sh
    # Pyenvの場合
    pyenv install -v 3.13.11
    pyenv local 3.13.11
    # Pythonインストーラー
    # https://www.python.org/downloads/release/python-31312/
    ```
- venvを作成します
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
- envを作成します
    
    .env.sampleをコピーして設定してください。
- 起動
    ```sh
    python main.py
    ```

    role.jsonが生成されます。