FROM python:3.11

WORKDIR /service

COPY ./requirements.txt /service/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /service/requirements.txt

COPY . .

EXPOSE 8000

RUN chmod 700 prestart.sh

ENTRYPOINT [ "/bin/bash" ]

CMD [ "./prestart.sh" ]