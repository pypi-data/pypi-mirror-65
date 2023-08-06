import asyncio
import time
import os
import requests


def fetch(url):
    """ Make the request and return the results """
    start_time = time.monotonic()
    r = requests.get(url)
    request_time = time.monotonic() - start_time
    return {"status_code": r.status_code, "request_time": request_time}


async def worker(name, queue, results):
    """
    A function to take unmet requests from a que, perform the request and
    add the results the to queue
    """
    # Get the loop object to use it for calling the fetch function
    cur_loop = asyncio.get_event_loop()
    while True:
        # Wait to get a new request
        url = await queue.get()
        if os.getenv("DEBUG"):
            print(f"{name} fetching {url}")
        future_result = cur_loop.run_in_executor(None, fetch, url)
        result = await future_result
        results.append(result)
        # Mark the request in job as done
        queue.task_done()


async def distribute_work(url, req_numb, concurrency, results):
    """
    Create the queue with the requests to be done, create tasks and call
    workers to implement the tasks
    """
    # Create the queue from asyncio Queue class that contains all the tasks
    # that need to be done (all the requests)
    queue = asyncio.Queue()

    # Add an item to the queue for every request that we need to make
    for _ in range(req_numb):
        queue.put_nowait(url)

    # Create the list of tasks. Each task is a worker that will implement a
    # request from the queue
    tasks = []
    for i in range(concurrency):
        # Create the workers calling the async worker function
        task = asyncio.create_task(worker(f"worker-{i+1}", queue, results))
        tasks.append(task)

    start_time = time.monotonic()
    # Start the tasks and wait for them to finish
    await queue.join()
    stop_time = time.monotonic()
    total_time = stop_time - start_time

    # Cancel/Destroy all the workers tasks that have started
    for task in tasks:
        task.cancel()

    return total_time


def assault(url, requests, concurrency):
    """ Entrypoint to be called by the CLI command to make the requests"""
    # Create the results list to be passed to other functions
    results = []
    # Call the async function distribute work. Call it with asyncio
    total_time = asyncio.run(distribute_work(url, requests, concurrency, results))
    return total_time, results
