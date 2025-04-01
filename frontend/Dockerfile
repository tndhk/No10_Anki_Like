FROM node:18-alpine

WORKDIR /app

# 依存関係をインストール
COPY package*.json ./
RUN npm install

# アプリケーションのソースをコピー
COPY . .

# 開発モードで起動
CMD ["npm", "run", "dev"]
