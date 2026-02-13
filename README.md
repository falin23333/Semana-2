# Análisis de Mercados con Python y Asyncio

Este proyecto descarga datos históricos de acciones desde Yahoo Finance y realiza agregaciones por semana y mes usando **pandas**. El objetivo principal es **comparar la ejecución paralela** usando corutinas.

## Paralelización

Se implementan dos enfoques para ejecutar descargas en paralelo:

1. **`asyncio.to_thread()`**  
   Ejecuta funciones bloqueantes (`requests`) en hilos.  
   Tiempo de ejecución: ~2.8 s

2. **`asyncio.create_task()`**  
   Ejecuta funciones asíncronas (`async def`) como corutinas.  
   Tiempo de ejecución: ~0.39 s

> Observación: `create_task()` es mucho más rápido aquí porque permite concurrencia real en tareas I/O-bound.

## Uso

1. Instalar dependencias:
```bash
pip install pandas curl-cffi
