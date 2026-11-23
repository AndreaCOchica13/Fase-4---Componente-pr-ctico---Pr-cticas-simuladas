# Clases fundamentales del dominio: entidad abstracta y gestión encapsulada de usuarios

from abc import ABC, abstractmethod
from fallos_sistema import ValidacionCampoError


class ElementoCorporativo(ABC):
    # Clase abstracta base que garantiza identificación única y representación textual
    def __init__(self, id_registro: str):
        if not isinstance(id_registro, str) or len(id_registro.strip()) < 3:
            raise ValidacionCampoError("El identificador debe tener al menos 3 caracteres.")
        self._id_registro = id_registro.strip().upper()

    @property
    def id_registro(self) -> str:
        return self._id_registro

    @abstractmethod
    def ficha_tecnica(self) -> str:
        # Contrato obligatorio para generar resumen legible de cada objeto
        pass


class UsuarioCliente(ElementoCorporativo):
    # Entidad que encapsula la información del cliente con validación en cada propiedad
    def __init__(self, id_registro: str, nombre_completo: str, email: str, documento: str):
        super().__init__(id_registro)
        self.nombre_completo = nombre_completo
        self.email = email
        self.documento = documento

    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, dato: str) -> None:
        if not isinstance(dato, str) or len(dato.strip().split()) < 2:
            raise ValidacionCampoError("Debe ingresar nombre y apellido del cliente.")
        self._nombre_completo = dato.strip().title()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, dato: str) -> None:
        if not isinstance(dato, str) or "@" not in dato or not dato.endswith((".com", ".co", ".org", ".net", ".edu")):
            raise ValidacionCampoError(f"Dirección de correo no admitida: '{dato}'.")
        self._email = dato.strip().lower()

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, dato: str) -> None:
        if not isinstance(dato, str) or not dato.isdigit() or not (6 <= len(dato) <= 12):
            raise ValidacionCampoError("El documento debe tener entre 6 y 12 dígitos numéricos.")
        self._documento = dato

    def ficha_tecnica(self) -> str:
        return f"Usuario [{self.id_registro}] {self.nombre_completo} | Doc: {self.documento} | Mail: {self.email}"
