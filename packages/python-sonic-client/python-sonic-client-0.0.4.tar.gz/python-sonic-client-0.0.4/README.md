# pysonic

pysonic is a Python client for lightweight and fast search engine - [Sonic](https://github.com/valeriansaliou/sonic)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install python-sonic-client --upgrade
```

## Usage

```python
import pysonic

c = pysonic.Client()
with c.mode(pysonic.Mode.INGEST) as ingestor:
    resp = ingestor.ping()

with c.mode(pysonic.Mode.SEARCH) as searcher:
    resp = searcher.ping()


## TODO 0.1.0
- Ingest commands: POP, COUNT, FLUSHC, FLUSHB, FLUSHO
- Implement queue, auto reconnect socket
- Support escape characters
- Support Control mode
- Support push a bulk by parallel sockets
- Support LANG
- Add tags: testcov, version, build
- Update tests

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
