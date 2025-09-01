# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /code

# Instala uv
RUN pip install uv

# Copia solo el archivo de dependencias
COPY requirements.txt /code/
RUN uv pip install --system --no-cache -r /code/requirements.txt

# Copia solo el código de la aplicación
COPY ./app /code/app

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]