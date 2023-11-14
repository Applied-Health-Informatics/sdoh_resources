FROM python:3.11.6-alpine3.18
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5001
CMD [ "python", "app.py" ]

# build command: docker build -t sdoh .
# run command: docker run -p 5005:5001 sdoh
