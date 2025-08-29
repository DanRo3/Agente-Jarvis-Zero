# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /code

# Copia el archivo de dependencias y las instala
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia el código de la aplicación
COPY ./app /code/app

# Comando para ejecutar la aplicación
# El host 0.0.0.0 es necesario para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]