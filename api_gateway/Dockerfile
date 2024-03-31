# 
FROM python:3.8

# 
WORKDIR /api_gateway

# 
COPY ./requirements.txt /api_gateway/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /api_gateway/requirements.txt

# 
COPY ./app /api_gateway/app
EXPOSE 8000
# 
CMD ["uvicorn", "app.main:app","--host","0.0.0.0", "--port", "8000"]
