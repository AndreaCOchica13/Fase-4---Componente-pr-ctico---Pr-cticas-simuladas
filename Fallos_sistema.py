# Definición de jerarquía propia de excepciones para control de fallos en Software FJ

class ErrorAplicacionFJ(Exception):
    # Excepción raíz de toda la plataforma
    pass


class ValidacionCampoError(ErrorAplicacionFJ):
    # Error disparado ante parámetros vacíos, nulos o fuera de formato
    pass


class RecursoOcupadoError(ErrorAplicacionFJ):
    # Error disparado cuando se intenta asignar un servicio que ya está en uso
    pass


class TransicionEstadoError(ErrorAplicacionFJ):
    # Error disparado al intentar confirmar o anular una solicitud en un estado inválido
    pass


class LiquidacionTarifaError(ErrorAplicacionFJ):
    # Error disparado si los porcentajes o montos financieros son incoherentes
    pass
