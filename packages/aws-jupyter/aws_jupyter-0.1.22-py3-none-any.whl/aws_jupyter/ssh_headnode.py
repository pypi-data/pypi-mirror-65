#!/usr/bin/env python
import argparse
import os
import sys

from operator import itemgetter
from .common import load_config
from .common import query_status


def ssh_headnode(args):
    args = load_config(args)
    all_status = query_status(args)
    if len(all_status) == 0:
        print("No instance found in the cluster '{}'. Quit.".format(args["name"]))
        return
    print("{} clusters found with the name '{}'.".format(len(all_status), args["name"]))

    for idx, status in enumerate(all_status):
        total = len(status)
        if total == 0:
            continue
        print("\nCluster {}:".format(idx + 1))
        ready = sum(t[0] == "running" for t in status)
        # neighbors = list(map(itemgetter(1), status))
        print("    Total instances: {}\n    Running: {}".format(total, ready))
        if ready == 0:
            print("    Instances status: {}".format(status[0][0]))
            continue
        print("Connecting to the first node.")
        url = [t[1] for t in status if t[0] == "running"][0]
        os.system("ssh -i {} ubuntu@{}".format(args["key_path"], url))
        break


def main_ssh_headnode():
    parser = argparse.ArgumentParser(
        description="SSH into the head node of a cluster",
        usage="aws-jupyter config <args>",
    )
    parser.add_argument("--name",
                        required=False,
                        help="cluster name")
    parser.add_argument("--region",
                        help="Region name")
    parser.add_argument("--credential",
                        help="path to the credential file")
    args = vars(parser.parse_args(sys.argv[2:]))
    ssh_headnode(args)


if __name__ == '__main__':
    main_ssh_headnode()
