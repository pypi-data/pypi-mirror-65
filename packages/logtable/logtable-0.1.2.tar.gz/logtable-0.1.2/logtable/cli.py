# flake8: noqa

import argparse
import os.path as osp
import re
import sys
import textwrap
import warnings

import tabulate
import yaml

from . import __version__
from .parser import parse


def main():
    config_file = ".logtable"
    if osp.exists(config_file):
        print(" * Config file: {}".format(config_file))
        with open(".logtable") as f:
            default_args = yaml.safe_load(f)
    else:
        default_args = {}

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version", "-V", action="store_true", help="show version and exit",
    )
    parser.add_argument(
        "--logdir",
        "-l",
        default=default_args.pop("logdir", "logs"),
        help="logs dir",
    )
    parser.add_argument(
        "--exclude",
        "-e",
        nargs="+",
        default=default_args.pop("exclude", []),
        help="exclude keys",
    )
    parser.add_argument(
        "--include",
        "-i",
        nargs="+",
        default=default_args.pop("include", []),
        help="include keys",
    )
    parser.add_argument("--keys", action="store_true")
    parser.add_argument(
        "--significant-figures",
        "-s",
        type=int,
        default=default_args.pop("significant_figures", 3),
        help="significant figures",
    )
    parser.add_argument(
        "--index",
        type=int,
        nargs="+",
        default=default_args.pop("index", None),
        help="index filtering",
    )
    parser.add_argument(
        "--column",
        "-c",
        type=int,
        default=default_args.pop("column", 30),
        help="maximum column width (0 for infinite)",
    )
    parser.add_argument(
        "--multi-column",
        action="store_true",
        default=default_args.pop("multi_column", False),
        help="prefer multi-column to vertically shorten the table",
    )
    parser.add_argument(
        "--params-basename",
        default=default_args.pop("params_basename", "params.json"),
        help="params or args of the experiment",
    )
    parser.add_argument(
        "--log-basename",
        default=default_args.pop("log_basename", "log.csv"),
        help="log of the experiment",
    )
    parser.add_argument(
        "--key-epoch",
        default=default_args.pop("key_epoch", "epoch"),
        help="key name of the epoch in the log file",
    )
    parser.add_argument(
        "--key-iteration",
        default=default_args.pop("key_iteration", "iteration"),
        help="key name of the iteration in the log file",
    )
    parser.add_argument(
        "--key-elapsed-time",
        default=default_args.pop("key_elapsed_time", "elapsed_time"),
        help="key name of the elapsed_time in the log file",
    )
    args = parser.parse_args()

    if args.version:
        print("logtable {}".format(__version__))
        sys.exit(0)

    if default_args:
        warnings.warn(
            "Config file .logtable has unsupported keys: {}".format(
                list(default_args.keys())
            )
        )

    float_format = "{:.%dg}" % args.significant_figures

    root_dir = osp.abspath(args.logdir)
    df, summary_keys, _, log_keys = parse(
        root_dir,
        float_format=float_format,
        params_basename=args.params_basename,
        log_basename=args.log_basename,
        key_epoch=args.key_epoch,
        key_iteration=args.key_iteration,
        key_elapsed_time=args.key_elapsed_time,
    )

    if args.index is not None:
        df = df.iloc[args.index]

    print(" * Log directory: {}".format(args.logdir))

    summary_keys = ["log_dir"] + summary_keys

    summary_keys_ = []
    for key in summary_keys:
        for excl in args.exclude:
            if re.match(excl, key):
                if any(re.match(incl, key) for incl in args.include):
                    summary_keys_.append(key)
                break
        else:
            summary_keys_.append(key)
    summary_keys = summary_keys_

    if args.keys:
        for key in summary_keys:
            print(key)
        sys.exit(0)

    headers = [""]
    for key in summary_keys:
        key_splits = key.replace("/", "/\n").replace("_", "_\n").splitlines()
        if args.column:
            key_splits = [
                x
                for key_split in key_splits
                for x in textwrap.wrap(key_split, width=args.column)
            ]
        key = "\n".join(key_splits)
        headers.append(key)
        if args.multi_column and key in log_keys:
            headers.append("")

    if df.empty:
        df.columns = summary_keys

    rows = []
    for index, df_row in df[summary_keys].iterrows():
        row = [index]
        for key, x in zip(summary_keys, df_row):
            if isinstance(x, tuple):
                assert len(x) == 2
                if args.multi_column:
                    row.extend(x)
                else:
                    x = "\n".join(str(xi) for xi in x)
                    row.append(x)
            else:
                x = str(x)
                x = textwrap.wrap(x, width=args.column) if args.column else [x]
                x = "\n".join(x)
                row.append(x)
        rows.append(row)

    table = tabulate.tabulate(
        tabular_data=rows,
        headers=headers,
        tablefmt="fancy_grid",
        stralign="center",
        showindex=False,
        disable_numparse=True,
    )
    print(table)
