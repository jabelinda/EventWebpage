FROM python:3-alpine3.17
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
VOLUME /app/instance
EXPOSE 80:80
CMD python3 ./main.py
