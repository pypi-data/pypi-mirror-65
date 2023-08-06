# irma-shared

irma-shared is a collection of objects and well-known values used by
[IRMA](https://github.com/quarkslab/irma) and required to communicate with its
API.

*irma-shared is not a project in itself and is only meant to be used as a
dependency*

```python
import requests
import sys
from irma.shared.schemas.v2 import ScanSchema
from irma.shared.csts import ScanStatus

scanid = "9e21108a-3552-4309-af39-684c32664391"
r = requests.get("http://172.16.1.30/api/v2/scans/" + scanid)
scan = ScanSchema().loads(r.text)

assert scan.id == scanid

if scan.status >= ScanStatus.finished:
    print("Scan finished", file=sys.stderr)
else:
    print("Scan in progress", file=sys.stderr)
```

## Work in progress

- Use a stable version of marshmallow
- Complete unit tests

## Get it now

```console
$ pip install irma-shared
```

## Documentation

None for now

## Requirements

- python >= 3.5
- marshmallow >= 3.0.0

Requirements are exhaustively listed in
[setup.py](https://github.com/quarkslab/irma-shared/setup.py)

## Authors

irma-shared is developed by the IRMA development team at
[Quarkslab](https://quarkslab.com); mail: irma-dev AT quarkslab DOT com.

## Project links

- IRMA: https://github.com/quarkslab/irma/
- Documentation: None
- PyPI: https://pypi.org/project/irma-shared/
- Issues: https://github.com/quarkslab/irma-shared/issues/

## License

APACHE v2 licensed. See the attached
[LICENSE](https://github.com/quarkslab/irma-shared/LICENSE)
