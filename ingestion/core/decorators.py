from functools import wraps
import time
import os

from ingestion.core.logger import get_logger
from ingestion.core.storage import upload_file


def log_execution(name: str):
    """
    Decorador para logar início, fim, erro e tempo de execução.
    Também envia o arquivo de log para o Supabase.
    """

    logger = get_logger(name)

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start_time = time.time()

            logger.info(f"Iniciando {func.__name__}")

            try:
                result = func(*args, **kwargs)

                logger.info(f"Finalizado {func.__name__}")

                return result

            except Exception as e:
                logger.error(
                    f"Erro em {func.__name__}: {e}"
                )
                raise

            finally:
                end_time = time.time()
                duration = round(
                    end_time - start_time,
                    2
                )

                logger.info(
                    f"⏱ Tempo de execução: {duration}s"
                )

                # Garante que os logs sejam escritos no arquivo
                for handler in logger.handlers:
                    handler.flush()

                # Caminho local do arquivo de log
                log_path = logger.log_path

                # Nome do arquivo
                log_filename = os.path.basename(log_path)

                # Caminho dentro do bucket
                storage_path = f"logs/{log_filename}"

                try:
                    upload_file(
                        log_path,
                        storage_path,
                        upsert=True
                    )

                    logger.info(
                        f"Log enviado para o Supabase: "
                        f"{storage_path}"
                    )

                except Exception as e:
                    logger.error(
                        f"Erro ao enviar log para o Supabase: {e}"
                    )

        return wrapper

    return decorator


def retry(times: int = 3, delay: int = 2):
    """
    Decorador para retry automático em casos de falha
    (APIs, scraping instável).
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(1, times + 1):

                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    last_exception = e

                    logger = get_logger(func.__name__)

                    logger.warning(
                        f"⚠️ Tentativa {attempt}/{times} "
                        f"falhou: {e}"
                    )

                    time.sleep(delay)

            logger.error(
                f"Todas as {times} tentativas "
                f"falharam em {func.__name__}"
            )

            raise last_exception

        return wrapper

    return decorator


def throttle(seconds: int):
    """
    Decorador para controle de taxa
    (evita bloqueio em scraping).
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)

            time.sleep(seconds)

            return result

        return wrapper

    return decorator