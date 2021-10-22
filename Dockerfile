FROM python:3.8-slim

# COPY global_requirments.txt /code/global_requirments.txt
# COPY requirements.txt /code/requirements.txt

WORKDIR /code
ENV PYTHONPATH=/code

COPY ./ /code

# RUN pip install --user -r requirements.txt
# RUN pip install --user -r global_requirments.txt

ENTRYPOINT ["python", "twitter_api/scripts/search.py"]