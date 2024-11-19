FROM python:3.11.2

RUN pip3 install --upgrade pip
RUN pip3 install PyYAML requests 
RUN pip3 install --upgrade streamlit
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE none

EXPOSE 5142 8501

ADD opensyslog_helper.py opensyslog_syslog.py main_opensyslog.py web_ui.py const.py /

ARG GIT_TAG=unknown
LABEL version=$GIT_TAG
 
CMD ["python", "-u", "./main_opensyslog.py"]
