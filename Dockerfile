FROM python:3.8-buster
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD python ./run_chessbot.py
