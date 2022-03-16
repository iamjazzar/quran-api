FROM python:3

ENV PYTHONUNBUFFERED=1

COPY requirements* /app/

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements-test.txt

RUN groupadd -r quran  && useradd -r -g quran quran

RUN mkdir -p /app/media /app/static \
  && chown -R quran:quran /app/

COPY . /app/
WORKDIR /app

RUN python manage.py collectstatic --no-input

EXPOSE 8000
ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api.wsgi:application"]
