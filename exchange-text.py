import nest_asyncio  # Jupyter NotebookやColab内でasyncio（非同期処理）を重複して動かすためのライブラリ
from pyngrok import ngrok  # ローカルサーバーを外部公開（トンネリング）するためのngrokライブラリ
import uvicorn  # ASGIサーバー（FastAPIを動かすためのエンジン）
from fastapi import FastAPI  # Web APIフレームワークの本体
from pydantic import BaseModel  # データバリデーション（型定義）のためのライブラリ
from fastapi.middleware.cors import CORSMiddleware  # ブラウザからのクロスドメインリクエストを許可するための設定

# --- 設定 ---
# ngrokの認証トークンを設定（自分のアカウントのトークンをここに記述）
NGROK_AUTH_TOKEN = "ngrok auth token"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# FastAPIのインスタンスを作成
app = FastAPI()

# CORS（Cross-Origin Resource Sharing）の設定。
# JavaScript（ブラウザ）からこのサーバーにアクセスすることを許可する設定
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],      # すべてのサイトからのアクセスを許可
    allow_methods=["*"],      # GET, POSTなどすべてのメソッドを許可
    allow_headers=["*"]       # すべてのヘッダーを許可
)

# --- データ構造（送られてくるデータの中身） ---
# クライアント（JS側）から送られてくるJSONデータの構造を定義
class UserData(BaseModel):
    name: str  # 「name」というキーで文字列が送られてくることを期待

# --- 処理（エンドポイント） ---
# 「/hello」というURLに対してPOSTメソッドでアクセスがあった時の処理
@app.post("/hello")
def say_hello(data: UserData):
    # クライアントから届いた data.name を使って、返信メッセージを作成してJSON形式で返す
    return {"message": f"Pythonサーバーから： {data.name}さん、こんにちは！"}

# --- 起動 ---
# ngrokを使って、ローカルの8000番ポートをインターネットに公開し、そのURLを取得
public_url = ngrok.connect(8000)
print(f"★★★ 公開URL: {public_url} ★★★")

# Colab環境でuvicornを非同期実行できるようにパッチを当てる
nest_asyncio.apply()

# サーバーの設定（ホスト 0.0.0.0、ポート 8000番でFastAPIアプリを起動）
config = uvicorn.Config(app, host="0.0.0.0", port=8000)
server = uvicorn.Server(config)

# サーバーを待機・実行状態にする
await server.serve()
