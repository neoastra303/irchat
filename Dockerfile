FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENTRYPOINT ["python", "irc_chat.py"]
CMD ["irc.libera.chat", "6667"]