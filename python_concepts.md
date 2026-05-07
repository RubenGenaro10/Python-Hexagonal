# Conceptos de Python

Este documento sirve como una guía de referencia para aprender Python a medida que revisas el código del proyecto. Los conceptos se irán agregando aquí sin repetir lo que ya se ha explicado.

## 1. Clases y Programación Orientada a Objetos (POO)

### Creación de una Clase
En Python, una clase se define usando la palabra clave `class`, seguida del nombre de la clase (por convención en PascalCase, con la primera letra en mayúscula) y dos puntos `:`.

```python
class NombreDeLaClase:
    pass # 'pass' es una palabra reservada para indicar que no hay código aquí aún
```

### El decorador `@dataclass`
En el archivo `src/domain/task.py`, usamos `@dataclass` justo antes de definir la clase `Task`:

```python
from dataclasses import dataclass

@dataclass
class Task:
    ...
```
Un **decorador** (que empieza con `@`) añade funcionalidades extra a una clase o función. El decorador `@dataclass` es muy útil porque genera automáticamente por ti métodos que normalmente tendrías que escribir a mano (como el método para inicializar la clase `__init__`, o métodos para comparar objetos). Es ideal para clases que principalmente almacenan datos.

### Atributos y Tipado Estático (Type Hinting)
A diferencia de otros lenguajes que te obligan a definir el tipo de variable, Python es de tipado dinámico. Sin embargo, en proyectos modernos, se usan las **anotaciones de tipo** para que el código sea más claro y los editores de código puedan ayudarte con autocompletado:

```python
from typing import Optional

    id: Optional[str]
    title: str
    completed: bool = False
```
* **`str`**: Cadena de texto.
* **`bool`**: Valor booleano (`True` o `False`). El `= False` indica que, si no le decimos nada, el valor por defecto será falso.
* **`Optional[str]`**: Importado de la librería `typing`, esto indica que la variable `id` puede ser un texto (`str`) **o** puede ser nula (`None` en Python, equivalente a `null` en otros lenguajes). Esto tiene sentido porque una tarea nueva no tiene un ID hasta que se guarda en la base de datos.

### Métodos y la palabra clave `self`
Las funciones dentro de una clase se conocen como **métodos** y se definen con la palabra reservada `def`.

```python
    def mark_as_completed(self):
        self.completed = True
```
* **`self`**: Es **obligatorio** como primer parámetro en los métodos que pertenecen al objeto. Representa a la instancia actual de la clase (es el equivalente exacto a `this` en lenguajes como Java, C# o JavaScript). 
* Para acceder o modificar las variables del propio objeto, siempre debes usar `self.nombre_variable`.

## 2. Herencia, Interfaces y Tipado de Retorno

### Paréntesis en la definición de una Clase: Herencia
En el archivo `src/application/ports/task_repository.py` vemos la siguiente línea:

```python
class TaskRepository(ABC):
```
Los paréntesis `()` después del nombre de la clase se usan para la **herencia**. Significa que `TaskRepository` está heredando (o basándose en) la clase `ABC`. 

* **¿Qué es `ABC`?** Proviene del módulo `abc` (Abstract Base Classes) que viene incluido en Python. Al heredar de `ABC`, estamos diciendo que esta clase no está hecha para ser instanciada directamente (no puedes crear un objeto a partir de ella), sino que sirve como una "plantilla" o "contrato" (lo que en Arquitectura Hexagonal y otros lenguajes se conoce como una **Interfaz** o un **Puerto**).

### El decorador `@abstractmethod`
Así como vimos `@dataclass` antes, aquí utilizamos el decorador `@abstractmethod`:

```python
    @abstractmethod
    def save(self, task: Task) -> Task:
        pass
```
Este decorador obliga a que cualquier clase "hija" que herede de `TaskRepository` (por ejemplo, un adaptador que guarde en memoria o en base de datos) **tenga que implementar obligatoriamente** el método `save`. El uso de `pass` aquí significa que el método no tiene lógica dentro del puerto; solo estamos definiendo el "contrato" (lo que debe recibir y lo que debe devolver).

### Tipado en Funciones y la flecha `->`
La flecha `->` en la definición de un método se utiliza para indicar (o hacer un *hint*) sobre el **tipo de dato que va a retornar** (devolver) dicha función. 

```python
    def save(self, task: Task) -> Task:
```
* **`task: Task`**: Es el parámetro que recibe la función. Indica que recibe una variable llamada `task` que debe ser obligatoriamente del tipo `Task` (tu entidad).
* **`-> Task`**: Indica que, al terminar su ejecución, este método devolverá un objeto de tipo `Task`.
* **`-> Optional[Task]`**: En otro de tus métodos, significa que puede devolver una tarea o puede no devolver nada (`None` / nulo), como cuando intentas buscar por ID y no existe.
* **`-> List[Task]`**: Significa que la función va a devolver una Lista (arreglo) conformada por objetos de tipo `Task`.

## 3. Constructores, Creación de Atributos y Excepciones

### El método `__init__` y creación de atributos con `self`
En el archivo `src/application/use_cases/task_manager.py` vemos esto:

```python
    def __init__(self, repository: TaskRepository):
        self.repository = repository
```
* **`__init__` (Constructor)**: Es un método especial en Python (nota los dobles guiones bajos `__` al principio y al final, conocidos como "dunder"). Funciona como el **constructor** de la clase y se ejecuta automáticamente cuando creas una nueva instancia de ese objeto. (Nota: en la entidad `Task` no lo tuvimos que escribir a mano porque el decorador `@dataclass` generó este constructor por nosotros).
* **Creación dinámica de Atributos (Comparación con Java)**:
Esta es una diferencia fundamental entre Python y lenguajes como Java o C#. 
En **Java**, necesitas declarar el atributo a nivel de clase ANTES de poder usarlo en el constructor:

```java
public class TaskManagerUseCase {
    private TaskRepository repository; // Declaración estricta previa

    public TaskManagerUseCase(TaskRepository repository) {
        this.repository = repository; // Asignación
    }
}
```

En **Python**, los objetos funcionan internamente de forma muy dinámica (como si fuesen diccionarios). **No declaras los atributos de instancia previamente a nivel de clase**. 
Cuando escribes `self.repository = repository` dentro del `__init__`, Python está haciendo dos cosas a la vez:
1. "Inventa" o **crea** la variable `repository` atada a esa instancia específica en ese preciso instante.
2. Le asigna el valor que venía en el parámetro.

Por lo tanto, en Python no existe la "declaración previa"; declaras el atributo en el momento exacto en que le asignas un valor a `self` dentro del constructor.

### Validaciones lógicas: `if not`
En el método `get_task` vemos:

```python
        if not task:
```
* **`not`**: Invierte la condición (como el `!` en otros lenguajes).
* **Valores "Falsy"**: En Python, ciertos valores se evalúan automáticamente como falsos. Por ejemplo: `None` (nulo), `0`, strings vacíos `""`, listas vacías `[]`, o `False`. Dado que tu repositorio puede devolver un objeto `Task` o `None`, al evaluar `not task`, Python interpreta: "Si `task` es nulo, la condición se cumple y entramos al bloque `if`".

### Manejo de Errores: `raise` y Excepciones Personalizadas
Dentro del mismo `if`, vemos:

```python
            raise TaskNotFoundError(f"Tarea con ID {task_id} no encontrada")
```
* **`raise`**: Es la palabra clave que se utiliza para "lanzar" un error (una excepción). Es el equivalente exacto a `throw new Error()` en lenguajes como JavaScript, Java, PHP o C#. Al lanzar un error, la ejecución normal del código se interrumpe inmediatamente y el error "sube" hasta que alguna otra parte del código lo atrape.
* **Excepciones personalizadas**: `TaskNotFoundError` es una clase que tú creaste en `src/domain/exceptions.py` y que hereda de `Exception`. Es una muy buena práctica crear tus propios errores de Dominio en vez de lanzar errores genéricos, porque te da mayor claridad sobre qué falló exactamente.
* **Strings formateados (`f"..."`)**: La letra `f` antes de las comillas indica que es un texto formateado (f-string). Esto te permite inyectar variables directamente dentro del texto usando llaves `{}`. Es igual que los template literals con comillas invertidas `` ` `` en JS o el prefijo `$` en C#.

## 4. Diccionarios y Generación de IDs (UUID)

En el archivo `src/infrastructure/adapters/out_db/memory_task_repository.py` nos encontramos con nuevos conceptos relacionados con el almacenamiento en memoria.

### Diccionarios y `Dict[]`
En el constructor, inicializamos la variable:
```python
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
```
* **Diccionarios (`{}`)**: En Python, las llaves `{}` se usan para crear **Diccionarios**. Son estructuras de datos que almacenan información en pares de `clave: valor`. Es el equivalente exacto a un **`HashMap`** en Java o un objeto literal en JavaScript.
* **`Dict[str, Task]`**: Esto es Type Hinting. Le estamos diciendo a Python que este diccionario (`self.tasks`) va a usar una cadena de texto (`str`) como llave (clave) y un objeto `Task` como valor. En Java, esto sería idéntico a escribir: `HashMap<String, Task> tasks = new HashMap<>();`.

### Guardar y actualizar datos en un Diccionario
Dentro del método `save`, agregamos la tarea al diccionario así:
```python
        self.tasks[task.id] = task
```
* En Java, para agregar o actualizar un valor en un mapa usarías el método `.put()` (ej: `tasks.put(task.getId(), task);`).
* En Python, la sintaxis directa es usando los corchetes `[]`. Esta línea significa: *"Busca en el diccionario `self.tasks` la llave que corresponda a `task.id`. Si no existe, créala; y a esa llave asígnale el objeto `task` completo"*.

### Generación de IDs únicos (`uuid.uuid4()`) y Casteo (`str`)
Si la tarea es nueva y no tiene ID, le asignamos uno:
```python
        if not task.id:
            task.id = str(uuid.uuid4())
```
* **`uuid.uuid4()`**: El módulo interno `uuid` de Python sirve para generar "Identificadores Únicos Universales" (UUIDs). Específicamente, el método `uuid4()` genera un código único aleatorio muy difícil de repetir (ej: `550e8400-e29b-41d4-a716-446655440000`).
* **`str()` (Casteo)**: La función `uuid4()` devuelve un "objeto de tipo UUID", no un texto puro. Sin embargo, en nuestra clase `Task`, nosotros dijimos que el ID debe ser un `str` (texto). Por lo tanto, usamos la función `str()` para envolver el resultado y "convertir" o castear ese objeto UUID a una cadena de texto plana. 
* Esto en Java sería el equivalente exacto a: `UUID.randomUUID().toString();`

## 5. El Punto de Entrada y la Inversión de Dependencias

En el archivo `src/main.py` es donde ocurre la magia de ensamblar todo nuestro proyecto (el llamado *Composition Root*).

### El bloque `if __name__ == "__main__":`
Al final del archivo encontramos estas líneas:
```python
if __name__ == "__main__":
    main()
```
* **¿Qué significa?** Cuando ejecutas un archivo de Python directamente desde la consola (por ejemplo, escribiendo `python src/main.py`), Python le asigna automáticamente el nombre especial `"__main__"` a la variable global interna `__name__`.
* **¿Para qué sirve?** Si en algún momento otro archivo hiciera un `import src.main`, la variable `__name__` no sería `"__main__"`, sino `"src.main"`. De esa forma, el bloque `if` **no se cumpliría** y el método `main()` no se ejecutaría de forma no deseada. Básicamente, es una medida de seguridad que dice: *"Solo arranca la aplicación si ejecuté este archivo de manera explícita como programa principal"*. Es el equivalente de Python al `public static void main(String[] args)` de Java.

### Inversión de Dependencias y Arquitectura Hexagonal
Dentro de la función `main` observamos lo siguiente:
```python
    repository = MemoryTaskRepository()
    task_manager = TaskManagerUseCase(repository)
```
Aquí aplicamos un concepto clave de la Arquitectura de Software:

* **Inversión de Dependencias (la "D" en los principios SOLID)**: Este principio dicta que los módulos de alto nivel (tu Caso de Uso `TaskManagerUseCase`) no deben depender de los detalles o módulos de bajo nivel (como tu adaptador `MemoryTaskRepository`), sino que **ambos deben depender de abstracciones** (la interfaz `TaskRepository`).
* **¿Cómo lo lograste?** Si revisas el caso de uso, él pide un `TaskRepository` en su constructor, pero él **no sabe** si esos datos se guardarán en memoria, en una base de datos MySQL o en un archivo de texto. Solo sabe que puede llamar a `save()` o `get_by_id()`. 
* **Inyección de Dependencias**: Al crear el objeto `MemoryTaskRepository` aquí afuera en el `main` y luego **"inyectarlo"** (pasarlo por parámetro) al Caso de Uso, estás delegando la responsabilidad de "crear dependencias" al punto más externo de la aplicación (el *Composition Root*). 
* Si mañana decides cambiar tu proyecto para usar una base de datos real, solo tendrías que crear un `SqlTaskRepository`, y cambiarías *una sola línea* en `main.py` (`repository = SqlTaskRepository()`). Tu lógica de negocio en el Caso de Uso permanecería intacta y no se enteraría del cambio. ¡Ese es el poder y el objetivo principal de la Arquitectura Hexagonal!
