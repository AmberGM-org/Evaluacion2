# Evaluación 2 — Indicaciones de viaje con GraphHopper - **Aldo Borotto y Ambar Gonzalez**

Este proyecto es un **script en Python** que consulta la API de **GraphHopper** para:
- Geocodificar **origen** y **destino** (latitud/longitud y etiquetas legibles).
- Calcular una **ruta** para los perfiles `car`, `bike` o `foot`.
- Mostrar **distancia total**, **duración total** y la **narrativa paso a paso** del trayecto en español.
- Funciona en modo interactivo por consola.

---

## Requisitos

- **Python 3.8+**
- Librería **requests**
- **Clave de API** de GraphHopper (gratuita o de pago)

```bash
pip install requests
```

> **Nota:** El script incluye la constante `GRAPHOPPER_KEY`. Reemplázala por tu propia clave antes de ejecutar.

---

## Archivos principales

- `Instrucciones de viaje.py` (o el nombre de archivo que estés usando)
- Este `README.md`

---

## Configuración de la API

Edita la constante en el archivo `.py`:

```python
GRAPHOPPER_KEY = "TU-CLAVE-DE-GRAPHHOPPER"
```

> Si prefieres no hardcodear la clave, puedes leerla desde una variable de entorno:
>
> ```python
> import os
> GRAPHOPPER_KEY = os.getenv("GRAPHOPPER_KEY", "")
> ```
> y exportarla antes de ejecutar:
> ```bash
> export GRAPHOPPER_KEY="tu_clave_aquí"
> ```

---

## Ejecución rápida

Desde VS Code o terminal:

```bash
python3 "ruta/al/archivo/Instrucciones de viaje.py"
```

El programa mostrará los **perfiles disponibles**, solicitará **origen** y **destino**, y luego imprimirá el **resumen** y la **narrativa** del viaje.

> Puedes **salir** en cualquier momento ingresando `s` o `salir` cuando se te pida un perfil, origen o destino.

---

## Flujo de uso (interactivo)

1. Selecciona el **perfil de vehículo**: `car`, `bike` o `foot`.  
   - Si ingresas un valor inválido o vacío, se usa **`car`** por defecto.
2. Ingresa la **Ubicación de origen** (puede ser ciudad, comuna y/o país).
3. Ingresa la **Ubicación de destino**.
4. El programa:
   - Geocodifica ambos puntos y muestra su **etiqueta** y **tipo OSM**.
   - Llama a la API de **routing** y muestra:
     - **Estado de Routing** (esperado `200` si fue exitoso).
     - **Distancia total** (km y millas).
     - **Duración total** (horas y minutos).
     - **Narrativa paso a paso** con texto en español, indicando distancia y tiempo por indicación.

---

## Ejemplo de sesión

```
+++++++++++++++++++++++++++++++++++++++++++++
Perfiles de vehículo disponibles en GraphHopper:
+++++++++++++++++++++++++++++++++++++++++++++
car, bike, foot
+++++++++++++++++++++++++++++++++++++++++++++
Presionar 's' o escribir 'salir' para terminar)

Ingresa un perfil(vehículo): car

Ubicación de origen: Santiago, Chile
Santiago, Región Metropolitana, Chile (Tipo: city)

Ubicación de destino: Valparaíso, Chile
Valparaíso, Región de Valparaíso, Chile (Tipo: city)

=================================================
Indicaciones desde °Santiago, Región Metropolitana, Chile° hasta °Valparaíso, Región de Valparaíso, Chile° en car
=================================================
Estado de Routing: 200
=================================================
Distancia total: 116.45 km / 72.37 mi
Duración total: 1.48 h / 88.73 min
=================================================
Narrativa del viaje (paso a paso):
01. Continúe por Autopista X  —>  3.50 km, 5.20 min
02. Incorpórese a Ruta 68     —>  95.60 km, 70.30 min
03. Tome la salida hacia...   —>  2.10 km, 3.40 min
...
=================================================
```

> Los valores son **referenciales** según la API y pueden variar por perfil (`car/bike/foot`) y datos de tráfico/mapa disponibles.

---

## Mensajes y estados

- **`Estado de Routing: 200`** → la consulta de ruta fue satisfactoria.  
- **Geocoding sin resultados** → el script muestra *“No se encontraron resultados para la ubicación indicada.”*  
- **Errores de API** → se imprime el **código HTTP** y el **mensaje** devuelto por GraphHopper, por ejemplo:
  - *“Mensaje de error: No se encontró conexión entre los puntos o error desconocido.”*

---

## Buenas prácticas y notas

- Prefiere entradas **específicas** para mejorar la geocodificación (por ejemplo, “Providencia, Santiago, Chile”).
- Respeta los **límites de uso/cuotas** de tu plan GraphHopper.
- Para automatizar pruebas, puedes adaptar el script para leer entradas desde variables o argumentos en lugar de `input()`.

---

## Estructura del código (resumen)

- `geocodificar(lugar)`: consulta geocoding, devuelve `(lat, lng, etiqueta)` o `None`.
- `ruta(origen, destino, vehiculo)`: consulta routing y devuelve el primer `path` o `None`.
- `main()`: bucle interactivo, controla flujo y salida formateada.

---

## Licencia

Proyecto académico para fines educativos. Ajusta la licencia según los lineamientos de tu curso/institución.
