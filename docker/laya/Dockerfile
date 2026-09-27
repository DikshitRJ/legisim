FROM python:3.11-slim
RUN pip install --no-cache-dir "laya[serve]" uvicorn
ENV LAYA_MODELS="english,multilingual"
ENV LAYA_HOST="0.0.0.0"
ENV LAYA_PORT="8001"
ENV LAYA_PRELOAD="1"
EXPOSE 8001
CMD ["laya-serve"]
