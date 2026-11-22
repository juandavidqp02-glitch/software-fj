"""Simulación de 12 operaciones (válidas e inválidas) de Software FJ."""
from software_fj.gestor import GestorFJ
from software_fj.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from software_fj.logger import RUTA_LOG
from software_fj.reserva import IVA


def paso(n: int, texto: str) -> None:
    print(f"\n{n:>2}. {texto}")


def main() -> None:
    g = GestorFJ()

    paso(1, "Cliente válido")
    ana = g.registrar_cliente("Ana Pérez", "1043567890", "ana@correo.com", "3001234567")
    paso(2, "Cliente inválido (correo mal formado)")
    g.registrar_cliente("Luis Gómez", "1098765432", "luis#correo", "3109876543")
    paso(3, "Cliente inválido (parámetros faltantes)")
    g.registrar_cliente("Marta Ruiz")
    paso(4, "Cliente válido")
    carlos = g.registrar_cliente("Carlos Díaz", "72345678", "carlos@mail.co", "3205551234")

    paso(5, "Servicio válido: sala de reuniones")
    sala = g.registrar_servicio(ReservaSala, "Sala Innovación", 80000, capacidad=10)
    paso(6, "Servicio inválido: tarifa negativa")
    g.registrar_servicio(AlquilerEquipo, "Portátil Pro", -5000, tipo_equipo="Laptop")
    paso(7, "Servicios válidos: equipo y asesoría")
    equipo = g.registrar_servicio(AlquilerEquipo, "Videobeam 4K", 25000, tipo_equipo="Proyector")
    asesoria = g.registrar_servicio(AsesoriaEspecializada, "Arquitectura Cloud", 120000,
                                    especialidad="Cloud", nivel="senior")

    paso(8, "Reserva exitosa (sala, 3h, 6 asistentes)")
    r1 = g.crear_reserva(ana, sala, 3, asistentes=6)
    paso(9, "Reserva fallida (excede la capacidad de la sala)")
    g.crear_reserva(carlos, sala, 2, asistentes=25)
    paso(10, "Reserva con descuento 10% (asesoría senior, 2h)")
    g.crear_reserva(carlos, asesoria, 2, descuento=0.10)
    paso(11, "Reserva fallida (servicio no disponible)")
    equipo.disponible = False
    g.crear_reserva(ana, equipo, 5)
    paso(12, "Reserva fallida (descuento inconsistente de 150%)")
    equipo.disponible = True
    g.crear_reserva(ana, equipo, 5, descuento=1.5)
    paso(13, "Cancelar reserva y volver a cancelar (operación no permitida)")
    g.cancelar_reserva(r1)
    g.cancelar_reserva(r1)
    paso(14, "Reserva con cliente nulo (dato inválido)")
    g.crear_reserva(None, sala, 1)

    print("\n--- Sobrecarga de calcular_costo (sala, 4h) ---")
    print(f"  solo base:              ${sala.calcular_costo(4):,.2f}")
    print(f"  con IVA {IVA:.0%}:           ${sala.calcular_costo(4, IVA):,.2f}")
    print(f"  con IVA y 10% dscto:    ${sala.calcular_costo(4, IVA, 0.10):,.2f}")

    print("\n--- Resumen ---")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | "
          f"Reservas: {len(g.reservas)}")
    for r in g.reservas:
        print("  ", r.describir())
    print(f"\nEl sistema terminó sin interrupciones. Log en: {RUTA_LOG}")


if __name__ == "__main__":
    main()
