FROM python:3.9.1

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv

RUN pipenv install

COPY . .
COPY .env.production .env

CMD ["pipenv", "run", "python", "bot.py"]