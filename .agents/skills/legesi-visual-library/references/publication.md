# Public publishing workflow

## Canonical release
1. Inspect the existing catalogue/schema, current head of `main`, validator, gallery and intake workflow. Never add a competing gallery.
2. Prepare one WebP final and one WebP thumbnail for each approved distinct visual. Check text legibility, aspect ratio, EXIF/metadata and original fidelity.
3. Prepare `candidate_catalogue_entries.json` and a release manifest with original SHA-256, approval evidence, rights/privacy/factual review and intended paths. Do not include sensitive details in the public ZIP.
4. Validate ZIP filenames, CRC, entry sizes, safe paths, extension/MIME, count, unique IDs/public paths, hashes and required file pairs. Exclude private originals, source documents, secrets and restricted entries.
5. Upload release ZIP to `imports/` on an `intake/legesi-visuals-*` branch; the importer must auto-discover permitted ZIP names (including browser-renamed `(1)` variants), **not** commit the intake ZIP into `main`. One ZIP per intake commit is preferred.
6. Import into the branch, run `python scripts/validate_visual_library.py`, site-quality/browser checks, and inspect PR diffs. Rebase onto current `main` without overwriting newer unrelated site work; never force-merge conflicted branches.
7. After authorised merge, verify production `/visuals/` plus every representative image URL and thumbnail via real HTTP/browser loading. Distinguish deployed from merged and report failures honestly.

## Safety
User approval of a final version does not grant blanket permission to publish confidential or third-party content. Keep source originals in a separate private repo without public Pages configuration; the public repository may retain image bytes in its Git history after deletion. Do not rewrite rights status from a pending value merely to pass the importer. Avoid publishing stale financial metrics as present-day facts.

## Expected publication evidence
Catalogue entry count/IDs, ZIP checksum, CI job results, branch/PR/merge SHA, deployment run and live URL response with render test. Missing verification remains pending, never 'published'.
