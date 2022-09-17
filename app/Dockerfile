FROM python:3.8-slim
WORKDIR /app
COPY .requirements/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY app .
ENV FLASK_APP=.
COPY entrypoint.sh entrypoint.sh
ENV FLASK_ENV=development
RUN chmod u+x entrypoint.sh
CMD [ "entrypoint.sh" ]

