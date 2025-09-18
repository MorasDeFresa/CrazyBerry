# Crazy Berry

Crazy Berry es un juego de plataformas 2D donde controlas a un personaje que debe recolectar frutas de los árboles mientras evita enemigos.

## Características

- Sistema de menús (principal y game over)
- Personaje jugable con movimientos físicos realistas
- Múltiples tipos de enemigos con comportamientos diferentes
- Sistema de recolección de frutas con valores variables
- Sistema de vidas y puntuación
- Efectos de sonido
- Animaciones de sprites

## Controles

- Flecha izquierda/derecha: Moverse
- Flecha arriba: Saltar
- Flecha abajo: Interactuar con árboles (recolectar frutas)

## Instalación

1. Asegúrate de tener Python 3.x instalado
2. Instala PyGame: `pip install pygame`
3. Ejecuta el juego: `python game.py`

## Estructura del Proyecto

- `game.py`: Archivo principal del juego
- `entities.py`: Clases para entidades (jugador, enemigos, frutas)
- `tilemap.py`: Sistema de mapas y colisiones
- `utils.py`: Utilidades para carga de assets
- `ui.py`: Sistema de menús e interfaz de usuario
- `data/`: Carpeta con assets (sprites y sonidos)

## Mecánicas de Juego

- Recolecta frutas de los árboles presionando la flecha abajo cuando estés cerca
- Cada fruta tiene un valor aleatorio (5, 10 o 15 puntos)
- Evita a los enemigos que patrullan el nivel
- Si un enemigo te toca, perderás una vida
- El juego termina cuando te quedas sin vidas

## Personalización

Puedes modificar el nivel editando la función `__init__` en `tilemap.py` para cambiar la disposición de plataformas, árboles y enemigos.