FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENV TOKEN="MTI1OTgzNjkzMDY1MzQyNTcxNQ.G9z-7S._v_9_aq6OyZfa_WvrX1-nfPE3sXbQzq0CC36QA"
CMD ["python", "main.py"]
