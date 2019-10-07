FROM python:3.7
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY app.py /app/app.py
COPY .git /app/.git
ENV FLASK_APP=app.py
CMD ["scope-run", "gunicorn", "-b", "0.0.0.0:8000", "app:app"]
