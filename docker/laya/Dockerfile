FROM python:3.11-slim

# Set pip timeout and retry limits globally
ENV PIP_DEFAULT_TIMEOUT=1000 \
    PIP_RETRIES=10

# Option A (Recommended): Pre-install CPU-only PyTorch (~180MB vs ~450MB) 
# to keep image small and avoid PyPI timeout issues
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install laya and uvicorn
RUN pip install --no-cache-dir "laya[serve]" uvicorn

ENV LAYA_MODELS="english,multilingual"
ENV LAYA_HOST="0.0.0.0"
ENV LAYA_PORT="8001"
ENV LAYA_PRELOAD="1"

EXPOSE 8001

CMD ["laya-serve"]