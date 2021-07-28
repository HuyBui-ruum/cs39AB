# CS39AB - Cloud Computing - Summer 2021
# Instructor: Thyago Mota
# Description: Activity 10 - Extract the dollar to real exchange rate, saving it into a database.

FROM python:latest 
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ethereum_scrape.py .
ENV DB_HOST=lab3.cc6kw1lnwyaw.us-west-1.rds.amazonaws.com
ENV DB_NAME=ethereum
ENV DB_USER= ethereum
ENV DB_PASSWORD=12345678
CMD ["python", "ethereum_scrape.py"]