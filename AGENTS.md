# AI Companion Trio

## Scope
- Maintain the trio pet package, editable animation frames, offline preview and build tool.
- Keep the sprite ID `ai-companion-trio` and v2 geometry: 1536 x 2288, cells 192 x 208.
- Preserve third-party notices. Artwork is CC BY-NC-SA 4.0; original code is MIT.
- Keep scripts and configuration ASCII. Chinese is appropriate for user-facing documentation and preview text.

## Validation
- Install Pillow from requirements.txt in an isolated environment.
- Run `python tools/build.py --check` to verify frames and the release atlas.
- Run `python tools/build.py --output build` to assemble an editable build.
- Visually inspect changed frames at native cell size and verify any generated atlas before a release.
- Keep credentials, local machine paths and private working logs outside the repository.
