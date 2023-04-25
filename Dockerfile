FROM python:3.11-slim-bullseye

ENV HOME /home/cisa
RUN useradd -m cisa
WORKDIR $HOME
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt
USER cisa

COPY cisa.py cisa.py
COPY config.py config.py
COPY utils utils
COPY cogs cogs

RUN ln -sf /run/secrets/cisabot-config config.json

CMD ["python3", "cisa.py"]
