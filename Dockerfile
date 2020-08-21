FROM jcdemo/flaskapp

WORKDIR /src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b","0.0.0.0:5000","wsgi:application", "--log-file", "gunicorn.log"]

COPY . .
