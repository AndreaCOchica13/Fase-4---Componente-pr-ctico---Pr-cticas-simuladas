# Gestión de solicitudes de reserva, estados y sobrecarga funcional de liquidación

from nucleo import ElementoCorporativo, UsuarioCliente
from catalogo_servicios import ServicioBase
from fallos_sistema import (
    ValidacionCampoError,
    RecursoOcupadoError,
    TransicionEstadoError,
    LiquidacionTarifaError,
)


class SolicitudReserva(ElementoCorporativo):
    # Vincula un cliente con un servicio durante un tiempo determinado
    def __init__(self, id_registro: str, cliente: UsuarioCliente, servicio: ServicioBase, horas: int):
        super().__init__(id_registro)
        if not isinstance(cliente, UsuarioCliente):
            raise ValidacionCampoError("El titular de la reserva debe ser un UsuarioCliente válido.")
        if not isinstance(servicio, ServicioBase):
            raise ValidacionCampoError("El objeto asociado debe ser un ServicioBase válido.")
        if not isinstance(horas, int) or horas <= 0:
            raise ValidacionCampoError("La cantidad de horas debe ser un entero mayor a cero.")

        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "CREADA"
        self._valor_neto = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def valor_neto(self) -> float:
        return self._valor_neto

    def calcular_monto(self, iva: float = 0.0, porcentaje_descuento: float = 0.0, recargo_fijo: float = 0.0) -> float:
        # Método con parámetros opcionales (sobrecarga) para liquidar con impuestos, descuentos o cargos extra
        if iva < 0 or porcentaje_descuento < 0 or porcentaje_descuento >= 1 or recargo_fijo < 0:
            raise LiquidacionTarifaError("Parámetros financieros fuera de rango permitido.")

        subtotal = self._servicio.liquidar_subtotal(self._horas)
        tras_descuento = subtotal * (1 - porcentaje_descuento)
        con_impuesto = tras_descuento * (1 + iva)
        total = con_impuesto + recargo_fijo

        if total <= 0:
            raise LiquidacionTarifaError("La liquidación produjo un monto inválido.")
        return round(total, 2)

    def aprobar(self, iva: float = 0.19, porcentaje_descuento: float = 0.0, recargo_fijo: float = 0.0) -> None:
        # Valida disponibilidad, calcula el total y bloquea el servicio
        if self._estado != "CREADA":
            raise TransicionEstadoError(f"La solicitud {self.id_registro} no puede aprobarse desde estado '{self._estado}'.")
        if not self._servicio.activo:
            raise RecursoOcupadoError(f"El servicio '{self._servicio.titulo}' no está disponible.")

        self._valor_neto = self.calcular_monto(iva=iva, porcentaje_descuento=porcentaje_descuento, recargo_fijo=recargo_fijo)
        self._servicio.activo = False
        self._estado = "APROBADA"

    def anular(self) -> None:
        # Anula la solicitud y libera el recurso si ya había sido aprobado
        if self._estado == "ANULADA":
            raise TransicionEstadoError(f"La solicitud {self.id_registro} ya fue anulada previamente.")
        if self._estado == "APROBADA":
            self._servicio.activo = True
        self._estado = "ANULADA"

    def ficha_tecnica(self) -> str:
        return (
            f"Solicitud [{self.id_registro}] | Cliente: {self._cliente.nombre_completo} | "
            f"{self._servicio.detalle_modalidad()} ({self._horas}h) | "
            f"Estado: {self._estado} | Total: ${self._valor_neto:,.2f}"
        )
