# common (común) 

```
Del lat. commūnis.
```

1. `adj.` Dicho de una cosa: Que, no siendo privativamente de nadie, pertenece o se extiende a varios. *Bienes, pastos comunes*.
2. `adj.` Corriente, recibido y admitido de todos o de la mayor parte. *Precio, uso, opinión común*.
3. `adj.` Ordinario, vulgar, frecuente y muy sabido.
4. `adj.` Bajo, de inferior clase y despreciable.
5. `m.` Todo el pueblo de cualquier ciudad, villa o lugar.
6. `m.` Comunidad, generalidad de personas.
7. `m.` retrete (‖ aposento).

> Source https://dle.rae.es/com%C3%BAn

# Common Library (v2019.11.28)

## Instalación

Se requiere la versión de `python` **>=3.6**, en adelante.

### Con entorno virtual

```bash
# creamos el entorno virtual
> virtualenv --python=python37 common

# ingresamos al directorio del entorno
> cd common

# iniciamos el entorno
> source ./bin/activate

# instalamos dentro del entorno
> pip install https://github.com/aysa-sa/common/archive/2019.11.28.zip
```

### Sin entorno virtual

```bash
# Instalar
> pip install https://github.com/aysa-sa/common/archive/2019.11.28.zip

# Actualizar
> pip install https://github.com/aysa-sa/common/archive/2019.11.28.zip --upgrade
```

### Desde el código fuente

```bash
# clonamos el repositorio
> git clone https://github.com/aysa-sa/common.git --branch 2019.11.28 --single-branch 

# ingresamos al directorio del repositorio
> cd common

# instalamos
> python setup.py install
```

# Desarrollo

## Repositorio

```bash
# clonación
> git clone https://github.com/aysa-sa/common.git

# acceso al proyecto
> cd common
```

## Dependencias

Las dependencias se encuentran definidas en el archivo `Pipfile`, para la gestión de las mismas es requerido tener instalado `pipenv`, visitar [**site**](https://pipenv.readthedocs.io/).

### Pipenv

* Documentación: [**usage**](https://pipenv.readthedocs.io/en/latest/#pipenv-usage).
* Instalación: `pip install pipenv`.

#### Instalación de las dependencias:

```bash
> pipenv install
```

#### Iniciar el Shell:

```bash
> pipenv shell
```

#### Crear el archivo `requirements.txt`

```bash
> pipenv lock --requirements > requirements.txt
```