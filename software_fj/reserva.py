"""Clase Reserva: integra cliente, servicio, duración y estado."""
from enum import Enum

from .cliente import Cliente
from .entidades import Entidad
from .excepciones import (OperacionNoPermitidaError, ReservaInvalidaError,
                          ServicioNoDisponibleError, SoftwareFJError)
from .logger import log
from .servicios import Servicio

IVA = 0.19


class Estado(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    FALLIDA = "Fallida"


class Reserva(Entidad):
    def __init__(self, cliente: Cliente = None, servicio: Servicio = None,
                 horas: float = None, **extras) -> None:
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido.")
        if horas is None:
            raise ReservaInvalidaError("Falta la duración de la reserva.")
        self._cliente, self._servicio = cliente, servicio
        self._horas, self._extras = horas, extras
        self._estado = Estado.PENDIENTE
        self._costo_total = None

    @property
    def estado(self) -> Estado:
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self, descuento: float = 0.0) -> float:
        """try/except/else/finally + encadenamiento de excepciones."""
        if self._estado is not Estado.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva {self._estado.value}.")
        try:
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' no está disponible.")
            costo = self._servicio.calcular_costo(self._horas, IVA, descuento,
                                                  **self._extras)
        except ServicioNoDisponibleError:
            raise
        except SoftwareFJError as e:
            raise ReservaInvalidaError(
                f"Reserva #{self.id} no pudo confirmarse: {e}") from e
        else:
            self._costo_total = costo
            self._estado = Estado.CONFIRMADA
            log.info("Reserva #%s CONFIRMADA | %s | %s | %sh | total $%s",
                     self.id, self._cliente.nombre, self._servicio.nombre,
                     self._horas, f"{costo:,.2f}")
            return costo
        finally:
            log.info("Intento de confirmación de reserva #%s finalizado", self.id)

    def cancelar(self) -> None:
        if self._estado is Estado.CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        if self._estado is Estado.FALLIDA:
            raise OperacionNoPermitidaError("No se puede cancelar una reserva fallida.")
        self._estado = Estado.CANCELADA
        log.info("Reserva #%s CANCELADA", self.id)

    def procesar(self, descuento: float = 0.0) -> bool:
        """Procesa la reserva; ante cualquier error la marca como fallida."""
        try:
            self.confirmar(descuento)
            return True
        except SoftwareFJError as e:
            if self._estado is Estado.PENDIENTE:
                self._estado = Estado.FALLIDA
            log.error("Reserva #%s FALLIDA | %s | causa: %r",
                      self.id, e, e.__cause__)
            return False

    def describir(self) -> str:
        costo = f"${self._costo_total:,.2f}" if self._costo_total else "-"
        return (f"Reserva #{self.id} [{self._estado.value}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} ({self._horas}h) total: {costo}")
