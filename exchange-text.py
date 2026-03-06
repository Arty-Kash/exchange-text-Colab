import nest_asyncio
from pyngrok import ngrok
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# --- 設定 ---
NGROK_AUTH_TOKEN = "ngrok auth token"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- データ構造（送られてくるデータの中身） ---
class UserData(BaseModel):
    name: str

# --- 処理（エンドポイント） ---
@app.post("/hello")
def say_hello(data: UserData):
    # 受け取った名前に文字を足して返すだけ
    return {"message": f"Pythonサーバーから： {data.name}さん、こんにちは！"}

# --- 起動 ---
public_url = ngrok.connect(8000)
print(f"★★★ 公開URL: {public_url} ★★★")

nest_asyncio.apply()
config = uvicorn.Config(app, host="0.0.0.0", port=8000)
server = uvicorn.Server(config)
await server.serve()

