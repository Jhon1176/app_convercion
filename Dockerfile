# 1. Escoger una imagen base de Python pequeña y oficial para ahorrar espacio
FROM python:3.10-slim
# 2. Definir el directorio de trabajo dentro del contenedor (dentro del sistema de archivos del contenedor)
WORKDIR /app
# 3. Copiar todos los archivos del proyecto a esa carpeta /app dentro del contenedor
COPY . .
# 4. Instalar las dependencias que definiste en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# 5. Indicar que el contenedor expondrá el puerto 5000 (el que usa Flask)
EXPOSE 5000
# 6. Comando para iniciar la aplicación cuando el contenedor arranque
CMD ["python", "app.py"]
