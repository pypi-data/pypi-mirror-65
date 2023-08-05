# Clitellum

## Introducción

Es un framework de comunicación que es capaz de utilizar conectores tcp, amqp y zeromq, indistintamente. Puede ser usado para implementar publicadores de eventos, suscriptores de eventos, intercambiadores de protocolo, etc.

Implementa patrones de diseños empresariales como el “Reliable Endpoint”, que en caso de producirse un pérdida de conexión, el propio endpoint es capaz de volverse a conectar, tantas veces como sea necesario, ya sea para recibir un mensaje como para enviarlo. O patrones como el “Dead Letter Channel”, que en caso de producirse un error durante el procesamiento del mensaje, se envía el mensaje a un endpoint de errores, para que sea investigado.

Por esto, es muy útil para implementar microservicios en python, o intercambiadores de protocolo, ya que los endpoints de entrada y salida pueden ser de tipos diferentes.

Mas información en la web

https://clitellum.hotaka.io/

# Configuracion entorno de python
Instalación de librabbitmq

```
brew install autoconf automake pkg-confi
git clone git://github.com/celery/librabbitmq.git
cd librabbitmq
make install

python3 setup.py install
```

En entornos linux Ubuntu se puede bajar directamente del repositorio
```
pip install librabbitmq
```

Instalación de pipenv
```
pip3 install pipenv
```

Creacion de un entorno virtual de python3
```
pipenv --three
```

Instalación de todos los requerimientos
```
pipenv install
o
pipenv install --dev
```

Activacion de la consola
```
pipenv shell
```

Ejecución de los test
```
cd tests
pipenv run python runner_test.py
```

# Generación pypi

```bash
python3 setup.py sdist bdist_wheel bdist_egg
python2 setup.py bdist_wheel bdist_egg

twine upload dist/*
```
