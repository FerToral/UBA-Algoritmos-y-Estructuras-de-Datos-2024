# Algoritmos y Estructuras de Datos — UBA

Prácticas de laboratorio de la cursada 2024 de Algoritmos y Estructuras de Datos, Facultad de Ciencias Exactas y Naturales, Universidad de Buenos Aires. Los talleres recorren introducción a Java, programación orientada a objetos, aliasing, colecciones, depuración y árboles binarios de búsqueda.

## Talleres

| Taller | Contenido                                                   | Proyecto                                             |
| ------ | ----------------------------------------------------------- | ---------------------------------------------------- |
| 1      | Funciones y estructuras básicas de Java                     | [Introducción a Java](Talleres/01-Introduccion-Java) |
| 2      | Arreglos redimensionables, recordatorios, agenda y aliasing | [POO y aliasing](Talleres/02-POO-y-Aliasing)         |
| 3      | Depuración y cobertura de código                            | [Debugging](Talleres/03-Debugging)                   |
| 4      | Lista doblemente enlazada e iteradores                      | [Listas enlazadas](Talleres/04-Listas-Enlazadas)     |
| 5      | Conjuntos, ABB, eliminación y recorrido ordenado            | [Árboles binarios](Talleres/05-Arboles-Binarios)     |

Cada taller conserva su proyecto Maven y sus pruebas. El `pom.xml` de la raíz permite ejecutarlos juntos; no fusiona sus clases ni paquetes.

## Compilar y probar

Requisitos: JDK y Maven, con `JAVA_HOME` configurado hacia el JDK. Comprobado con **JDK 21.0.3 y Maven 3.9.16**; los proyectos conservan su configuración de compilación Java 8.

Desde la raíz:

```sh
mvn test
```

Para ejecutar solamente un taller:

```sh
mvn -pl Talleres/05-Arboles-Binarios test
```

La primera ejecución puede descargar dependencias de Maven. Los resultados se escriben dentro de `target/surefire-reports` de cada taller y el informe JaCoCo en `target/site/jacoco/index.html`. Esos archivos son generados, no forman parte de las fuentes.

La comprobación actual ejecuta **75 pruebas**: 70 ya existentes y cinco regresiones del ABB. Las nuevas verifican el conjunto vacío, la eliminación del último elemento, la eliminación de una raíz con sucesor no trivial, duplicados y 2000 operaciones reproducibles contrastadas con `TreeSet`. El iterador vacío devuelve `haySiguiente() == false`; el recorrido agotado conserva la excepción `NoSuchElementException`. Las pruebas propias no equivalen a una aprobación docente.

## Material y alcance

Estas implementaciones son trabajo de estudio de Fernando Toralez sobre interfaces, ejercicios y pruebas de la materia; no se atribuyen al alumno las consignas ni las plantillas docentes. El repositorio reúne los talleres Java y el TP1 académico, no todas las guías teóricas de la cursada.

## Trabajo práctico de especificación

[TP1 · Fondo Monetario Común](Trabajos-Practicos/01-Especificacion-WP):
contratos, recursos/redistribución, trayectorias, decisiones de cooperación,
apuestas y demostración con WP. Trabajo grupal con Juan Pablo Otero,
revisado sobre la versión3 del 1C2024. Incluye LaTeX autocontenido y un
verificador auxiliar con racionales exactos.

El trabajo práctico de SIU tiene su repositorio e historia independientes: [AED — TP2](https://github.com/FerToral/AED-tp2-dise-o-e-implementacion-de-estructuras). Su acceso depende de los permisos del repositorio. No se incorporan aquí laboratorios C++ de Algo1, proyectos de Introducción a la Programación, notebooks ITBA ni prácticas de Codo a Codo.

Los nombres históricos de los directorios y las versiones anteriores permanecen en el historial Git. La organización actual sigue el orden de los talleres sin sustituir soluciones posteriores por copias antiguas.
