import contextlib

from . import main

# This file is the entrypoint when `hohh` is run as a module, defer all actual logic to
# common `main` function defined in `main.py`
with contextlib.suppress(KeyboardInterrupt):
    main.main()
