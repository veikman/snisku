# Change log
This log follows the conventions of
[keepachangelog.com](http://keepachangelog.com/).

## Unreleased

### Changed
- Deprecated the whitelist module in favour of the option module.

### Added
- An option module using a dataclass for privileged values and offering an
  OptionParameter class that can expose a tuple of such options, but does not
  otherwise use them.

### Developer
- More type annotations.

## Version 0.2.0
### Added
- Standard-library argparse integration.
- New types for real numbers.
- Documentation. This change log and an introduction by example.
