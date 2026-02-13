
######################################Coroutines###########################################

import asyncio


#  función asíncrona , se ejectura parte de la función hasta el asyncio.sleep(10) , espera y continúa el resto de ejecución
"""
async def main():
    print('hello')
    await asyncio.sleep(10)
    print('world')

asyncio.run(main())
"""

############################
# función asíncrona donde se llama a la funcion say_after , pasamos parametros de time en sg y string para imprimir
"""
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')     # Espera 1sg e imprime "hello"
    await say_after(2, 'world')     # Espera 2sg e imprime "world"

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
"""

###########################
"""
# La función asyncio.create_task() se utiliza para ejecutar coroutines de forma concurrente como tareas de asyncio (Tasks).
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    
async def main():
    task1 = asyncio.create_task(        #asyncio.create_task() se utiliza para ejecutar coroutines de forma concurrente como tareas de asyncio (Tasks)
        say_after(1, 'hello'))          #asyncio.create_task() se utiliza para ejecutar coroutines de forma concurrente como tareas de asyncio (Tasks)

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())

"""
########################
# La clase asyncio.TaskGroup proporciona una alternativa más moderna a create_task(). Usando esta API, el último ejemplo queda de la siguiente forma:

"""

import asyncio
import time
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(
            say_after(1, 'hello'))

        task2 = tg.create_task(
            say_after(2, 'world'))

        print(f"started at {time.strftime('%X')}")

    # The await is implicit when the context manager exits.

    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())

"""

# El tiempo de ejecución y la salida deberían ser los mismos que en la versión anterior.



###########################Awaitables#####################################

"""
import asyncio

async def nested():
    return 42

async def main():
    # Nothing happens if we just call "nested()".
    # A coroutine object is created but not awaited,
    # so it *won't run at all*.
    nested()  # will raise a "RuntimeWarning".

    # Let's do it differently now and await it:
    print(await nested())  # will print "42".

asyncio.run(main())
"""


"""
asyncio_reference.py
---------------------------------
Referencia completa de asyncio en Python
Incluye coroutines, tasks, TaskGroup, timeouts, ejecuciones concurrentes y más.
Versión de Python: 3.14+
Autor: Rafa
"""

import asyncio
import time
import datetime
from asyncio import TaskGroup

# ------------------------------
# 1. COROUTINES
# ------------------------------
# Las coroutines se definen con async def y se ejecutan usando await o asyncio.run()

async def hello_world():
    print("hello")
    await asyncio.sleep(1)
    print("world")

# asyncio.run(hello_world())


# ------------------------------
# 2. AWAITABLES
# ------------------------------
# Objetos que se pueden usar con await: coroutines, Tasks, Futures

async def nested():
    return 42

async def await_example():
    # Corutina simple
    result = await nested()
    print("Nested result:", result)

# asyncio.run(await_example())


# ------------------------------
# 3. CREATING TASKS
# ------------------------------

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def tasks_example():
    # Crear Tasks concurrentes
    task1 = asyncio.create_task(say_after(1, "hello"))
    task2 = asyncio.create_task(say_after(2, "world"))

    print(f"Started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"Finished at {time.strftime('%X')}")

# asyncio.run(tasks_example())


# ------------------------------
# 4. TASK GROUPS (Python 3.11+)
# ------------------------------
# Permite ejecutar varias coroutines de forma concurrente
async def taskgroup_example():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(say_after(1, "hello"))
        tg.create_task(say_after(2, "world"))
        print(f"Started at {time.strftime('%X')}")
    print(f"Finished at {time.strftime('%X')}")

# asyncio.run(taskgroup_example())


# ------------------------------
# 5. TASK CANCELLATION
# ------------------------------
async def cancel_me():
    print("cancel_me(): before sleep")
    try:
        await asyncio.sleep(3600)
    except asyncio.CancelledError:
        print("cancel_me(): cancel sleep")
        raise
    finally:
        print("cancel_me(): after sleep")

async def cancellation_example():
    task = asyncio.create_task(cancel_me())
    await asyncio.sleep(1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Task is cancelled now")

# asyncio.run(cancellation_example())


# ------------------------------
# 6. RUNNING TASKS CONCURRENTLY
# ------------------------------
async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), i={i}")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

async def gather_example():
    results = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4)
    )
    print("Results:", results)

# asyncio.run(gather_example())


# ------------------------------
# 7. SLEEPING
# ------------------------------
async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

# asyncio.run(display_date())


# ------------------------------
# 8. TIMEOUTS
# ------------------------------
async def eternity():
    await asyncio.sleep(3600)

async def timeout_example():
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print("timeout!")

# asyncio.run(timeout_example())


# ------------------------------
# 9. RUNNING IN THREADS
# ------------------------------
def blocking_io():
    print(f"Start blocking_io at {time.strftime('%X')}")
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")

async def threads_example():
    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(1)
    )
    print(f"Finished main at {time.strftime('%X')}")

# asyncio.run(threads_example())


# ------------------------------
# 10. INTROSPECTION
# ------------------------------
async def introspection_example():
    task = asyncio.current_task()
    print("Current task:", task)
    all_tasks = asyncio.all_tasks()
    print("All tasks:", all_tasks)
    print("Is coroutine:", asyncio.iscoroutine(hello_world()))

# asyncio.run(introspection_example())


# ------------------------------
# 11. MAIN
# ------------------------------
# Para ejecutar cualquier ejemplo:
if __name__ == "__main__":
    asyncio.run(taskgroup_example())




