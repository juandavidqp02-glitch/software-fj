"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todos los errores del sistema."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos de cliente inválidos o faltantes."""


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros inválidos al crear o usar un servicio."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Reserva mal formada o que no pudo procesarse."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación no válida para el estado actual del objeto."""


class CalculoInconsistenteError(SoftwareFJError):
    """Cálculo de costos con resultados o parámetros inconsistentes."""
