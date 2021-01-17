# HEVC Video Batch Converter

## Introducción

**hevcbatchconverter** es una herramienta desarrollada en Python3, que se apoya en las librerías [**ffmpeg**](https://ffmpeg.org/) para convertir videos al formato HEVC que es el que mejor se conporta con la aplicación Fotos en iCloud

El 'Layout' del proyecto, las recomendaciones de empaquetado y su distribución, han sido implementadas apoyándonos en en la documentación obtenida de ["The Hitchhiker’s Guide to Packaging"](https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/index.html) y de ["kennethreitz.org
Report abuse"](https://github.com/kennethreitz/samplemod)

Si lo que pretendes es simplemente descargar e instalar la herramienta para su uso, salta directamente a la sección [Instalación de la herramienta](#Instalación-de-la-herramienta). Si en cambio, tu intención es extender la herramienta, sigue los pasos documentados a continuación.

## Requisitos para el desarrollador

Esta documentación, esta orientada a desarrolladores que quieran extender la herramienta y que utilicen como plataforma de desarrollo 'Ubuntu' y desarrollen sobre un entorno virtual generado con [virtualenv](https://virtualenv.pypa.io)

En cualquier caso, para otros sistemas operativos, existen tutoriales análogos que nos permitirán desarrollar sobre el proyecto sin muchos problemas.

### Instalación de los requisitos mínimos

- [python3](https://www.python.org/), como lenguaje de desarrollo

```bash
$sudo apt install python3
```

- [pip3](https://pypi.org/project/pip/), como administrador de paquetes python

```bash
$sudo apt install python3-pip
```

- [virtualenv](https://virtualenv.pypa.io), nos permite aislar nuestro entorno de desarrollo en Python y sus dependencias. Para su instalación ejecutamos:

```bash
$sudo apt install python3-venv
```

### Otros requisitos recomendados

- Ubuntu 18 o superior
- Visual Studio Code

## Instalación del proyecto

- Clonar el proyecto en un directorio en local

```bash
$git clone git@github.com:rvillamil/hevc-video-batch-converter.git
```

- Crear el entorno virtual con [virtualenv](https://virtualenv.pypa.io). El entorno, lo podemos generar donde creamos conveniente, aunque una buena opción es dentro del propio proyecto de la siguiente forma:

```bash
$python3 -m venv .venv
```

- Activación del entorno virtual

```bash
$source .venv/bin/activate
```

- Para desactivar un entorno virtual, porque se necesita trabajar en otro diferente, se ejecuta el comando **deactivate** de virtualenv. No es necesario ir al directorio del entorno virtual para realizar esta operación:

```bash
$deactivate
```

- Para la instalación de las dependencias para el desarrollo del proyecto, se ejecuta, **dentro del entorno virtual**, el comando:

```bash
$python setup.py develop
```

## Pruebas unitarias

Se utiliza el soporte de [**pytest**](https://docs.pytest.org/) para lanzar las pruebas.

- **Dentro del entorno virtual**, en la raíz del directorio del proyecto ejecutamos:

```bash
$python -m pip install -U pytest
```

- Ahora, previa [Configuración de la herramienta](#Configuración-de-la-herramienta), podrás correr las pruebas unitarios,con el comando:

```bash
$pytest
```

Otra opción sería ejecutarlas con la herramienta de **setup** de la siguiente forma:

```bash
$python setup.py pytest
```

## Linter y "formateador" de código recomendados

Como recomendación, puedes instalar **dentro del entorno virtual**, las siguientes herramientas:

- Como 'Linter' usaremos **flake8**

```bash
$python -m pip install -U flake8
```

- Como "formateador" usaremos **autopep8**

```bash
$python -m pip install -U autopep8
```

## Generación de una 'Release'

Antes de generar una release, deberías de:

- Actualizar el fichero CHANGELOG.md con el contenido de la release asociado a una version

- Generar la el fichero 'tgz' con la release:

```sh
$python setup.py sdist
```

Esto creará un subdirectorio **dist** dentro del proyecto con un fichero en formato **.tgz** listo para su distribución e instalación.

- Subir los cambios anteriores a la rama 'develop'

- "Mergear" 'Develop' a 'Master' desde el interface de GitLab

- Crear un [tag](https://github.com/rvillamil/hevc-video-batch-converter/releases) con la **'release'** y adjuntar el artefacto al tag como parte de la documentación

- Finalmente, actualizar el fichero con la versión del proyecto [__version__py](/hevcbatchconverter/__version__.py), siguiendo las normas de [SemVer](http://semver.org/)

## Instalación de la herramienta

### Desde el código fuente

Si eres un desarrollador y te has descargado el código fuente y configurado el entorno de desarrollo como se explicar al comienzo de la guía, se trataría de lanzar desde **fuera del entorno virtual** el comando de instalación de la herramienta:

```sh
$pip3 install -e . --user # --user , indica que se lo debe instalar solo para el usuario activo. Si se omite el parámetro se instalaría para todos los usuarios
```

### Desde una release

Si eres un usuario y te has descargado una ['Release'](https://github.com/rvillamil/hevc-video-batch-converter/releases), el procedimiento sería:

- Instalar python3 y el gestor de paquetes pip3 si no lo has hecho ya
  
```bash
$sudo apt install python3 python3-pip
```

- Descomprimir el fichero de la siguiente forma:
  
```sh
$tar xvf hevcbatchconverter-*.tar.gz
```

- Dentro del directorio del proyecto, ejecutar el comando:
  
```sh
$pip3 install -e . --user # --user , indica que se lo debe instalar solo para el usuario activo. Si se omite el parámetro se instalaría para todos los usuarios
```

## Desinstalación de la herramienta

Lanzar desde una terminal

```sh
$pip3 uninstall hevcbatchconverter
```

## Anexos

### Sobre Visual Studio Code

Una configuración recomendada para Visual Studio Code podría establecerse en el **settings.json** del proyecto.

```json
{
    "python.pythonPath": ".venv/bin/python",
    "python.testing.pyTestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pyTestEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.formatting.provider": "autopep8"
}
```

## Licencia

Este proyecto está licenciado bajo la licencia de [MIT](https://opensource.org/licenses/MIT). Ver el fichero [LICENSE](LICENSE) para mas detalles.
