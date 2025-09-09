# musicalmacaw

Show duration from image creation time till now in user-friendly format.

## Install

```bash
pip install musicalmacaw
```

## Run without installing

```bash
# Run directly from GitHub
uvx --from git+https://github.com/gkwa/musicalmacaw.git musicalmacaw /path/to/IMG_20250909_085620.jpg

# With options
uvx --from git+https://github.com/gkwa/musicalmacaw.git musicalmacaw -v /path/to/image.jpg
uvx --from git+https://github.com/gkwa/musicalmacaw.git musicalmacaw -t UTC /path/to/image.jpg
```

## Usage

```bash
# Basic usage - shows time since image was taken
musicalmacaw /path/to/IMG_20250909_085620.jpg
# Output: 8h32m

# With verbose output to see parsing details
musicalmacaw -v /path/to/image.jpg

# Override timezone (default: system timezone)
musicalmacaw -t UTC /path/to/image.jpg
musicalmacaw -t +0900 /path/to/image.jpg
musicalmacaw -t -0500 /path/to/image.jpg

# Multiple verbose levels for debugging
musicalmacaw -vv /path/to/image.jpg  # More debug info
musicalmacaw -vvv /path/to/image.jpg # Maximum debug info
```

## Supported Formats

- Android: `IMG_20250909_085620.jpg`
- iPhone: `IMG_2025-09-09_08-56-20.jpg`
- Generic: `2025-09-09_08-56-20.jpg`, `20250909_085620.jpg`

## Output Format

- Hours and minutes only: `1h30m`, `45m`, `2h15m`
- No seconds shown for clean output
- Shows `0m` for future timestamps

```

The key is using `uvx --from git+https://github.com/gkwa/musicalmacaw.git musicalmacaw` which will:
1. Clone the repo
2. Install it in a temporary environment
3. Run the `musicalmacaw` command (defined in your pyproject.toml entry point)

This lets people try it without installing anything permanently.
```
