FROM python:3.11.5

WORKDIR /usr/src/app

COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# run the command
# CMD ["python", "./app.py"]
CMD guincorn -b 0.0.0.0:5000 app:app --timeout 600