FROM python:3.9.5

# 修改镜像时区
ENV TimeZone=Asia/Shanghai
# 使用软连接，并且将时区配置覆盖/etc/timezone
RUN ln -snf /usr/share/zoneinfo/$TimeZone /etc/localtime && echo $TimeZone > /etc/timezone
RUN sed -i 's/cn.archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

COPY app /app
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 5000
WORKDIR /app
ENTRYPOINT ["gunicorn", "-b","0.0.0.0:5000","wsgi:application"]
