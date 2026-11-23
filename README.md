# Fase-4---Componente-pr-ctico---Pr-cticas-simuladas
Sistema de gestión de reservas, alquiler de equipos y asesorías desarrollado en Python sin bases de datos, con registro de errores en archivo de texto.


# Plataforma Integral de Gestión - Software FJ
**Programa:** Ingeniería de Sistemas - UNAD  
**Curso:** Programación (Código: 213023) - Componente Práctico  

## Descripción
Aplicación desarrollada en Python aplicando Programación Orientada a Objetos (abstracción, herencia, polimorfismo y encapsulación) junto con manejo avanzado de excepciones (`try/except/else/finally`, excepciones personalizadas y encadenamiento). El sistema administra clientes, catálogo de servicios y reservas en memoria sin uso de motores de bases de datos, registrando cada evento y error en un archivo de auditoría `.log`.

## Estructura del proyecto
* `fallos_sistema.py`: Jerarquía de excepciones personalizadas (`ErrorAplicacionFJ`, `ValidacionCampoError`, `RecursoOcupadoError`, `TransicionEstadoError`, `LiquidacionTarifaError`).
* `bitacora.py`: Clase `AuditoriaArchivo` para el registro cronológico de eventos y errores en `auditoria_fj.log`.
* `nucleo.py`: Clase abstracta `ElementoCorporativo` y clase `UsuarioCliente` con encapsulación y validaciones estrictas.
* `catalogo_servicios.py`: Clase abstracta `ServicioBase` y subclases polimórficas (`SalaCorporativa`, `EquipoTecnologico`, `ConsultoriaTecnica`).
* `operaciones_reserva.py`: Clase `SolicitudReserva` con gestión de estados y cálculo de montos con parámetros opcionales.
* `app.py`: Controlador principal (`GestorPlataformaFJ`) y ejecución automatizada de 13 operaciones completas.

## Ejecución
1. Descargar todos los archivos `.py` en un mismo directorio.
2. Ejecutar desde la terminal o entorno de desarrollo:
   ```bash
   python app.py
   ```
3. Revisar los resultados en consola y el archivo `auditoria_fj.log` generado en la carpeta del proyecto.
