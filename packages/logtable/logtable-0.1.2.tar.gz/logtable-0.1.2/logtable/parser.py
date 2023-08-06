import datetime
import json
import math
import os
import os.path as osp

import pandas


def parse(
    root_dir,
    sort=None,
    q=None,
    float_format=None,
    params_basename="params.json",
    log_basename="log.csv",
    key_epoch="epoch",
    key_iteration="iteration",
    key_elapsed_time="elapsed_time",
):
    """parse(root_dir, sort=None, q=None)

    Parse log directory to create a log table.

    Parameters
    ----------
    root_dir: str
        Root directory that contains logs.
    sort: str, optional
        Sort logs.
    q: str, optional
        Query of log keys.
    float_format: str, optional.
        Float value formatting (default: '{:.3g}').

    Returns
    -------
    df: pandas.DataFrame
        Log table.
    summary_keys: list of str
        List of keys from summary.
    args_keys: list of str
        List of keys from args.
    log_keys: list of str
        List of keys from log.
    """
    if float_format is None:
        float_format = "{:.3g}"

    log_dirs = sorted(os.listdir(root_dir))

    # params
    params_keys = set()
    log_keys = set()
    data = []
    for log_dir in sorted(log_dirs):
        params_file = osp.join(root_dir, log_dir, params_basename)
        try:
            with open(params_file) as f:
                params = json.load(f)
        except IOError:
            data.append({"log_dir": log_dir})
            continue
        params_keys = params_keys | set(params.keys())
        datum = params
        datum["log_dir"] = log_dir

        log_file = osp.join(root_dir, log_dir, log_basename)
        ext = osp.splitext(log_basename)[1]
        try:
            if ext == ".csv":
                log = pandas.read_csv(log_file)
            elif ext == ".json":
                with open(log_file) as f:
                    log = pandas.DataFrame(json.load(f))
            else:
                data.append(datum)
                continue
            if log.empty:
                raise pandas.errors.EmptyDataError
        except (IOError, pandas.errors.EmptyDataError):
            datum[key_epoch] = 0
            datum[key_iteration] = 0
            data.append(datum)
            continue

        if key_epoch not in log.columns:
            log[key_epoch] = 0

        datum[key_epoch] = log[key_epoch].max()
        datum[key_iteration] = log[key_iteration].max()
        datum[key_elapsed_time] = datetime.timedelta(
            seconds=int(round(log[key_elapsed_time].max()))
        )

        now = datetime.datetime.now()
        mtime = datetime.datetime.fromtimestamp(osp.getmtime(log_file))
        seconds = (now - mtime).total_seconds()
        datum["updated_at"] = datetime.timedelta(seconds=int(round(seconds)))

        for col in log.columns:
            if col in [key_epoch, key_iteration, key_elapsed_time]:
                continue

            key = "{} (max)".format(col)
            log_keys.add(key)
            index = log[col].idxmax()
            if math.isnan(index):
                break
            datum[key] = (
                log[col][index],
                (log[key_epoch][index], log[key_iteration][index]),
            )

            key = "{} (min)".format(col)
            log_keys.add(key)
            index = log[col].idxmin()
            datum[key] = (
                log[col][index],
                (log[key_epoch][index], log[key_iteration][index]),
            )

        data.append(datum)

    summary_keys = [key_epoch, key_iteration, key_elapsed_time, "updated_at"]
    summary_keys += sorted(params_keys)
    summary_keys += sorted(log_keys)

    df = pandas.DataFrame(data=data, columns=["log_dir"] + summary_keys)

    if sort is not None:
        key = sort
        ascending = True
        if key.startswith("-"):
            key = key[1:]
            ascending = False
        df = df.sort_values(by=key, ascending=ascending)

    # format
    for col in df.columns:
        if col.endswith(" (min)") or col.endswith(" (max)"):
            key = col[:-6]
            values = []
            for value in df[col].values:
                if isinstance(value, tuple):
                    values.append((float_format.format(value[0]), value[1],))
                else:
                    values.append((value, (0, 0)))
            df[col] = values
        elif df[col].dtype.name == "timedelta64[ns]":
            values = []
            for value in df[col]:
                try:
                    value = datetime.timedelta(seconds=value.total_seconds())
                    value = str(value)
                except ValueError:
                    pass
                values.append(value)
            df[col] = values
        else:
            df[col] = df[col].astype(str)

    if q is not None:
        try:
            df = df.query(q)
        except Exception:
            pass

    return df, summary_keys, params_keys, log_keys
