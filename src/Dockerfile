FROM python:3.11.4-alpine

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /api

EXPOSE 5005

RUN apk update

RUN pip install --upgrade pip

COPY ./requirements.txt /api/requirements.txt

RUN pip install -r requirements.txt


COPY . /api

#ENTRYPOINT
CMD [ "sh", "entrypoint.sh" ]