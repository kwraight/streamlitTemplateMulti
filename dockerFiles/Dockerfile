# base image
FROM python:3.9.15

# exposing default port for streamlit
EXPOSE 8501

# copy over and install packages
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r /core/requirements.txt

# copying everything over
COPY *.py ./code/
COPY core/*.py ./code/core/
COPY corePages/*.py ./code/corePages/
COPY userPages/ ./code/userPages/


WORKDIR code

# match exposed port
CMD ["streamlit", "run", "mainApp.py","--server.port=8501"]
