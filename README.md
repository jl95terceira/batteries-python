Batteries to complement the standard library (Python)

# Build and install

Required:

- Python packages:

  - `hatch`
  - `build`

  These packages can be `pip`-installed. Example:

  ```
  pip install hatch
  ```

To build / pack up, run the following command at the top directory.

```
python -m build
```

A `.whl` is generated at directory `dist` which can then be `pip`-installed like so.

```
pip install dist\jl95terceira_batteries-...whl
```
