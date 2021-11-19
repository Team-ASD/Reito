# Reito

## Prerrequisitos
- Crear un nuevo entorno virtual
El sistema tendrá que correr en un entorno virtual provisto por la herramienta virtualenv, sin embargo primero tenemos que instalar dicha herramienta.
Primeramente instalamos pip que nos ayuda a instalar herramientas:
```shell
   $ sudo apt update

   $ sudo apt install python3-pip
   ```
Una vez instalado pip instalamos la herramienta virtualenv:
```shell
   $ sudo pip install virtualenv
   ```
Despues creamos el nuevo entorno virtual y lo activamos:
```shell
   $ cd .

   $ virtualenv env_reito

   $ . env_reito/bin/activate
   ```

- Clonar el repositorio
Instalamos git en caso de no tenerlo:
```shell
   $ sudo apt-get install git
   ```
Nos movemos al directorio donde vamos a almacenar el proyecto, una vez ahí ejecutamos las siguientes lineas:
```shell
   $ git clone https://github.com/Team-ASD/Reito

   $ cd Reito/reito/
   ```

- Instalar dependencias con archivo requirements.
Dentro de la carpeta raíz tenemos un archivo llamado requirements.txt el cual contiene todas las dependencias que necesita el proyecto para correr, ejecutamos la siguiente linea:
```shell
   $ pip install -r requeriments.txt
   ```
Dicha linea instalará todo lo necesario.

- Configurar cuenta de almacenamiento en Cloudinary (almacenamiento de imagenes)
Será necesario tener una cuenta de Cloudinary.
Puedes crearla en el siguiente link: https://cloudinary.com/
Cambiar datos de cuenta en el archivo settings.py ubicado en /reito/settings.py en las lineas indicadas. Los datos solicitados los proporciona Cloudinary en la pantalla principal de su plataforma.
```shell
   104   cloudinary.config( 
   105      cloud_name = "CloudName de tu cuenta", 
   106      api_key = "api_key de tu cuenta", 
   107      api_secret = "api_secret de tu cuenta" 
         )
   ```

- Realizar migraciones y llenar BD con destinos por defecto.
Para crear las entidades en la base de datos tenemos que correr las siguientes lineas:
```shell
   $ python3 manage.py makemigrations

   $ python3 manage.py migrate

   $ python3 script_destinos.py
   ```

## Probar el proyecto
Una vez instaladas todas las dependencias y configurado todo lo necesario verificaremos que el proyecto corre de manera correcta.

- Ejecutar el sistema

Con la siguiente linea se ejecuta el sistema:
```shel
   $ python3 manage.py runserver 0.0.0.0:8000 
   ```
Si el sistema está corriendo de manera correcta podremos acceder de la siguiente manera:
   > http://localhost:8000/

Lo cual debe de mostrar el Home del sistema.

## Versión

1.0.0 - Septiembre 2021

## Autores

* **Gerardo Jiménez Arguelles**
* **Oscar Leonardo Corvera Espinosa**
* **Luis Alberto Gómez Delgado**
* **José de Jesús Jiménez Arguelles**
* **Martín Salas Orozco**