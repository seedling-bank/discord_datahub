FROM python:3.11
WORKDIR /
COPY main.py /
COPY requirements.txt /
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["python", "main.py"]


