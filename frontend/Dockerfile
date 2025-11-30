# === Build Stage ===
FROM node:20-bookeorm-slim AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# === Production Stage ===
FROM nginx:stable-alpine-slim

# Cloud Run 需要服務監聽 $PORT
ENV PORT=8080
EXPOSE 8080

# 替換 Nginx 預設設定，讓其使用 PORT（Cloud Run 會注入 PORT）
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 放置 Vue build output
COPY --from=builder /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]