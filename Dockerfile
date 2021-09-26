FROM python:3.9-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY sources/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY sources /app

CMD [ "python", "main.py" ]