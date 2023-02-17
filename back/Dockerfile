FROM python:3.10

RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup \
 && chmod +x mariadb_repo_setup \
 && ./mariadb_repo_setup \
 && rm mariadb_repo_setup \
 && apt-get update \
 && apt-get install -y \
      libmariadb3 \
      libmariadb-dev \
 && rm -rf /var/cache/apt/*

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD back.py .

CMD ["uvicorn", "back:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
