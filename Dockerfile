FROM python:3.12.7
WORKDIR /usr/src/app
RUN pip install flask==3.1.0
RUN pip install requests==2.32.3
RUN pip install SQLAlchemy==2.0.36
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]