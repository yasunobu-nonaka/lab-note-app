FROM python:3.13-slim

RUN apt-get -q -y update && apt-get -y upgrade
RUN apt-get install -y gcc
RUN apt-get install -y netcat-openbsd

ENV USERNAME=lab-note-user
ENV USERGROUP=lab-note-group
ENV WORKING_DIR=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR ${WORKING_DIR}

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN groupadd ${USERGROUP} && useradd -g ${USERGROUP} ${USERNAME}
RUN chown -R ${USERNAME}:${USERGROUP} ${WORKING_DIR}
RUN chmod -R u=rwx,g=rwx ${WORKING_DIR}

USER ${USERNAME}
ENV PATH="$PATH:/home/${USERNAME}/.local/bin"

EXPOSE 5000

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "4", "run:app"]
