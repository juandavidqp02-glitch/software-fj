"""Clase Cliente con encapsulación y validaciones robustas."""
import re

from .entidades import Entidad
from .excepciones import ClienteInvalidoError

_RE_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(Entidad):
    def __init__(self, nombre: str = None, documento: str = None,
                 correo: str = None, telefono: str = None) -> None:
        super().__init__()
        if None in (nombre, documento, correo, telefono):
            raise ClienteInvalidoError("Parámetros faltantes: se requieren nombre, "
                                       "documento, correo y teléfono.")
        self.__nombre = self._validar_nombre(nombre)
        self.__documento = self._validar_documento(documento)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

    # --- validaciones ---
    @staticmethod
    def _validar_nombre(v) -> str:
        if not isinstance(v, str) or len(v.strip()) < 3 or any(c.isdigit() for c in v):
            raise ClienteInvalidoError(f"Nombre inválido: {v!r}")
        return v.strip().title()

    @staticmethod
    def _validar_documento(v) -> str:
        v = str(v).strip()
        if not v.isdigit() or not 6 <= len(v) <= 12:
            raise ClienteInvalidoError(f"Documento inválido: {v!r} (6 a 12 dígitos)")
        return v

    @staticmethod
    def _validar_correo(v) -> str:
        if not isinstance(v, str) or not _RE_CORREO.match(v.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {v!r}")
        return v.strip().lower()

    @staticmethod
    def _validar_telefono(v) -> str:
        v = str(v).strip()
        if not v.isdigit() or len(v) != 10:
            raise ClienteInvalidoError(f"Teléfono inválido: {v!r} (10 dígitos)")
        return v

    # --- propiedades (encapsulación) ---
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def documento(self) -> str:
        return self.__documento

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        self.__correo = self._validar_correo(valor)

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self.__telefono = self._validar_telefono(valor)

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} (doc. {self.documento}, {self.correo})"
