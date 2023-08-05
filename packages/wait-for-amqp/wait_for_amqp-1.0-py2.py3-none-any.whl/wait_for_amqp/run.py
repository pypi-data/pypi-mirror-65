# coding=UTF-8
from __future__ import print_function

import time
from coolamqp.objects import NodeDefinition
from coolamqp.exceptions import ConnectionDead
from coolamqp.clustering import Cluster
import sys


def wait_for_amqp(host_name, wait_timeout, login, password, virtual_host):
    start_at = time.time()
    wait_println_counter = 0
    node_def = NodeDefinition(host=host_name, user=login, password=password, virtual_host=virtual_host)
    while time.time() - start_at < wait_timeout:
        time_remaining = wait_timeout - (time.time() - start_at)
        try:
            Cluster([node_def]).start(wait=True, timeout=time_remaining)
        except ConnectionDead:
            wait_println_counter += 3
            if wait_println_counter == 3:
                print("Waiting 30 more seconds...")
                wait_println_counter = 0
            time.sleep(10)
        else:
            sys.exit(0)
    else:
        print("Waiting time exceeded, aborting...")
        sys.exit(1)


def print_banner():
        print('''Use like:

    wait_for_amqp <hostname> <wait timeout> <login> <password> <virtual_host>

    All of these parameters are required.
    ''')
        sys.exit(0)


def run():
    if '-h' in sys.argv:
        print_banner()

    try:
        _, hostname, timeout, login, password, virtual_host = sys.argv
        timeout = int(timeout)
    except ValueError:
        print_banner()

    wait_for_amqp(hostname, timeout, login, password, virtual_host)


if __name__ == '__main__':
    run()
