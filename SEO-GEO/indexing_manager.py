import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_PATH = (
    r"C:\Users\micnu\OneDrive\PROYECTOS\AIPRODIG\SEO-GEO\seogeoprodig.json"
)
URLS_FILE = "urls_to_index.txt"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def run_indexing():
    if not os.path.exists(CREDENTIALS_PATH):
        print(
            f"[ERROR] No se encontro el archivo de credenciales en: {CREDENTIALS_PATH}"
        )
        return

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_PATH, SCOPES
    )
    service = build("indexing", "v3", credentials=credentials)

    with open(URLS_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("[INFO] No se encontraron URLs en el archivo.")
        return

    print(f"[INFO] Se procesaran {len(urls)} URLs...\n")

    for url in urls:
        body = {"url": url, "type": "URL_UPDATED"}
        try:
            service.urlNotifications().publish(body=body).execute()
            print(f"[OK] Indexacion exitosa: {url}")
        except Exception as e:
            print(f"[ERROR] Fallo en {url}: {e}")

    print("\n[INFO] Proceso de indexacion finalizado.")


if __name__ == "__main__":
    run_indexing()
