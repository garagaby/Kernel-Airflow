# Kernel-Airflow
Implementación de un modelo de riesgo crediticio, tomando como archivo fuente *files/german_credit_data.csv*, implementado en un contenedor de Docker, el cuál genera gráficos del modelo de riesgo y distintas distribuciones. Además de la generación de dos archivos csv, los cuales contienen la clasificación completa del dataset de acuerdo a los modelos (RandomForest y GaussianNB), todo esto orquestado mediante Apache AirFlow.


## Tecnológias
- Python3
- Apache Airflow 
- Docker

## Carpetas del Proyecto
- **bin** Contiene los archivos python para la lectura, generación de gráficas, implementación de modelos y escritura de datasets.
- **files** Contiene el archivo fuente *german_credit_data.csv* para la implementación del modelo de riesgo. 
- **dags** Se encuentra el archivo con la configuración del DAG para Apache AirFlow.
- **yaml_docker** Configuración auxiliar de Docker.

## Instalación y ejecucción 

Instalación de la imagen de Docker, que contiene Apache Airflow en la terminal del sistema operativo.

```shell
docker pull puckel/docker-airflow
```

Tomar de la carpeta *yaml_docker* el archivo *docker-compose-CeleryExecutor.yml* .

Navegar hasta la ruta donde se haya guardado el archivo *docker-compose-CeleryExecutor.yml*.

```shell
cd C:/.../yaml_docker
```
A continuación ejecutar el siguien comando 
```shell
docker-compose -f docker-compose-CeleryExecutor.yml up -d
```
Iniciar el contenedor de Docker con Airflow

```shell
docker run -d -p 8080:8080 puckel/docker-airflow webserver
```
En caso de de error apagar el contenedor creado creado por *docker-compose-CeleryExecutor.yml*

Y volver ejecutar el comando anterior *docker run*

Una vez en ejecución, acceder a la terminal del contenedor de Docker .

```shell
docker exec -ti <container name> bash
```
Para saber el nombre del contenedor puedes ejecutar el siguiente comando 
```shell
docker ps
```

Posteriormente crear las siguientes carpetas:

```shell
mkdir /usr/local/airflow/dags
mkdir /usr/local/airflow/bin
mkdir /usr/local/airflow/files
mkdir /usr/local/airflow/output
```
Para la ejecución del pipeline intalar las siguientes librerias:

```shell
pip install sklearn
pip install xgboost
pip install pandas
pip install plotly
pip install matplotlib
pip install seaborn
pip install -U kaleido
```

Traansferir los archivos al contenedor de la siguiente forma, desde la maquina local host:

```shell
docker cp C:.../dags/riesgo_crediticio_dag.py <container id>:/usr/local/airflow/dags

docker cp C:.../bin/. <container id>:/usr/local/airflow/bin

docker cp C:.../files/german_credit_data.csv <container id>:/usr/local/airflow/files
```
Para saber el id del contenedor puedes ejecutar el siguiente comando 

```shell
docker ps
```
Para ingresar a la interfaz de Apache Airflow

http://localhost:8080/admin/

## Funcionamiento

Se creo un DAG de Apache Airflow, que lee los datos del archivo fuente, posteriormente genera distintas gráficas que describen el comportamiento de los datos y ejecuta los modelos de riesgo, dando como resultado los datasets con las clasificaciones de acuerdo al modelo.

 ![DAG](https://github.com/garagaby/Kernel-Airflow/blob/main/imagenes_resultado/DAG.PNG)
<p align="center">
Figura 1. DAG
</p>
Para ello el DAG se divide en dos secciones la generación de graficas y ejecucion de modelos, la primera ejecuta distintas task en paralelo, ya que el procesamiendo es ligero generando distintas gráficas de la distribucion de los datos; la segunda ejecuta los modelos de riesgo de manera secuencial, ya que son tareas computacionalmente costosas, dando como resultado un dataset de pandas con la clasificación completa para cada modelo (RandomForest y GaussianNB).


## Resultados

Las gráficas se obtienen en formato PNG y de guardan en la carpeta *output* en el contenedor de Docker, se extraer con el siguiente comando:
 
 ```shell
docker cp <container id>:/usr/local/airflow/output/target_variable_distribution.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/age_distribution.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/age_categorical.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/housing_distribution.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/sex_distribution.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/job_distribution.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/distribution_credit_amont.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/saving_accounts_by_risk.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/data_correlation.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/checking_accounts_distribution.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/checking_distribution.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/credit_amount_by_job.png C:/.../output/
docker cp <container id>:/usr/local/airflow/output/algorithm_comparison.png C:/.../output/
 ```
![Gráficas generadas](https://github.com/garagaby/Kernel-Airflow/blob/main/imagenes_resultado/graficos.PNG)
<p align="center">
Figura 2. Gráficas Generadas
</p>

![Correlación de los datos](https://github.com/garagaby/Kernel-Airflow/blob/main/imagenes_resultado/Data_correlation.PNG)
<p align="center">
Figura 3. Correlación de los datos 
</p>

Los dataset que se generan, se guardan en l carpeta */usr/local/airflow/modelos/*. Y se pueden extraer de la siguiente forma:

```shell
docker cp f4fe8709b67b:/usr/local/airflow/modelos/modelo_1.csv C:/..../modelos/
docker cp f4fe8709b67b:/usr/local/airflow/modelos/modelo_2.csv C:/..../modelos/
```
![csv Modelo 1 (RandomForest)](https://github.com/garagaby/Kernel-Airflow/blob/main/imagenes_resultado/data_set_modelo_1.PNG)
<p align="center">
Figura 4. Dataset Modelo 1 (RandomForest)
</p>

 ![Carpetas en Docker](https://github.com/garagaby/Kernel-Airflow/blob/main/imagenes_resultado/files_Docker.PNG)
<p align="center">
Figura 5. Archivos generados en Docker  
</P>













