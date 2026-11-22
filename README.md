# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Proyecto UNAD · Programación (213023) · Fase 4 · Python 3.9+ · sin bases de datos.

## Ejecución
```bash
python main.py
```
Genera `logs/software_fj.log` con todos los eventos y errores.

## Estructura
| Archivo | Contenido |
|---|---|
| `software_fj/entidades.py` | Clase abstracta `Entidad` |
| `software_fj/cliente.py` | `Cliente` (encapsulación + validaciones) |
| `software_fj/servicios.py` | `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `software_fj/reserva.py` | `Reserva` (confirmar, cancelar, procesar) |
| `software_fj/excepciones.py` | Excepciones personalizadas |
| `software_fj/gestor.py` | Listas internas y operaciones tolerantes a fallos |
| `software_fj/logger.py` | Registro de eventos en archivo |
| `main.py` | Simulación de 14 operaciones válidas e inválidas |

## Conceptos aplicados
- **Abstracción:** `Entidad` y `Servicio` (ABC con métodos abstractos).
- **Herencia y polimorfismo:** tres servicios sobrescriben `validar_parametros`, `calcular_costo_base` y `describir`.
- **Encapsulación:** atributos privados y propiedades con validación en `Cliente`.
- **Sobrecarga:** `calcular_costo(horas)`, `(horas, impuesto)`, `(horas, impuesto, descuento)`.
- **Excepciones:** jerarquía propia, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento (`raise ... from e`).
- **Logs:** cada error y evento relevante queda en `logs/software_fj.log`.

## Integrantes
Juan Quiroz 
