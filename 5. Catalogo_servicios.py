# Jerarquía polimórfica de servicios ofrecidos por Software FJ

from abc import ABC, abstractmethod
from nucleo import ElementoCorporativo
from fallos_sistema import ValidacionCampoError


class ServicioBase(ElementoCorporativo, ABC):
    # Clase abstracta que estandariza tarifas, disponibilidad y validación de uso
    def __init__(self, id_registro: str, titulo: str, valor_hora: float):
        super().__init__(id_registro)
        if not isinstance(titulo, str) or len(titulo.strip()) < 4:
            raise ValidacionCampoError("El título del servicio es demasiado corto.")
        if not isinstance(valor_hora, (int, float)) or valor_hora <= 0:
            raise ValidacionCampoError("El valor por hora debe ser un número positivo.")

        self._titulo = titulo.strip()
        self._valor_hora = float(valor_hora)
        self._activo = True

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def valor_hora(self) -> float:
        return self._valor_hora

    @property
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(self, nuevo_estado: bool) -> None:
        self._activo = bool(nuevo_estado)

    @abstractmethod
    def verificar_reglas(self, horas: int) -> None:
        # Comprueba condiciones particulares antes de liquidar el servicio
        pass

    @abstractmethod
    def liquidar_subtotal(self, horas: int) -> float:
        # Calcula el costo base según la lógica propia de cada subclase
        pass

    @abstractmethod
    def detalle_modalidad(self) -> str:
        # Describe las características técnicas del servicio
        pass

    def ficha_tecnica(self) -> str:
        disponibilidad = "Libre" if self.activo else "En uso"
        return f"{self.id_registro} - {self.titulo} (${self.valor_hora:,.0f}/h) [{disponibilidad}]"


class SalaCorporativa(ServicioBase):
    # Servicio de préstamo de espacios físicos equipados
    def __init__(self, id_registro: str, titulo: str, valor_hora: float, aforo_maximo: int, incluye_videoconferencia: bool):
        super().__init__(id_registro, titulo, valor_hora)
        if not isinstance(aforo_maximo, int) or aforo_maximo < 2:
            raise ValidacionCampoError("El aforo mínimo de una sala debe ser de 2 personas.")
        self._aforo_maximo = aforo_maximo
        self._incluye_videoconferencia = bool(incluye_videoconferencia)

    def verificar_reglas(self, horas: int) -> None:
        if not (1 <= horas <= 10):
            raise ValidacionCampoError("Las salas solo se asignan en bloques de 1 a 10 horas.")

    def liquidar_subtotal(self, horas: int) -> float:
        self.verificar_reglas(horas)
        cargo_tecnologico = 25000.0 if self._incluye_videoconferencia else 0.0
        return (self.valor_hora * horas) + cargo_tecnologico

    def detalle_modalidad(self) -> str:
        equipo_av = "con videoconferencia" if self._incluye_videoconferencia else "estándar"
        return f"Sala '{self.titulo}' (Aforo: {self._aforo_maximo}, {equipo_av})"


class EquipoTecnologico(ServicioBase):
    # Servicio de alquiler de estaciones de trabajo o hardware especializado
    def __init__(self, id_registro: str, titulo: str, valor_hora: float, categoria: str):
        super().__init__(id_registro, titulo, valor_hora)
        if categoria.lower() not in ("ofimatica", "desarrollo", "servidor"):
            raise ValidacionCampoError("Categoría inválida. Use: ofimatica, desarrollo o servidor.")
        self._categoria = categoria.lower()

    def verificar_reglas(self, horas: int) -> None:
        if horas < 3:
            raise ValidacionCampoError("El alquiler de hardware exige un mínimo de 3 horas.")

    def liquidar_subtotal(self, horas: int) -> float:
        self.verificar_reglas(horas)
        factores = {"ofimatica": 1.0, "desarrollo": 1.2, "servidor": 1.5}
        return self.valor_hora * horas * factores[self._categoria]

    def detalle_modalidad(self) -> str:
        return f"Hardware '{self.titulo}' [Línea {self._categoria}]"


class ConsultoriaTecnica(ServicioBase):
    # Servicio de acompañamiento experto por sesiones
    def __init__(self, id_registro: str, titulo: str, valor_hora: float, especialidad: str):
        super().__init__(id_registro, titulo, valor_hora)
        if not isinstance(especialidad, str) or len(especialidad.strip()) < 3:
            raise ValidacionCampoError("Debe indicar una especialidad válida para la consultoría.")
        self._especialidad = especialidad.strip()

    def verificar_reglas(self, horas: int) -> None:
        if not (1 <= horas <= 6):
            raise ValidacionCampoError("Las sesiones de consultoría permiten máximo 6 horas continuas.")

    def liquidar_subtotal(self, horas: int) -> float:
        self.verificar_reglas(horas)
        monto = self.valor_hora * horas
        # Bonificación del 12% si la sesión es de 4 horas o más
        if horas >= 4:
            monto *= 0.88
        return monto

    def detalle_modalidad(self) -> str:
        return f"Consultoría en {self._especialidad}: '{self.titulo}'"

