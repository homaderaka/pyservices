FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

# Run main.py when the container launches
CMD ["python", "./service/main.py"]
