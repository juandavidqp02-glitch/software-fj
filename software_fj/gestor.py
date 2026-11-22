"""Gestor central: listas internas y operaciones tolerantes a fallos."""
from .cliente import Cliente
from .excepciones import SoftwareFJError
from .logger import log
from .reserva import Reserva
from .servicios import Servicio


class GestorFJ:
    def __init__(self) -> None:
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def _crear(self, fabrica, destino: list, etiqueta: str, *args, **kwargs):
        """Crea un objeto; si falla registra el error y el sistema continúa."""
        try:
            obj = fabrica(*args, **kwargs)
        except SoftwareFJError as e:
            log.error("%s inválido: %s", etiqueta, e)
            print(f"   [ERROR controlado] {e}")
            return None
        except Exception as e:  # error inesperado: nunca detiene la aplicación
            log.critical("Error inesperado creando %s: %r", etiqueta, e)
            print(f"   [ERROR inesperado controlado] {e!r}")
            return None
        else:
            destino.append(obj)
            log.info("%s creado: %s", etiqueta, obj.describir())
            print(f"   [OK] {obj.describir()}")
            return obj

    def registrar_cliente(self, *args, **kwargs):
        return self._crear(Cliente, self.clientes, "Cliente", *args, **kwargs)

    def registrar_servicio(self, clase, *args, **kwargs):
        return self._crear(clase, self.servicios, "Servicio", *args, **kwargs)

    def crear_reserva(self, cliente, servicio, horas, descuento=0.0, **extras):
        reserva = self._crear(Reserva, self.reservas, "Reserva",
                              cliente, servicio, horas, **extras)
        if reserva is None:
            return None
        try:
            if reserva.procesar(descuento):
                print(f"   [OK] {reserva.describir()}")
            else:
                print(f"   [FALLIDA] {reserva.describir()}")
        except Exception as e:
            log.critical("Error inesperado procesando reserva: %r", e)
        return reserva

    def cancelar_reserva(self, reserva):
        try:
            reserva.cancelar()
            print(f"   [OK] {reserva.describir()}")
        except SoftwareFJError as e:
            log.error("Cancelación no permitida: %s", e)
            print(f"   [ERROR controlado] {e}")
