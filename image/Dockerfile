FROM amazonlinux:latest

RUN /usr/bin/curl -O https://bootstrap.pypa.io/3.2/get-pip.py
RUN /usr/bin/python get-pip.py
RUN /usr/local/bin/pip install -U pip setuptools
RUN /usr/bin/yum -y install gcc python27-devel libffi-devel openssl-devel zip

CMD ["/bin/bash"]
