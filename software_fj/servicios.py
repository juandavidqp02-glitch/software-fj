"""Clase abstracta Servicio y tres servicios especializados."""
from abc import abstractmethod

from .entidades import Entidad
from .excepciones import CalculoInconsistenteError, ServicioInvalidoError


class Servicio(Entidad):
    """Abstracción de un servicio ofrecido por Software FJ."""

    def __init__(self, nombre: str = None, tarifa_hora: float = None,
                 disponible: bool = True) -> None:
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio requiere un nombre válido.")
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool) \
                or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r}")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self.disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    # --- métodos abstractos (se sobrescriben en cada servicio) ---
    @abstractmethod
    def validar_parametros(self, horas: float, **extras) -> None:
        """Valida duración y parámetros propios del servicio."""

    @abstractmethod
    def calcular_costo_base(self, horas: float, **extras) -> float:
        """Costo sin impuestos ni descuentos."""

    @abstractmethod
    def describir(self) -> str:
        ...

    # --- sobrecarga simulada: calcular_costo(horas) / (horas, impuesto) /
    #     (horas, impuesto, descuento) ---
    def calcular_costo(self, horas: float, *args, **extras) -> float:
        """Variantes:
        - calcular_costo(horas)                       -> costo base
        - calcular_costo(horas, impuesto)             -> base + impuesto
        - calcular_costo(horas, impuesto, descuento)  -> (base - descuento) + impuesto
        """
        if len(args) > 2:
            raise CalculoInconsistenteError("Demasiados parámetros para calcular_costo.")
        impuesto = args[0] if len(args) >= 1 else 0.0
        descuento = args[1] if len(args) == 2 else 0.0
        for nombre, v in (("impuesto", impuesto), ("descuento", descuento)):
            if not isinstance(v, (int, float)) or not 0 <= v <= 1:
                raise CalculoInconsistenteError(f"{nombre} fuera de rango [0,1]: {v!r}")
        self.validar_parametros(horas, **extras)
        base = self.calcular_costo_base(horas, **extras)
        if base <= 0:
            raise CalculoInconsistenteError(f"Costo base inconsistente: {base}")
        neto = base * (1 - descuento)
        return round(neto * (1 + impuesto), 2)

    @staticmethod
    def _validar_horas(horas, maximo: float) -> None:
        if not isinstance(horas, (int, float)) or isinstance(horas, bool) \
                or not 0 < horas <= maximo:
            raise ServicioInvalidoError(f"Duración inválida: {horas!r} (0 < h <= {maximo})")


class ReservaSala(Servicio):
    def __init__(self, nombre=None, tarifa_hora=None, capacidad: int = None,
                 disponible: bool = True) -> None:
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, horas, **extras) -> None:
        self._validar_horas(horas, 12)
        asistentes = extras.get("asistentes", 1)
        if not isinstance(asistentes, int) or not 1 <= asistentes <= self._capacidad:
            raise ServicioInvalidoError(
                f"Asistentes {asistentes!r} exceden la capacidad ({self._capacidad}).")

    def calcular_costo_base(self, horas, **extras) -> float:
        return self._tarifa_hora * horas

    def describir(self) -> str:
        return (f"Sala '{self.nombre}' - capacidad {self._capacidad} personas, "
                f"${self._tarifa_hora:,.0f}/h")


class AlquilerEquipo(Servicio):
    SEGURO = 0.05

    def __init__(self, nombre=None, tarifa_hora=None, tipo_equipo: str = None,
                 disponible: bool = True) -> None:
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El alquiler requiere un tipo de equipo.")
        self._tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, horas, **extras) -> None:
        self._validar_horas(horas, 72)

    def calcular_costo_base(self, horas, **extras) -> float:
        return self._tarifa_hora * horas * (1 + self.SEGURO)  # incluye seguro

    def describir(self) -> str:
        return (f"Equipo '{self.nombre}' ({self._tipo_equipo}) - "
                f"${self._tarifa_hora:,.0f}/h + seguro {self.SEGURO:.0%}")


class AsesoriaEspecializada(Servicio):
    NIVELES = {"junior": 1.0, "senior": 1.5}

    def __init__(self, nombre=None, tarifa_hora=None, especialidad: str = None,
                 nivel: str = "junior", disponible: bool = True) -> None:
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La asesoría requiere una especialidad.")
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r}")
        self._especialidad, self._nivel = especialidad.strip(), nivel

    def validar_parametros(self, horas, **extras) -> None:
        self._validar_horas(horas, 8)

    def calcular_costo_base(self, horas, **extras) -> float:
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self) -> str:
        return (f"Asesoría '{self.nombre}' en {self._especialidad} "
                f"(nivel {self._nivel}) - ${self._tarifa_hora:,.0f}/h")
