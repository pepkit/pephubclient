# `PEPHubClient`

[![PEP compatible](https://pepkit.github.io/img/PEP-compatible-green.svg)](https://pepkit.github.io)
![Run pytests](https://github.com/pepkit/geofetch/workflows/Run%20pytests/badge.svg)
[![pypi-badge](https://img.shields.io/pypi/v/pephubclient)](https://pypi.org/project/pephubclient)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`PEPHubClient` is a tool to provide Python API and CLI for [PEPhub](https://pephub.databio.org).

`pephubclient` features: 
1) `push` (upload) projects)
2) `pull` (download projects)

Additionally, our client supports pephub authorization.
The authorization process is based on pephub device authorization protocol.
To upload projects or to download private projects, user must be authorized through pephub.

To login, use the `login` argument; to logout, use `logout`.

----
`phc --help`
```text
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ login                 Login to PEPhub                                                                        │
│ logout                Logout                                                                                 │
│ pull                  Download and save project locally.                                                     │
│ push                  Upload/update project in PEPhub                                                        │
│ version               Version                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

`phc pull --help`
```text
 Usage: pephubclient pull [OPTIONS] PROJECT_REGISTRY_PATH                                                       
                                                                                                                
 Download and save project locally.                                                                             
                                                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    project_registry_path      TEXT  [default: None] [required]                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────╮                                        
│                                         [default: default]                                                   │
│ --force             --no-force          Last name of person to greet. [default: no-force]                    │
│ --help                                  Show this message and exit.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

`phc push --help`
```text
 Usage: pephubclient push [OPTIONS] CFG                                                                         
                                                                                                                
 Upload/update project in PEPhub                                                                                
                                                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    cfg      TEXT  Project config file (YAML) or sample table (CSV/TSV) with one row per sample to          │
│                     constitute project                                                                       │
│                     [default: None]                                                                          │
│                     [required]                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --namespace                        TEXT  Project name [default: None] [required]                          │
│ *  --name                             TEXT  Project name [default: None] [required]                          │
│    --tag                              TEXT  Project tag [default: None]                                      │
│    --force         --no-force               Force push to the database. Use it to update, or upload project. │
│                                             [default: no-force]                                              │
│    --is-private    --no-is-private          Upload project as private. [default: no-is-private]              │
│    --help                                   Show this message and exit.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```