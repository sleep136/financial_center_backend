FROM python:3.9-slim

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV HF_ENDPOINT=https://hf-mirror.com
WORKDIR /app
# 安装基础依赖
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://apt.oracle.com/ oracle-repository main" > /etc/apt/sources.list.d/oracle.list && \
    wget -qO - https://apt.oracle.com/oracle-repository.key | apt-key add - && \
    apt-get update && \
    apt-get install -y oracle-instantclient-basic

# 设置环境变量
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH
ENV ORACLE_HOME=/opt/oracle/instantclient


# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 启动 Flask 应用
#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]