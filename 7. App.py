# Controlador principal y ejecución de escenario de pruebas de Software FJ

from fallos_sistema import ErrorAplicacionFJ, ValidacionCampoError, TransicionEstadoError
from bitacora import AuditoriaArchivo
from nucleo import UsuarioCliente
from catalogo_servicios import ServicioBase, SalaCorporativa, EquipoTecnologico, ConsultoriaTecnica
from operaciones_reserva import SolicitudReserva


class GestorPlataformaFJ:
    # Administra las colecciones en memoria y controla las transacciones del sistema
    def __init__(self, bitacora: AuditoriaArchivo):
        self._bitacora = bitacora
        self._usuarios: list[UsuarioCliente] = []
        self._catalogo: list[ServicioBase] = []
        self._solicitudes: list[SolicitudReserva] = []

    def alta_usuario(self, usuario: UsuarioCliente) -> bool:
        try:
            if any(u.id_registro == usuario.id_registro or u.documento == usuario.documento for u in self._usuarios):
                raise ValidacionCampoError(f"Duplicidad detectada para el usuario '{usuario.id_registro}'.")
            self._usuarios.append(usuario)
        except ErrorAplicacionFJ as err:
            self._bitacora.registrar_fallo(f"Fallo en alta de usuario: {err}")
            return False
        else:
            self._bitacora.registrar_exito(f"Usuario incorporado: {usuario.ficha_tecnica()}")
            return True

    def alta_servicio(self, servicio: ServicioBase) -> bool:
        try:
            if any(s.id_registro == servicio.id_registro for s in self._catalogo):
                raise ValidacionCampoError(f"El código de servicio '{servicio.id_registro}' ya está registrado.")
            self._catalogo.append(servicio)
        except ErrorAplicacionFJ as err:
            self._bitacora.registrar_fallo(f"Fallo en alta de servicio: {err}")
            return False
        else:
            self._bitacora.registrar_exito(f"Servicio incorporado: {servicio.ficha_tecnica()}")
            return True

    def _obtener_usuario(self, id_usuario: str) -> UsuarioCliente:
        for u in self._usuarios:
            if u.id_registro == id_usuario.upper():
                return u
        raise ValidacionCampoError(f"Usuario '{id_usuario}' no encontrado en memoria.")

    def _obtener_servicio(self, id_servicio: str) -> ServicioBase:
        for s in self._catalogo:
            if s.id_registro == id_servicio.upper():
                return s
        raise ValidacionCampoError(f"Servicio '{id_servicio}' no encontrado en el catálogo.")

    def ejecutar_reserva(
        self,
        id_reserva: str,
        id_usuario: str,
        id_servicio: str,
        horas: int,
        iva: float = 0.19,
        descuento: float = 0.0,
        recargo: float = 0.0,
    ) -> SolicitudReserva | None:
        solicitud_final = None
        try:
            cliente = self._obtener_usuario(id_usuario)
            servicio = self._obtener_servicio(id_servicio)
            solicitud = SolicitudReserva(id_reserva, cliente, servicio, horas)
            solicitud.aprobar(iva=iva, porcentaje_descuento=descuento, recargo_fijo=recargo)
            self._solicitudes.append(solicitud)
            solicitud_final = solicitud
        except ErrorAplicacionFJ as err:
            # Encadenamiento de excepciones preservando el origen del problema
            try:
                raise TransicionEstadoError(f"Transacción abortada en solicitud '{id_reserva}'") from err
            except TransicionEstadoError as error_encadenado:
                self._bitacora.registrar_fallo(f"{error_encadenado} -> Motivo: {error_encadenado.__cause__}")
        else:
            self._bitacora.registrar_exito(f"Reserva aprobada: {solicitud_final.ficha_tecnica()}")
        finally:
            self._bitacora.registrar_alerta(f"Auditoría cerrada para intento de reserva '{id_reserva}'.")

        return solicitud_final

    def anular_reserva(self, id_reserva: str) -> bool:
        try:
            hallada = next((r for r in self._solicitudes if r.id_registro == id_reserva.upper()), None)
            if hallada is None:
                raise ValidacionCampoError(f"No existe la solicitud '{id_reserva}'.")
            hallada.anular()
        except ErrorAplicacionFJ as err:
            self._bitacora.registrar_fallo(f"Imposible anular solicitud: {err}")
            return False
        else:
            self._bitacora.registrar_exito(f"Solicitud anulada correctamente: {id_reserva.upper()}")
            return True


def iniciar_pruebas() -> None:
    bitacora = AuditoriaArchivo("auditoria_fj.log")
    plataforma = GestorPlataformaFJ(bitacora)
    print("=== PLATAFORMA OPERATIVA SOFTWARE FJ ===\n")

    # Operaciones 1 y 2: Alta exitosa de clientes
    try:
        u1 = UsuarioCliente("USR-01", "valeria rojas", "vrojas@innovacion.co", "1052398412")
        u2 = UsuarioCliente("USR-02", "mateo cardenas", "mcardenas@empresa.com", "79456123")
        plataforma.alta_usuario(u1)
        plataforma.alta_usuario(u2)
        print("[1-2] Clientes registrados correctamente.")
    except ErrorAplicacionFJ as e:
        bitacora.registrar_fallo(str(e))

    # Operación 3: Alta fallida por nombre sin apellido y correo inválido
    try:
        u_err = UsuarioCliente("USR-03", "Sofía", "sofia_correo_malo", "123")
        plataforma.alta_usuario(u_err)
    except ErrorAplicacionFJ as e:
        bitacora.registrar_fallo(f"Rechazo en creación de usuario: {e}")
        print(f"[3]   Error controlado en cliente inválido: {e}")

    # Operaciones 4, 5 y 6: Creación exitosa de los 3 tipos de servicios
    try:
        srv1 = SalaCorporativa("SRV-A1", "Sala Juntas Norte", 75000, aforo_maximo=12, incluye_videoconferencia=True)
        srv2 = EquipoTecnologico("SRV-B2", "Clúster GPU", 60000, categoria="servidor")
        srv3 = ConsultoriaTecnica("SRV-C3", "Migración Nube", 130000, especialidad="DevOps")
        plataforma.alta_servicio(srv1)
        plataforma.alta_servicio(srv2)
        plataforma.alta_servicio(srv3)
        print("[4-6] Catálogo de 3 servicios especializados cargado.")
    except ErrorAplicacionFJ as e:
        bitacora.registrar_fallo(str(e))

    # Operación 7: Creación fallida de servicio por categoría no permitida
    try:
        srv_err = EquipoTecnologico("SRV-B9", "Tablet Básica", 20000, categoria="gamer")
        plataforma.alta_servicio(srv_err)
    except ErrorAplicacionFJ as e:
        bitacora.registrar_fallo(f"Rechazo en creación de servicio: {e}")
        print(f"[7]   Error controlado en servicio inválido: {e}")

    # Operación 8: Reserva exitosa de sala corporativa
    res1 = plataforma.ejecutar_reserva("SOL-001", "USR-01", "SRV-A1", horas=3)
    if res1:
        print(f"[8]   {res1.ficha_tecnica()}")

    # Operación 9: Intento fallido de reservar sala ocupada
    res2 = plataforma.ejecutar_reserva("SOL-002", "USR-02", "SRV-A1", horas=2)
    if not res2:
        print("[9]   Error controlado: sala ocupada no permitió doble reserva.")

    # Operación 10: Reserva exitosa de consultoría con descuento, IVA y recargo fijo (sobrecarga)
    res3 = plataforma.ejecutar_reserva("SOL-003", "USR-02", "SRV-C3", horas=4, iva=0.19, descuento=0.05, recargo=10000)
    if res3:
        print(f"[10]  {res3.ficha_tecnica()}")

    # Operación 11: Intento fallido de alquiler de hardware por menos de 3 horas
    res4 = plataforma.ejecutar_reserva("SOL-004", "USR-01", "SRV-B2", horas=2)
    if not res4:
        print("[11]  Error controlado: hardware exige mínimo 3 horas.")

    # Operaciones 12 y 13: Anulación de reserva y nueva asignación del recurso liberado
    if plataforma.anular_reserva("SOL-001"):
        print("[12]  Solicitud SOL-001 anulada; sala liberada.")
        res5 = plataforma.ejecutar_reserva("SOL-005", "USR-02", "SRV-A1", horas=2, iva=0.0)
        if res5:
            print(f"[13]  {res5.ficha_tecnica()}")

    print("\n=== SIMULACIÓN COMPLETADA SIN INTERRUPCIONES ===")
    print("Revise el archivo 'auditoria_fj.log' para verificar el registro detallado.")


if __name__ == "__main__":
    iniciar_pruebas()
