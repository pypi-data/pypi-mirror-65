# anyser

Common interfaces for multiple serialization formats.

## API

- `dumps(obj, format: str, **options) -> str`
- `dumpb(obj, format: str, **options) -> bytes`
- `loads(s: str, format: str, **options) -> object`
- `loadb(b: bytes, format: str, **options) -> object`

format canbe:

| Format | Data format             | requires                |
|:-------|:------------------------|:------------------------|
| json   | `json`, `.json`         |                         |
| pickle | `pickle`                |                         |
| xml    | `xml`, `.xml`           |                         |
| json5  | `json5`, `.json5`       | install `anyser[json5]` |
| toml   | `toml`, `.toml`         | install `anyser[toml]`  |
| yaml   | `yaml`, `.yaml`, `.yml` | install `anyser[yaml]`  |
