# `fedora` on PyPI

This dummy project is not installable.
You probably want `python-fedora` instead.


## pyproject.toml tool.fedora namespace

The [PEP 518](https://www.python.org/dev/peps/pep-0518/#tool-table) declares
that a project can use the subtable `tool.$NAME` if `pyproject.toml` if,
and only if, they own the entry for `$NAME` in the Cheeseshop/PyPI.

That's what this project is for.
We own the entry for `fedora`, so we could use `tool.fedora` in .

## python-fedora

The Fedora Infra's [python-fedora](https://github.com/fedora-infra/python-fedora)
project provides an importable module named `fedora`.

This goes against the convention that PyPI distribution names should
match the module names.
But, python-fedora pre-dates wide use of that convention, and the issue
is hard to fix now.

Please install `python-fedora` to get the Fedora Infra's package.

### Please: Don't install packages blindly

When you see the exception:

```
ModuleNotFoundError: No module named 'foo'
```

… please research the actual requirements instead of going directly for
`pip install foo`.
The project (distribution) name may differ from the module(s) it
provides.
