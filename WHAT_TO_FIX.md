# What Was Fixed

Following the original README did not produce a working local site. The failure
was caused by several independent issues in the scripts, path handling, file
discovery, and Markdown parser.

## Development script

- `main.sh` tried to serve `public/`, but the generator writes the site to
  `docs/`. It now serves `docs/` on port 8888.
- `main.sh`, `build.sh`, and `test.sh` now have shell entrypoints, stop when a
  command fails, and change to the repository directory before running. This
  makes them work even when invoked from another directory.

## Base paths and generated links

- `src/main.py` read `sys.argv[0]`, which is the Python script name, instead of
  the optional base-path argument. It now reads `sys.argv[1]` and defaults to
  `/` for local development.
- `src/page_generator.py` inserted the literal text `{basepath}` into generated
  links and image URLs. It now uses the supplied value and normalizes leading
  and trailing slashes.
- `build.sh` passed a malformed GitHub URL as the base path. Its default is now
  `/static_site_generator/`, and a different deployment base path can be passed
  as its first argument.

## Content discovery

- Recursive generation attempted to parse every file as UTF-8 Markdown. On
  macOS, a `content/.DS_Store` file therefore crashed the build with a
  `UnicodeDecodeError`.
- The generator now renders only `.md` files and skips hidden files and
  directories. Other content files no longer crash the build or produce bogus
  HTML output.

## Markdown parsing

- Fenced code blocks now accept an optional language identifier, such as
  `python` or `bash`, after the opening fence.
- Inline code is parsed before bold and italic syntax. Markdown characters
  inside backticks are therefore preserved as code instead of being treated as
  unmatched formatting delimiters.

## Documentation and tests

- Invisible zero-width characters were removed from the README's fenced code
  blocks, and the local URL and generated directory are now stated explicitly.
- Regression tests cover base-path rewriting, non-Markdown file handling,
  language-tagged code fences, and Markdown characters inside inline code.
- The tracked `docs/` site was regenerated with corrected deployment links.

## Verification

- `./test.sh` passes all 79 tests.
- `./main.sh` successfully generates and serves the site.
- The homepage, a nested blog page, and a static image all return HTTP 200 from
  `http://localhost:8888`.
