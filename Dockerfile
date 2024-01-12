FROM python:3.12
WORKDIR /app
COPY python3.py /app/
RUN pip install requests
CMD ["python", "python3.py"]
