# Super Star Trek the Python Generation

La idea base es reflotar un juego de hace 50 años llamado Super Star Trek. En su momento corría en mainframes y su interfaz era puramente de texto, palabras y algo de "ascii art".

                     ,------*------,
     ,-------------   '---  ------'
      '-------- --'      / /
          ,---' '-------/ /--,
           '----------------'
     THE USS ENTERPRISE --- NCC-1701



# El juego original

La forma de uso del juego original es bastante espartana. Ponés comandos, a veces te pide alguna opción, y te tira lineas como respuesta, a veces con info escrita, a veces con dibujos hechos en ascii.

El objetivo es pilotear una Enterprise para destruir naves Klingon antes que se acabe el tiempo (se tiene un límite de días para completar la misión).

A continuación hago un resumen, pero pueden complementarlo con [este excelente artículo](https://gamesnostalgia.com/story/182/rediscovering-the-1978-text-only-super-star-trek-game) o incluso bajarse la versión que hizo esa persona y jugarlo un rato.


## Lo básico

Nos movemos por el espacio, el cual está simulado como una cuadrícula de 8 x 8 sectores llamados "cuadrantes", y en cada cuadrante (también una cuadrícula de 8 x 8) encontraremos estrellas, bases estelares y naves Klingon.

Ganamos el juego si destruimos todas las naves Klingon antes de la fecha límite. Perdemos si se acaba el tiempo antes, si nos quedamos sin energía, o si una nave Klingon nos destruye.

Para interactuar con la nave tenemos los siguientes comandos:

**`NAV` ("Navigation")**: Permite moverse por el espacio. El comando pide ingresar una dirección y un factor warp. Ver abajo en "Movimiento en el espacio".

**`SRS` ("Short Range Sensor")**: Muestra un escaneo del cuadrante actual, indicando la posición de la Enterprise, las naves Klingon, bases estelares de la Federación, y estrellas.

Ejemplo:
```
---------------------------------
     >!<     <*>                        STARDATE           3002
              *                         CONDITION          *RED*
                  *                     QUADRANT           6 , 7
              *       *                 SECTOR             1 , 4
                                        PHOTON TORPEDOES   10
 +K+                  *   *             TOTAL ENERGY       2916
                                        SHIELDS            0
                                        KLINGONS REMAINING 20
---------------------------------
```

(vemos que también muestra un reporte de estado resumido)


**`LRS` ("Long Range Sensor")**: Muestra el estado del espacio en los cuadrantes adyacentes a la Enterprise, indicando para cada cuadrante la cantidad de naves Klingon, de bases estelares, y de estrellas, como un número de 3 dígitos. Ejemplo: `207` significa 2 Klingons, 0 bases estelares, y 7 estrellas.

Ejemplo:

```
LONG RANGE SCAN FOR QUADRANT 8,4
-------------------
: 003 : 006 : 006 :
-------------------
: 005 : 001 : 002 :
-------------------
: *** : *** : *** :
-------------------
```

(la última fila está toda en asterisco porque estamos en el borde inferior de la galaxia)

**`PHA` ("Phasers")**: Permite atacar a las naves Klingon con una cantidad determinada de energía para debilitar sus escudos.

**`TOR` ("Torpedoes")**: Dispara torpedos fotón. Este arma tiene la ventaja de su potencia (si impacta en una nave Klingon la destruye inmediatamente) pero tiene la desventaja de su recorrido lineal (hay que apuntarle al enemigo, y si la dirección es equivocada o en el medio hay una estrella, el disparo será desperdiciado). Para indicar la dirección se usa el mismo sistema de curso que el motor warp, y tenemos la ventaja que la computadora (comando `COM`) puede calcular la trayectoria del torpedo automáticamente.

**`SHE` ("Shield")**: Permite asignar una cantidad de energía a los escudos.

**`DAM` ("Damage")**: Muestra el estado de reparación de todos los sistemas. Ejemplo:

```
DEVICE             STATE OF REPAIR
WARP ENGINES              -6.31
SHORT RANGE SENSORS        0
LONG RANGE SENSORS        -1.14
PHASER CONTROL             0
PHOTON TUBES               2.19
DAMAGE CONTROL             3.59
SHIELD CONTROL             0
LIBRARY-COMPUTER           0
```

Si el estado de un sistema es negativo, significa que está temporalmente "fuera de servicio".

**`COM` ("Computer")**: Permite acceder a la computadora de la nave; tiene seis opciones disponibles:

- Registro Galáctico Acumulativo: Muestra la memoria de la computadora con los resultados de todos los escaneos anteriores de sensores de corto y largo alcance. Ejemplo:

```
             1     2     3     4     5     6     7     8
           ----- ----- ----- ----- ----- ----- ----- -----
      1     ***   ***   ***   ***   ***   ***   ***   ***
           ----- ----- ----- ----- ----- ----- ----- -----
      2     ***   ***   004   008   006   ***   ***   ***
           ----- ----- ----- ----- ----- ----- ----- -----
      3     ***   ***   008   003   006   ***   ***   ***
           ----- ----- ----- ----- ----- ----- ----- -----
      4     ***   ***   004   001   005   ***   ***   ***
           ----- ----- ----- ----- ----- ----- ----- -----
      5     ***   ***   ***   ***   ***   ***   ***   ***
           ----- ----- ----- ----- ----- ----- ----- -----
      6     ***   ***   ***   ***   ***   ***   016   ***
           ----- ----- ----- ----- ----- ----- ----- -----
      7     ***   ***   003   006   006   ***   ***   ***
           ----- ----- ----- ----- ----- ----- ----- -----
      8     ***   ***   005   001   002   ***   ***   ***
           ----- ----- ----- ----- ----- ----- ----- -----
```

- Reporte de Estado: Indica el número de Klingons restantes, la fecha estelar y el número de bases estelares disponibles, más el mismo reporte de daños que se obtiene con `DAM`.

- Datos de Torpedos de Fotones: Calcula la dirección y distancia de los Klingons dentro del cuadrante actual.

- Datos de Navegación a Bases Estelares: Muestra la dirección y distancia a la base estelar más cercana en el cuadrante.

- Calculadora de Dirección/Distancia: Permite ingresar un par de coordenadas para obtener dirección y distancia entre esas coordenadas.

- Mapa de Regiones Galácticas: Muestra los nombres de las 16 regiones principales de la galaxia mencionadas en el juego.


## Los otros elementos en el espacio

**Naves Klingon**:
- son objetivo a destruir
- se mueven, lento... no me queda claro si pueden saltar de cuadrante (no haría la caza/búsqueda muy rara?)
- sabemos qué energía total tienen, pero no mucho más
- podemos atacarlas y nos pueden atacar cuando estamos en el mismo cuadrante

**Estrellas**:
- interrumpen torpedos
- si queremos pasar por ahí nos dañan
- no jode a los phasers
- no se mueven

**Bases estelares**:
- permite reabastecer energía
- permite reparar la nave
- todas las tareas llevan tiempo!
- no hay "combate" mientras estamos atracados
- no se mueven


## Movimiento

La nave arranca en un cuadrante al azar, en una posición al azar dentro del cuadrante, y se puede mover dentro del cuadrante (velocidad sublumínica) o entre cuadrantes (velocidad warp). Para moverse hay que utilizar el comando `NAV`, que pide dirección y velocidad.

La dirección del curso sigue un sistema "numérico circular":

 ```
         4  3  2
          . . .
           ...
       5 ---*--- 1
           ...
          . . .
         6  7  8
 ```

Se pueden usar valores enteros y decimales. Por ejemplo, `1.5` es un punto intermedio entre `1` y `2`.  El curso puede alcanzar hasta `9.0`, equivalente a `1.0`.

Un factor warp de `1` equivale a moverse un cuadrante. Ejemplo: Para ir del cuadrante `(6,5)` al `(5,5)`, usa curso `3` y factor warp `1`. Para moverse dentor del cuadrante la velocidad debe ser menor a 1. El motor warp deja a la nave en una posición al azar dentro del nuevo cuadrante (por lo que viajar a 2.1 o 2.9 de velocidad sería lo mismo), no estoy seguro por qué.

Hay situaciones donde el movimiento es prohibido: no se puede atraversar una estrella, una nave Klingon, o ir más allá del borde galáctico (se daña la nave de distintas formas). Por otro lado, el intentar atravesar una base estelar implica atracar en la base (para recarga de energía, reparaciones, etc.).

Si nos acercamos al borde de un cuadrante y nos movemos un poco más allá, cambiaremos de cuadrante. **Nota**: en el juego original la nave aparece en una posición al azar en el nuevo cuadrante, como si hubiese usado el motor warp, ¿quizás para evitar el problema de que justo haya una estrella en el punto de entrada del cuadrante?

Moverse consume energía (no sé en qué proporción... pero con los "tanques al 20%" deberíamos poder movernos uno o dos cuadrantes, y gran parte del cuadrante sublumínico, para poder llegar a una base).


## Sistemas de armas y combate

Separemos en dos grandes grupos, ataque y defensa. Para el ataque tenemos torpedos y phasers.

El torpedo tiene la ventaja de su potencia (si impacta en una nave Klingon la destruye inmediatamente) pero tiene la desventaja de su recorrido lineal (hay que apuntarle al enemigo, y si la dirección es equivocada o en el medio hay una estrella, el disparo será desperdiciado). Para indicar la dirección se usa el mismo sistema de curso que el motor warp, y tenemos la ventaja que la computadora (comando `COM`) puede calcular la trayectoria del torpedo automáticamente.

Tenemos una cantidad límite de torpedos, se recargan en las bases estelares Tener prendido el sistema de torpedos consume energía pero poca. Pueden dañarse y no podremos disparar.

Los phasers son guiados por la computadora e impactan automáticamente en todas las naves enemigas. Hay que asignarle energía para el disparo, y esa energía se dividirá (no equititivamente) entre todos los enemigos atacados.

Con respecto a la defensa tenemos únicamente el Escudo, que funciona a dos niveles. Por un lado absorbe impacto del ataque según la carga que tenga (aunque no de forma determinística); por ejemplo:

- la fuerza del ataque es de 500 unidades de energía
- el escudo tiene cargado 400, pero a nivel efectivo defenderá un poco menos que eso
- en el caso del ataque puntual, el azar dice que el escudo protegió 390
- el escudo se desgasta (pierde energía) un poco pero no demasiado (sino no tendría sentido tenerlo)
- los 110 restantes "impactan en la nave" (se descuentan esos valores de energía)

Por otro lado, la cobertura del escudoo puede no ser uniforme, y nuestros subsistemas pueden recibir daños puntuales; entonces en cada ataque existe la posibilidad de que se dañe algún subsistema.


# La modernización

Me gustaría tratar de mantener la jugabilidad inicial porque me parece bastante interesante. Tiene relativamente pocas vairables, pero interrelacionadas, lo cual deja *espacio para jugar* (pnu intended).

Al mismo tiempo, darle una vuelta de tuerca. Por un lado mejorar la interfaz pero manteniendola medio espartana, por otro lado hacerlo opcionalmente multijugador: que permita jugarlo de forma individual o cooperativo entre 1, 2 o 3 personas.

Veamos qué cambios pensaría sobre el juego original.


## La interfaz

La interfaz cambia bastante, principalmente para poder hacerlo multijugador. Por lo pronto tenemos tres "estaciones de trabajo" y una "pantalla general".

Si juegan tres personas, serán Capitán, Jefe de Ingeniería, y Oficial Militar. Cada persona verá alternativamente la pantalla general o su estación de trabajo. La pantalla general muestra información común y quizás no tan detallada, la consola de trabajo mostrará información muy detallada según cual estación de trabajo sea, más una linea de comandos que permite ingresar comandos para operar sobre el sistema.

Si juega una persona sola podrá alternar entre las distintas consolas de trabajo, como si se moviera en el puente de un lado para el otro. En cada estación de trabajo la dinámica es igual a como si estuviese jugando con otras personas. En el caso de jugar dos personas, una tendrá un rol fijo, y la otra se podrá mover entre las otras dos.

Más allá de eso, hay mucho del juego original que viene de una "limitación de interfaz". Ahora podemos mostrar más cosas al mismo tiempo, pero está bueno que no sea todo fácil/inmediato. Por ejemplo, en la pantalla general podríamos mostrar siempre el resultado del último `SRS`, pero NO que se actualice sólo.

Y está bueno mantener la interacción via comandos escritos, le da ese toque de arcaicidad :). Habiendo dicho eso, quizás es mejor que los comandos acepten parámetros, y no que repregunten. Por ejemplo, en el juego original se ingresa `NAV` y la computadora pide primero la dirección (ej. `6`) y la velocidad (ej. `0.8`), y me parece mejor que directamente podamos ingresar `NAV 6 0.8`.


## Comandos

Hablando de los comandos, lo mejor es mantener los originales, ya que tienen mucho sentido (excepto tal vez subcomandos de `COM`, ver abajo).

Por otro lado agregaría dos nuevos pensados en la administración de la energía, que creo le agregan una dinámica interesante de administración de recursos al juego, y además porque completan al rol de Jefe de Ingeniería. Estos dos comandos están explicados más abajo, en la descripción de ese rol.

Hay que ajustar también el comando `COM`. Comento puntualmente cada subcomando (la descripción de su funcionalidad ya fue hecha al principio del texto):

- Reporte de Estado: no nos aporta nada, lo sacaría; toda la info que está acá o es parte del reporte general o se obtiene con `DAM`

- Calculadora de Dirección/Distancia: este es útil, ya que nos permite calcular algo que sino tendríamos que hacer cuentas aparte (o hacerlas mentalmente, si nos queremos evitar perder tiempo en este subcomando, una decisión a tomar por quien juega)

- Datos de Torpedos de Fotones: este suena a trampa, lo sacaría; tener el cómo disparar a todos los Klingons en un paso suena como una sobresimplificación

- Datos de Navegación a Bases Estelares: lo sacaría; la base estelar ya se muestra, y nos podemos acercar iterando las distancias (no es a todo o nada como disparar un torpedo)

- Mapa de Regiones Galácticas: yay, nombres, no tienen otra utilidad, lo sacaría

En definitiva, `COM` tiene sólo un subcomando útil; sin confirmamos esto creo que podríamos re-pensarlo a que haga sólo el cálculo de trayectorias, quizás incluso renombrarlo a `TRA` o similar.

Para terminar, haría que `SRS` sólo reporte el mapa; la info extra que trae en el juego original debe ser parte de la pantalla general (estoy seguro que en el juego original se trae via `SRS` porque no se puede actualizar asincrónicamente).


## Los roles

Cada uno de los roles tiene una estación de trabajo diferente. La idea es que aunque haya algo de información compartida, los actuadores sean siempre distintos. Que los jugadores se tengan que comunicar para coolaborativamente llevar la misión a *buen puerto*.

Hay que lograr un balance entre: la info que todes ven todo el tiempo,  la info puntual que se puede pedir en cada estación de trabajo, y los actuadores también en cada una.


### Capitán

Hablando genéricamente es el que centraliza toda la operación.

Info que muestra todo el tiempo su estación de trabajo:
- cuantos klingons quedan en total
- cuantos días quedan en la misión
- energía total de la nave
- si la nave está "100% funcional" o no

Comandos que puede ejecutar:
- `NAV` ("Navigation")
- `SRS` ("Short Range Sensor")
- `LRS` ("Long Range Sensor")
- `COM` ("Computer") ??? (ver arriba "comandos")


### Jefe de Ingeniería

Es el responsable del mantenimiento, operación y optimización de todos los sistemas de la nave, especialmente el motor warp, la energía y las reparaciones en combate.

Info que muestra todo el tiempo su estación de trabajo:
- nivel de energía general disponible
- nivel de energía asignado a cada subsistema
- si la nave está "100% funcional" o no

Comandos que puede ejecutar:
- `DAM` ("Damage")
- `REP` ("Repair", ¡comando nuevo!): Permite asignar energía a cada subsistema para que se repare; cuanta más energía, más rápido se repara.
- `DIS` ("Distribute", ¡comando nuevo!): Permite asignar energía para el funcionamiento de cada subsistema; por ejemplo, los phasers pueden ser disparados con una determinada energía si esa energía estaba asignada previamente a ese subsistema.
- `COM` ("Computer") ??? (ver arriba "comandos")


### Oficial Militar

Es el encargado de la estrategia de combate, armamento y defensa de la nave.

Tiene el control del armamento y la defensa y protección de la nave: opera y dispara fásers y torpedos de fotón durante el combate, calcula trayectorias de disparo y ajusta la potencia de las armas, administra los escudos deflectores y ajusta su energía según sea necesario.

Info que muestra todo el tiempo su estación de trabajo:
- cuantos torpedos quedan
- sistema torpedos: on/off, y "ok/rotos"
- qué energía para phasers dispone
- escudo de la nave: a qué nivel están y si están funcionales

Comandos que puede ejecutar:
- `PHA` ("Phasers")
- `SHE` ("Shield")
- `TOR` ("Torpedoes")
- `COM` ("Computer") ??? (ver arriba "comandos")


### La pantalla general

Todos los roles ven la pantalla general, que contiene un resumen de la información disponible para todos los roles, aunque normalmente con menos precisión.

Por ejemplo (todos los datos se actualizan sólos, todo el tiempo, excepto donde se indique lo contrario):

- en qué cuadrante y en qué sector stá la nave
- la fecha estelar (o días faltantes para terminar la misión)
- cuantas naves Klingon quedan para terminar la misión
- el último mapa obtenido por el `SRS` (no se actualiza sólo!)
- la condición en general de la nave (no está muy definido, obvio "verde" es con todo al 100%, pero podríamos tener varias categorías en función de la energía restante y distintos subsistemas funcionando o no)
- escudos activados o no (sin indicar "potencia")
- si "armas" están ok: hay torpedos, el sistema está prendido y funcionando, los phasers están funcionando


## Movimiento

Replantaría lo de entrar en un cuadrante en un lugar al azar. La Enterprise "vuela rápido", no es que "salta de un punto al otro y puede caer más allá o más acá". Habría que manejar la situación de entrar a un cuadrante justo por donde está otro objeto (en velocidad sublumínica, donde la nave se mueve de a un casillero... si venía en velocidad warp podemos hacer que termine al costado del objeto).

El sistema de número circular es... raro. Claramente viene de teclados viejos; hoy por hoy se podría usar la disposición de números de un teclado numérico (el 6 a la derecha, 8 arriba, etc). Considerar que el teclado de un teléfono está espejado verticalmente. Por otro lado, ¿por qué no un sistema sexagesimal? (0-360°).

Es simpático que la computadora ayude a calcular el ángulo para moverse (o para disparar torpedos), poniendo coordenada origen y coordenada destino. Yo lo mantendría, porque aunque se siente como "hacer trampa" en realidad también lleva tiempo, con lo cual balancea.

No me queda claro si hay reglas estrictas con respecto a qué pasa si chocamos con cosas que no debemos chocar. Se podría definir que chocar con una estrella te saca N de energía, o chocar contra el borde de la galaxia te "rompe" el motor warp. O podría ser todo más al azar.


## Chau determinismo

Me parece que las reglas no tienen que ser absolutas. Un pequeño porcentaje de "anormalidad" está bueno en algunas situaciones. Por ejemplo:

- ante un ataque, hay un 10% de chance que se rompa un subsistema (al azar)

- chocar una estrella no saca un monto de energía fijo, sino entre un 40% y un 70% de la reserva actual

- nuestros ataquens impactan entre un 60% y 80% de la energía; por otro lado que las naves Klingon no ataquen siempre con la misma "fuerza"; usar para esto el contador interno que nos lleva a indicar si está viva o la destruimos, pero luego que use entre el 40% y el 60% de esa energía en cada ataque... esa energía si no tenemos escudos va directo a descontar la energía de la enterprise, pero si tenemos escudo la "neutraliza" entre un 80% y un 100% (según la energía del escudo) y al mismo tiempo el escudo se "desgasta" entre un 20% y un 40% de la energía recibida. Un ejemplo para mostrar todo esto que digo:

    - se encuentran las naves; la Klingon tiene 500 de energía; la Enterprise tiene 1000 de energía guardada y 400 en los escudos
    - la Enterprise dispara con 400 en los phasers, esto impacta en la Klingon y le resta 280 de energía, queda con 220 (sobrevive)
    - la Klingon dispara ahora, con 130 de fuerza, eso reduce los escudos en 40 (quedan en 360) y 25 "pasan y pegan en la nave" que queda en en 975
    - de ese ataque, el dado cayó en el 10% malo y se rompe un subsistema de la nave... al azar: el sistema de torpedos

Hay que encontrar más casos para eliminar el determinismo. Le da al juego la característica de ser predecible, "aprendible", pero sin poder predecir exactamente qué va a pasar.


## Comentarios sobre el setup inicial

Esto lo saqué del juego real, son variables que tenemos que definir y que balancean la dificultad del juego, así que son valores para arrancar probando:

- cuantas naves klingon (ej: 13)
- cuantos días (ej: 28)
- cuantas starbases (ej: 3)
- cuantas estrellas (ej: 50)
- distribuir todo eso al azar, poner la Enterprise al azar
- la Enterprise arranca con todos los sistemas funcionando, full energía, escudos apagados, full torpedos
- el espacio siempre es el mismo 8x8 cuadrantes, c/u con 8x8 posiciones

