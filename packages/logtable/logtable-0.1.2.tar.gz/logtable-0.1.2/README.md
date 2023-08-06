<h1 align="center">
  logtable
</h1>

<h3 align="center">
  Monitor and Compare Logs on Terminal.
</h3>

<div align="center">
  <a href="https://pypi.python.org/pypi/logtable"><img src="https://img.shields.io/pypi/v/logtable.svg"></a>
  <a href="https://pypi.org/project/logtable"><img src="https://img.shields.io/pypi/pyversions/logtable.svg"></a>
  <a href="https://github.com/wkentaro/logtable/actions"><img src="https://github.com/wkentaro/logtable/workflows/ci/badge.svg"></a>

  <br/>

  <img src=".readme/terminal.png" width="80%" />
</div>


## Installation

```bash
pip install logtable
```


## Usage

```bash
% cd examples
% logtable
 * Config file: .logtable
 * Log directory: logs
╒════╤════════════════════════╤═════════╤═════════════╤════════════╤══════════╤═══════════╤════════════╤═══════╤══════════════╤═══════════════╕
│    │          log_          │  epoch  │  iteration  │  elapsed_  │  class_  │  githash  │  hostname  │  lr   │    main/     │  validation/  │
│    │          dir           │         │             │    time    │   ids    │           │            │       │  loss (min)  │     main/     │
│    │                        │         │             │            │          │           │            │       │              │  loss (min)   │
╞════╪════════════════════════╪═════════╪═════════════╪════════════╪══════════╪═══════════╪════════════╪═══════╪══════════════╪═══════════════╡
│ 0  │ 20190310_093252.724597 │    1    │    1740     │  1:47:02   │   [1]    │  b48ce48  │ computer1  │ 0.001 │   0.00879    │     0.18      │
│    │                        │         │             │            │          │           │            │       │  (1, 1580)   │   (0, 880)    │
├────┼────────────────────────┼─────────┼─────────────┼────────────┼──────────┼───────────┼────────────┼───────┼──────────────┼───────────────┤
│ 1  │ 20190310_093829.691289 │    1    │    1720     │  1:45:37   │   [1]    │  f766b97  │ computer2  │ 0.001 │    0.0123    │     0.187     │
│    │                        │         │             │            │          │           │            │       │  (1, 1620)   │   (0, 440)    │
╘════╧════════════════════════╧═════════╧═════════════╧════════════╧══════════╧═══════════╧════════════╧═══════╧══════════════╧═══════════════╛
```

```yaml
# examples/.logtable

exclude:
  - out
  - updated_at
  - timestamp
  - loglevel
  - gpu
  - seed
  - 'lr .*'
  - '.*main/loss.*\(max\)'
  - '.*loss_.*'
params_basename: args.json
log_basename: log.json

# below configs are the same as the default
log_dir: logs
include: []
significant_figures: 3
index: null
multi_column: False
key_epoch: epoch
key_iteration: iteration
key_elapsed_time: elapsed_time
```
