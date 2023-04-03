# `PEPHubClient`

`PEPHubClient` is a tool to provide Python and CLI interface and Python API for [PEPhub](https://pephub.databio.org).

`pephubclient` features: 
1) `push` (upload) projects)
2) `pull` (download projects)

Additionally, our client supports pephub authorization.
The authorization process is based on pephub device authorization protocol.
To upload projects or to download privet projects, user must be authorized through pephub.

To login and logout use `login` and `logout` arguments respectively.

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