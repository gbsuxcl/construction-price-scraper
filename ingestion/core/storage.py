from supabase import create_client

from ingestion.core.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    SUPABASE_BUCKET,
)


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)


def upload_file(
    file_path: str,
    storage_path: str,
    upsert: bool = False
):
    with open(file_path, "rb") as file:
        return supabase.storage.from_(
            SUPABASE_BUCKET
        ).upload(
            storage_path,
            file.read(),
            file_options={
                "upsert": str(upsert).lower()
            }
        )