FROM python:3.9.7-slim

ENV AM_I_IN_A_DOCKER_CONTAINER=True

RUN pip install -U pip


WORKDIR /app


COPY requirements.txt ./
COPY [ "predict_app.py", "xgb_reg.pkl", "./" ]

RUN pip install -r requirements.txt

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict_app:app" ]

