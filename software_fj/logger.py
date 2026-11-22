"""Configuración del archivo de logs (único uso de archivos del sistema)."""
import logging
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().parent.parent / "logs" / "software_fj.log"


def obtener_logger(nombre: str = "software_fj") -> logging.Logger:
    logger = logging.getLogger(nombre)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    try:
        RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    except OSError:  # si no se puede escribir el archivo, el sistema sigue activo
        handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    return logger


log = obtener_logger()
