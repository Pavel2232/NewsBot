FROM python:3.11.6

WORKDIR /

RUN pip install "poetry==1.8.2"



COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

EXPOSE 8000
ENTRYPOINT ["bash","entrypoint.sh"]
CMD ["gunicorn", "NewsBot.wsgi", "-w", "4","-b","0.0.0.0:8000"]




