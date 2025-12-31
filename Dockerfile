FROM python:3.9-slim

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV HF_ENDPOINT=https://hf-mirror.com

WORKDIR /app
ADD instantclient-basic-linux.x64-11.2.0.4.0.zip /tmp/

# 安装基础依赖
RUN apt-get update && apt-get install -y \
    alien \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/oracle/instantclient

RUN unzip /tmp/instantclient-basic-linux.x64-11.2.0.4.0.zip \
    && mv instantclient_*_* /opt/oracle/instantclient




# 手动安装 libaio（如果包名找不到）
RUN cd /tmp && \
    wget http://ftp.de.debian.org/debian/pool/main/liba/libaio/libaio1_0.3.113-2_amd64.deb && \
    dpkg -i libaio1_0.3.113-2_amd64.deb || apt-get install -f -y && \
    rm -f libaio1_0.3.113-2_amd64.deb && \
    wget https://download.oracle.com/otn_software/linux/instantclient/185000/oracle-instantclient18.5-basiclite-18.5.0.0.0-3.x86_64.rpm && \
    wget https://download.oracle.com/otn_software/linux/instantclient/185000/oracle-instantclient18.5-devel-18.5.0.0.0-3.x86_64.rpm && \
    alien -i oracle-instantclient18.5-basiclite-18.5.0.0.0-3.x86_64.rpm && \
    alien -i oracle-instantclient18.5-devel-18.5.0.0.0-3.x86_64.rpm

# 设置环境变量
ENV LD_LIBRARY_PATH="/opt/oracle/instantclient/instantclient_11_2:${LD_LIBRARY_PATH}"
ENV ORACLE_HOME=/opt/oracle/instantclient/instantclient_11_2
# 创建符号链接
RUN cd /opt/oracle/instantclient/instantclient_11_2 && \
    ln -sf libclntsh.so.* libclntsh.so

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 启动 Flask 应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]