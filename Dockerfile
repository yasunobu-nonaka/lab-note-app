FROM python:3.13-slim

RUN apt-get -q -y update
RUN apt-get install -y gcc

ENV USERNAME=lab-note-user
ENV USERGROUP=lab-note-group
ENV WORKING_DIR=/app

WORKDIR ${WORKING_DIR}

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN groupadd ${USERGROUP} && useradd -g ${USERGROUP} ${USERNAME}
RUN chown -R ${USERNAME}:${USERGROUP} ${WORKING_DIR}
RUN chmod -R u=rwx,g=rwx ${WORKING_DIR}

USER ${USERNAME}
ENV PATH "$PATH:/home/${USERNAME}/.local/bin"

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
