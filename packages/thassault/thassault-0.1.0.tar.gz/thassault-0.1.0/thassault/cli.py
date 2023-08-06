import click
import json
import sys
from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output json file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    total_time, results = assault(url, requests, concurrency)
    assault_results = Results(total_time, results)
    display_results(assault_results, json_file)


def display_results(results: Results, json_file: str) -> None:
    """
    Prints the results or writes them to a json file
    """
    if json_file:
        # Write the results to the file
        try:
            with open(json_file, "w") as output_file:
                data = {
                    "Successful Requests": len(results.requests),
                    "Slowest": results.slowest(),
                    "Fastest": results.fastest(),
                    "Average": results.average_time(),
                    "Total time": results.total_time,
                    "Requests Per Minute": results.rpm(),
                    "Requests Per Second": results.rps(),
                }
                json.dump(data, output_file)
                print("... Done!")
        except (EnvironmentError, IOError) as e:
            print(e)
            sys.exit(1)
    else:
        # Print the results to the stdout
        print("... Done!")
        print("--- Results ---")
        print("{0: <25} {1}".format("Successful requests", len(results.requests)))
        print("{0: <25} {1}".format("Slowest", results.slowest()))
        print("{0: <25} {1}".format("Fastest", results.fastest()))
        print("{0: <25} {1}".format("Average", results.average_time()))
        print("{0: <25} {1}".format("Total time", results.total_time))
        print("{0: <25} {1}".format("Requests Per Minute", results.rpm()))
        print("{0: <25} {1}".format("Requests Per Seconds", results.rps()))
