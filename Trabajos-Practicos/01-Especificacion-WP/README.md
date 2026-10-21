# TP1 · Fondo Monetario Común

Especificación y correctitud de un juego de apuestas con redistribución.
Trabajo grupal de **Juan Pablo Otero y Fernando Toralez**, cursada 1C2024
de Algoritmos y Estructuras de Datos, Exactas UBA.

## Recorrido

1. Redistribuir el fondo entre todos los individuos.
2. Construir la trayectoria de recursos tras cada apuesta y reparto.
3. Reconocer una trayectoria con un único máximo local estricto.
4. Elegir si cooperar según los recursos finales.
5. Actualizar sólo la apuesta del individuo elegido.
6. Demostrar el algoritmo individual mediante WP, invariante y variante.

[PDF](Fondo-Monetario-Comun.pdf) · [fuente LaTeX](main.tex) · [modelo racional](comprobacion/modelo.py)
· [comprobaciones](comprobacion/test_modelo.py).

La fuente de referencia es la
[consigna versión 3, 08/04/2024](https://github.com/SashaBerkowsky/AyED-II/blob/42722b4636a1e8e3550f9c6500d3e3ed61e67792/Trabajos%20Pr%C3%A1cticos/TP1/enunciado.pdf).
Se consultó esa copia del documento docente; no se incorporaron soluciones
de otros grupos. La entrega del curso se pedía en PDF.

## Decisiones del modelo

- Apuestas entre cero y uno con suma uno; pagos e inversión inicial positivos.
  Los recursos posteriores pueden quedar en cero.
- Todas las personas participan del mismo horizonte temporal. Cada una
  puede tener su propia cantidad de eventos posibles.
- El reparto conserva recursos. Se calcula para todos antes de avanzar al
  instante siguiente; no se actualizan personas de manera secuencial.
- Los extremos de una trayectoria comparan con su único vecino. Un elemento
  aislado satisface la comparación vacía; las mesetas no son máximos estrictos.
- Las decisiones comparan recursos **al final** y no alteran parámetros ajenos.
  Los empates admiten cualquiera de las opciones óptimas.
- La apuesta óptima se especifica sobre el simplex cerrado. Exigir apuestas
  estrictamente positivas puede impedir que exista un máximo.

## Revisión de la resolución

La revisión posterior conserva autoría y contexto, y corrige longitud de
salidas, índices de vecinos, dimensiones, alcance de cuantificadores y firmas
de auxiliares. El procedimiento de trayectorias es inout y no devuelve una
lista adicional. En WP se mantiene el factor inicial durante toda la prueba
y se conservan las hipótesis del contrato en el invariante.

El pseudocódigo de la versión3 inicia res con recursos, aunque su parámetro
se llama recurso. El documento normaliza ese nombre y señala la errata.
El algoritmo sigue siendo el mismo.

La edición pública usa paquetes LaTeX estándar y macros propias. El paquete
de Overleaf con logos, estilos y macros docentes se conserva íntegro en el
respaldo académico; no se necesita para compilar esta edición. Los cambios
posteriores no se presentan como entrega original ni aprobación docente.

## Compilar y comprobar

Abrir esta carpeta en un editor LaTeX o ejecutar:

```sh
tectonic main.tex
python -m unittest discover -s comprobacion -p "test_*.py"
```

Python3.12, biblioteca estándar y racionales exactos; no hay datos personales
ni dependencias numéricas externas. Las ocho pruebas contrastan la tabla de
la consigna sin redondeo, conservación, ceros, horizonte vacío, máximos
locales y cada prefijo del invariante.

apuesta_en_malla examina una malla racional finita: sirve para ejemplos y
contraejemplos, **no certifica el óptimo entre todos los reales**. La existencia
del máximo continuo se justifica por compacidad y continuidad en el documento.
