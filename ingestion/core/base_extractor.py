import time
import pandas as pd
from datetime import datetime
import os

from ingestion.core import config
from ingestion.core.storage import upload_file


class BaseScraper:

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.data = []

    def log(self, message: str):
        print(f"[{self.source_name}] {message}")

    def save(self, filename: str, df: pd.DataFrame):
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)

        # Garante que o arquivo seja Parquet
        filename = os.path.splitext(filename)[0] + ".parquet"

        # Caminho local
        path = os.path.join(config.OUTPUT_DIR, filename)

        # Salva localmente como Parquet
        df.to_parquet(
            path,
            index=False
        )

        self.log(f"Arquivo salvo localmente em: {path}")

        # Cria nome único para o arquivo no Supabase
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename_without_extension = os.path.splitext(filename)[0]

        storage_filename = (
            f"{filename_without_extension}_"
            f"{timestamp}.parquet"
        )

        # Caminho dentro do bucket
        storage_path = (
            f"construction-price-raw/"
            f"{self.source_name}/"
            f"{storage_filename}"
        )

        # Upload para o Supabase
        try:
            upload_file(
                path,
                storage_path
            )

            self.log(
                f"Arquivo enviado para o Supabase: {storage_path}"
            )

        except Exception as e:
            self.log(
                f"Erro ao enviar arquivo para o Supabase: {e}"
            )

    def add_timestamp(self, row: dict):
        row[config.DATE_FIELD] = datetime.now()
        return row

    def sleep(self):
        time.sleep(config.SLEEP_SECONDS)