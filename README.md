# SADI → PowerModels

Este repositorio contiene un conjunto de scripts para convertir la red del **SADI** publicada por **CAMMESA** en un modelo compatible con **PowerModels.jl**, pensado para estudios de flujo de carga en estado estacionario.

> **Nota:** PowerModels está orientado únicamente a flujos de carga en estado estacionario. No es adecuado para estudios dinámicos.

---

## Consideraciones de modelado

### Barras de baja impedancia
Se aplica el mismo criterio que en **PSS®E** para la unión de barras eléctricamente cercanas, utilizando un umbral de impedancia nula de `ZHRSHZ = 0.0001`.  
En todos los casos, se conserva la barra con el número más pequeño.

### Shunts
Actualmente se modelan como elementos fijos, ya que PowerModels no soporta el modelado de pasos (taps) de shunt de manera nativa.

### Líneas de corriente continua (HVDC)
Aunque PowerModels puede representar líneas HVDC, en la Base de Estudio de CAMMESA solo está presente el vínculo de **Furnas**.  
Por simplicidad, se opta por:
- Desconectar la conversora HVDC.
- Reemplazar su intercambio de potencia con una demanda equivalente.  

De esta forma se evita la existencia de dos barras swing en el sistema.

### Red de Paraguay
Se ha identificado que el vínculo radial **Ayolas–Villalbín** es el principal causante de grandes *mismatches* y problemas de convergencia.  
Para mejorar la estabilidad numérica del modelo:
- Se elimina este vínculo del sistema.
- Se agrega una demanda equivalente para representar el consumo de esa parte de la red.
