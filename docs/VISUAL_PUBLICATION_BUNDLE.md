# Publish the approved 18-image Legesi Visual Library release

The final-version selections and factual/rights checks were confirmed by the user. The website release is not live until the images are committed, checks pass, PR is merged and deployment is verified.

## GitHub web intake (recommended)

1. Download **legesi_visual_publication_web_batch_18.zip** from the ChatGPT conversation (approximately 5.4 MB). This smaller ZIP contains 18 WebP images, 18 WebP thumbnails and 18 approved catalogue records; no private-source PNG originals.
2. In GitHub, create a new branch from latest `main` named `intake/legesi-visuals-2026-11-01`.
3. On that branch choose **Add file → Upload files** and upload the ZIP **into `imports/`** so its repository path is exactly `imports/legesi_visual_publication_web_batch_18.zip`. Commit the upload to the intake branch, **not main**.
4. The `Import approved visual-library bundle` GitHub Action triggers automatically, checks ZIP entries, imports all 36 image derivatives and 18 catalogue entries, runs `scripts/validate_visual_library.py`, deletes the intake ZIP and commits the results to that branch.
5. Open a PR from `intake/legesi-visuals-2026-11-01` into `main` and confirm all required Site Quality checks pass. Review gallery previews and the diff before merging.
6. After an authorised merge, verify new images actually render at https://legesi.xyz/visuals/.

**Do not upload the 43 MB source-originals package to the public repository.** The 5.4 MB web batch is the release file.

## Alternative from a local clone

```bash
git checkout -b feature/import-legesi-visuals
python scripts/import_visual_library_bundle.py /path/to/legesi_visual_publication_web_batch_18.zip --dry-run
python scripts/import_visual_library_bundle.py /path/to/legesi_visual_publication_web_batch_18.zip
python scripts/validate_visual_library.py
git add static/data/visual-library.json static/img/visuals
git commit -m "Publish 18 approved Legesi visuals"
git push -u origin feature/import-legesi-visuals
```

Open a PR, validate CI, merge and verify production. Both routes are repeatable and keep the existing catalogue and gallery architecture.
