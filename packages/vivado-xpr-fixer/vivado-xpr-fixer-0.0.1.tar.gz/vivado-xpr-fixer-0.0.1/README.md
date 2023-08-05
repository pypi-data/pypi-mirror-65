# vivado-xpr-fixer
Fixes the project path name when using Vivado and Git together.

## Problem:

Vivado uses fully qualified pathnames when describing the location of the project file.
This causes issues when multiple people are working on multiple machines with the same Vivado project as the pathnames are likely to be different.

## Solution:

This script simply modifies the project file so that the pathname is fixed to the directory containing the project file.

## Installation:
This script can be installed using pip with:
```console
user@console~$ python3 -m pip install --user --upgrade vivado_xpr_fixer
```

## Installation from source
To install from source clone this repositry then run:
```console
user@console~$ python3 setup.py install
```

### Installing the Git Hook:

This script can operate as a git hook.
This means that it will automatically run whenever you perform a `git pull`.
You will need to install the git hook on every client machine as hooks aren't stored in the repository.

```console
user@console~$ vivado-xpr-fixer install
```

Note that "python" will need to be installed somewhere where git can execute it.

### Removing the Git Hook:

```console
user@console~$ vivado-xpr-fixer install
```

### Manually Updating the XPR File:

```console
user@console~$ vivado-xpr-fixer update
```

Note that you won't need to do this if you have it running via a git hook.
