# Notebook publication sources

These are reviewed publication copies, not the authoritative research projects.
Only published notebook exports are served from `static/labs/`.

## TDOA / GDOP

- Original: `sigproc-notes/notebooks/tdoa-gdop.py`.
- Original SHA-256 when copied:
  `d04518152efbdc4b0ceeb5e09954b24dfa062f95a61ccf84e70c134555381012`.
- Changes from the original: pin marimo 0.25.2 and add platform-specific package
  dependencies for Pyodide. Numerical code and controls are unchanged.
- Native versions: NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2.
- Browser versions: NumPy 2.4.3, SciPy 1.17.1, Matplotlib 3.10.8.

From the website repository root:

```sh
uvx --from marimo==0.25.2 marimo check notebooks/tdoa-gdop.py --select MW
uvx --from marimo==0.25.2 marimo export html-wasm notebooks/tdoa-gdop.py \
  --no-sandbox --mode run --no-show-code --output static/labs/tdoa-gdop
```

`--no-sandbox` here applies only to serialization of the WASM export; the export
command does not execute native notebook cells. Runtime dependencies remain in
the embedded script metadata for installation by Pyodide. Do not use this flag
as a substitute for the correct environment when executing a notebook locally.

To regenerate an existing export, review source changes first and add `--force`
to the export command.

The WASM export downloads its Python runtime and scientific packages on first
load and requires internet access. Browser versions are listed above; the
notebook code remains inspectable in run mode.

Preview with `zola serve`, then open `/technical/` and select **TDOA HGDoP
Exploration**. Check controls, plots, and the optional Monte Carlo run over HTTP.
Do not edit generated HTML/JavaScript to change the notebook.
