FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
    clustalo \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000
# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]