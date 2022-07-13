FROM python:3.10.4-alpine3.15
COPY . /application
WORKDIR /application
RUN apk add --no-cache git && pip install -r requirements.txt
CMD  python commit_helper.py changelog --dir="./invitation-api" | python main.py changelog
