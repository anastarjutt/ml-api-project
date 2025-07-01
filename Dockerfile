FROM python:3.11-slim
WORKDIR /p7
COPY p7/ .
COPY linux_wheels/ .
COPY linux_wheels/ ./linux_wheels/
RUN pip install --no-index --no-cache-dir --find-links=linux_wheels -r requirements.txt
EXPOSE 8000
CMD [ "uvicorn","main:app","--host","0.0.0.0","--port","8000" ]