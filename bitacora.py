# Módulo de auditoría para registrar eventos y excepciones en archivo plano

from datetime import datetime


class AuditoriaArchivo:
    # Gestiona la persistencia de trazas operativas sin detener el flujo del programa
    def __init__(self, nombre_archivo: str = "auditoria_fj.log"):
        self._ruta = nombre_archivo

    def escribir_evento(self, categoria: str, detalle: str) -> None:
        sello_tiempo = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
        registro = f"{sello_tiempo} | {categoria.upper():<7} | {detalle}\n"
        try:
            with open(self._ruta, mode="a", encoding="utf-8") as flujo:
                flujo.write(registro)
        except OSError as fallo_disco:
            print(f"[ADVERTENCIA] Imposible escribir en bitácora: {fallo_disco}")

    def registrar_exito(self, detalle: str) -> None:
        self.escribir_evento("EXITO", detalle)

    def registrar_alerta(self, detalle: str) -> None:
        self.escribir_evento("ALERTA", detalle)

    def registrar_fallo(self, detalle: str) -> None:
        self.escribir_evento("FALLO", detalle)
