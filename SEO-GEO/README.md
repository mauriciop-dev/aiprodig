# Google Indexing API Automation

Script para enviar notificaciones de indexacion a la Google Indexing API usando Service Account.

## Instalacion

```bash
pip install -r requirements.txt
```

## Archivos necesarios

- `seogeoprodig.json` - Credenciales de Google Cloud Service Account
- `urls_to_index.txt` - Lista de URLs a indexar (una por linea)

## Ejecucion

```bash
python indexing_manager.py
```

El script leera las URLs desde `urls_to_index.txt` y enviara notificaciones de tipo `URL_UPDATED` para cada una.