# GrowTech

El problema que `GrowTech` busca solucionar es la falta de un sistema eficiente de monitoreo agrícola, lo cual afecta a los aficionados a la jardineria hogareña. Actualmente, enfrentan dificultades para supervisar las condiciones ambientales, el riego y la salud de los cultivos. La falta de información precisa y oportuna dificulta la toma de decisiones informadas, lo que puede resultar en pérdidas de rendimiento y calidad en los cultivos.

# Pasos para ejecutar el proyecto

1. clona el repositorio:
   ```git
   git clone https://github.com/FerchoKD/GrowTech_rest.git
   ```
2. Navega hacia la carpeta ...
   ```shell
   cd GrowTech_rest/
   ```
   ## Dentro de la carpeta ejecuta los siguentes comandos:
   <br>
3. Crea una virtual environment usando el comando:
   
    ```python
    python -m venv env
    ```
    
4. Activa la virtual enviornment con el comando:
    ```python
    # for Linux
    source env/bin/activate

    # for Windows
    .\env\Script\activavte
    ```
    
5. Instala las dependencias:
   ```python
   pip install -r requirements.txt
   ```
6. Genera los archivos de migracion con:
   ```python
   python manage.py makemigrations
   ```
   
7. Ejecuta las migraciones con:
   ```python
   python manage.py migrate
   ```
8. Finalmente podras correr el proyecto con el comando:
   ```python
   python manage.py runserver
   ```
