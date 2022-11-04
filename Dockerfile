FROM python:3.10 as builder
RUN mkdir -p /otp
WORKDIR /otp
COPY pyproject.toml poetry.lock /otp/
ENV POETRY_VIRTUALENVS_CREATE false
RUN pip3 install pip --upgrade && pip3 install poetry --upgrade --pre && poetry install --no-root --only main

FROM python:3.10-slim
WORKDIR /otp
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY . /otp
CMD ["uvicorn" ,"otp.app:app", "--host", "0.0.0.0"]
