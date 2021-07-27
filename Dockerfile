FROM python:3.9

ENV PYTHONPATH "${PYTHONPATH}:/config"
ENV PYTHONPATH "${PYTHONPATH}:/src"

COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt

COPY src src
COPY config config
COPY data data

EXPOSE 10400

CMD [ "python", "./src/motiontag_challenge/main.py" ]