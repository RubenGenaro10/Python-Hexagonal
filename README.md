# Proyecto de Aprendizaje: Arquitectura Hexagonal en Python

Este es un proyecto diseñado para aprender los conceptos fundamentales de la **Arquitectura Hexagonal** (también conocida como *Puertos y Adaptadores*). Implementa un sencillo Gestor de Tareas (To-Do List) interactuando a través de CLI y guardando en memoria.

## Estructura del Proyecto

La estructura sigue estrictamente los principios de separación de responsabilidades:

```
src/
├── domain/                  # Lógica del Negocio Principal (Entities, Value Objects). No depende de NADA.
│   ├── exceptions.py        # Excepciones propias del dominio
│   └── task.py              # Entidad principal: Tarea
├── application/             # Orquestación y Reglas de la Aplicación. Depende de Domain.
│   ├── ports/               # Interfaces que definen cómo el sistema interactúa con el exterior.
│   │   └── task_repository.py # Puerto secundario (Out): Contrato para persistir tareas.
│   └── use_cases/           # Casos de uso de la app.
│       └── task_manager.py  # Lógica de crear, completar y obtener tareas.
├── infrastructure/          # Detalles de implementación. Depende de Application y Domain.
│   └── adapters/            # Implementaciones concretas de los puertos.
│       ├── in_cli/          # Adaptadores Primarios (Driving): Por donde "entra" la acción.
│       │   └── cli_app.py   # Interfaz de Línea de Comandos.
│       └── out_db/          # Adaptadores Secundarios (Driven): Salida de datos (BD, APIs).
│           └── memory_task_repository.py # Implementación en memoria del puerto TaskRepository.
└── main.py                  # Composition Root. El único lugar donde se ensambla todo.
```

## Conceptos Clave Demostrados

1. **Independencia de Frameworks:** La capa `domain` es puro Python sin librerías externas.
2. **Puertos y Adaptadores:** `TaskRepository` es el **Puerto**, `MemoryTaskRepository` es el **Adaptador**.
3. **Inversión de Dependencias (DIP):** El caso de uso (`TaskManagerUseCase`) depende de una abstracción (`TaskRepository`), no de una implementación concreta.
4. **Composition Root:** `main.py` se encarga de crear las instancias concretas y conectarlas.

## Cómo Ejecutarlo

Desde la raíz del proyecto, ejecuta el script principal como un módulo de Python para resolver correctamente las rutas relativas (`src...`):

```bash
python -m src.main
```

## Curiosidades y Conceptos de Python

### ¿Por qué aparecen carpetas `__pycache__`?
Cuando ejecutas el proyecto (por ejemplo usando el comando anterior), notarás que se crean carpetas llamadas `__pycache__` en varios directorios. Esto **no es un error**. 

Cuando Python importa un módulo (un archivo `.py`), lo compila internamente a un formato intermedio llamado *byte-code* (archivos `.pyc`). Este formato es mucho más rápido de procesar para la máquina. Python guarda estos archivos precompilados dentro de las carpetas `__pycache__` para que las futuras ejecuciones del programa arranquen más rápido. 

*Nota: Como buena práctica, estas carpetas nunca se deben compartir ni subir al control de versiones (Git), por lo que siempre se añaden al archivo `.gitignore`.*

### ¿Por qué hay archivos `__init__.py` vacíos en las carpetas?
Esto es una **buena práctica estándar de Python** y definitivamente no un error de lógica. 

En Python, colocar un archivo `__init__.py` (incluso si está vacío) dentro de una carpeta le indica al intérprete que ese directorio debe ser tratado como un **"paquete"**. 

Gracias a que estas carpetas son paquetes, podemos importar módulos de una carpeta a otra fácilmente usando rutas absolutas, por ejemplo:
`from src.application.use_cases.task_manager import TaskManagerUseCase`

*Nota Técnica: Desde Python 3.3 existen los "Namespace Packages", que permiten importar desde carpetas sin `__init__.py`, pero incluir este archivo sigue siendo la práctica más recomendada para paquetes estándar regulares.*

## Entendiendo Puertos y Adaptadores

La Arquitectura Hexagonal también se conoce formalmente como **"Arquitectura de Puertos y Adaptadores"**. Su objetivo principal es que el "núcleo" de tu aplicación (Domain y Application) sea completamente ajeno a las tecnologías externas (Bases de datos, Interfaces web, APIs externas).

### ¿Qué es un Puerto? (El Contrato)
Piensa en un puerto como un **enchufe en la pared** o un puerto USB en tu computadora. El puerto define una forma específica de conexión y un contrato (*"Si te conectas aquí, debes usar esta forma y recibirás electricidad"*), pero al puerto no le importa qué dispositivo vayas a conectar.

En código, un **Puerto es una Interfaz** (en Python usamos clases abstractas con `ABC`). Define **QUÉ** se necesita hacer, pero nunca dice **CÓMO** se hace.

### ¿Qué es un Adaptador? (La Implementación)
Siguiendo la analogía, el adaptador es **el dispositivo que conectas al enchufe** (una lámpara, un televisor, el cargador de tu celular). El adaptador transforma la electricidad genérica del enchufe en algo útil para el mundo real.

En código, un **Adaptador es la clase real** que implementa la interfaz del Puerto y se encarga de la tecnología específica (SQL, MongoDB, FastAPI, CLI, etc.). Dice el **CÓMO**.

### Ejemplos Prácticos

#### Ejemplo 1: Base de Datos (Adaptador Secundario / de Salida)
Tu aplicación necesita guardar tareas, pero no quiere saber nada de bases de datos para no acoplarse.
*   **El Puerto:** `TaskRepository`. Es una interfaz que dice *"Para trabajar conmigo, debes tener una función llamada `save(task)` y otra `get_by_id(id)`"*.
*   **Adaptador A:** `MemoryTaskRepository` (El que usamos en este proyecto. Guarda en un diccionario).
*   **Adaptador B:** `PostgresTaskRepository` (Se conecta a PostgreSQL usando SQLAlchemy).
*   **Adaptador C:** `MongoTaskRepository` (Se conecta a MongoDB usando PyMongo).
Tu Caso de Uso funciona con cualquiera de los tres sin cambiar ni una sola línea de código, porque solo habla con el Puerto.

#### Ejemplo 2: Interfaz de Usuario (Adaptador Primario / de Entrada)
Queremos que los usuarios puedan crear tareas.
*   **El Puerto:** Formalmente, los puertos siempre son interfaces. En un diseño estricto, aquí existiría una interfaz llamada `TaskManagerInputPort`. Sin embargo, en lenguajes dinámicos como Python, a menudo **el propio Caso de Uso (`TaskManagerUseCase`) actúa como el puerto de entrada** (su API pública es el contrato).
*   **Adaptador A:** `TaskCLI` (El que usamos. Pide datos por la terminal usando `input()`).
*   **Adaptador B:** `FastApiAdapter` (Recibe peticiones HTTP POST, extrae el JSON y llama al caso de uso).
*   **Adaptador C:** `TelegramBotAdapter` (Recibe mensajes de chat y llama al mismo caso de uso).
Tu aplicación central no sabe si le habla un humano por consola o un servidor web; solo recibe datos y devuelve resultados.

#### Ejemplo 3: Envío de Correos (Adaptador Secundario / de Salida)
Imagínate que al completar una tarea quieres enviar un email.
*   **El Puerto:** `EmailSenderPort` (Interfaz con el método `send_email(to, subject, body)`).
*   **Adaptador A:** `MailchimpAdapter` (Usa la API de Mailchimp).
*   **Adaptador B:** `AWS_SES_Adapter` (Usa Amazon Web Services).
Si mañana cambias de proveedor de correos porque Amazon es muy caro, solo creas un nuevo Adaptador; la lógica de tu aplicación jamás se toca.
