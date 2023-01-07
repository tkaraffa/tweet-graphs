FROM python:3.10-slim

# COPY global_requirments.txt /code/global_requirments.txt
COPY requirements.txt /code/requirements.txt

COPY ./ /code
WORKDIR /code
ENV PYTHONPATH=/code

# RUN pip install --user -r global_requirments.txt
RUN pip install --user -r requirements.txt

ENTRYPOINT ["python"]