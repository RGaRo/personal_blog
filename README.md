# Proyecto Django con Docker

Este proyecto utiliza Docker y Docker Compose para facilitar el despliegue y desarrollo de una aplicación Django con base de datos SQLite.


## Requisitos

- Docker
- Docker Compose


## Configuración

1. Copia el archivo `.env.example` a `.env` y ajusta las variables según tus necesidades.

2. Asegúrate de tener los siguientes archivos en la raíz del proyecto:

- `Dockerfile`
- `docker-compose.yml`
- `entrypoint.sh`


## Construir y levantar los contenedores

Para construir las imágenes sin usar caché y levantar los servicios en segundo plano, ejecuta:
```bash
docker compose build --no-cache && docker compose up -d
```

## Acceso a la aplicación

Una vez que los contenedores estén corriendo, abre tu navegador y navega a:
```bash
http://localhost:8000
```

## Logs

Para ver los logs del contenedor web:
```bash
docker-compose logs -f web
```
Para detener los contenedores:
```bash
docker-compose down
```

## Notas

- El contenedor ejecuta migraciones y recolecta archivos estáticos automáticamente al iniciar.
- La base de datos SQLite se persiste en un volumen para mantener los datos entre reinicios.
