# Legesi Visual Library — Publishing the recovered image bundle

The user has confirmed final-version selection and factual/rights clearance for the curated 18-image release. This file documents the final binary transfer into the existing website; the images are **not** part of this source-only PR.

1. Download `legesi_visual_publication_bundle_18.zip` from the corresponding ChatGPT conversation. It contains 18 approved image originals, 18 WebP web derivatives, 18 WebP thumbnails, and `candidate_catalogue_entries.json`.
2. In a local clone of `Superstar1910/Superstar1910.github.io`, create a new feature branch from current `main`.
3. Run:
   ```bash
   python scripts/import_visual_library_bundle.py /path/to/legesi_visual_publication_bundle_18.zip --dry-run
   python scripts/import_visual_library_bundle.py /path/to/legesi_visual_publication_bundle_18.zip
   python scripts/validate_visual_library.py
   ```
4. Inspect the image gallery, search and filters and check factual captions. Push the feature branch and open a pull request. Merge only after site quality checks pass.
5. Verify actual images render at https://legesi.xyz/visuals/ after the production deployment succeeds.

The importer refuses to overwrite existing images, validates presence of every referenced web image in the ZIP, rejects unsafe paths, guards catalogue uniqueness and keeps archived originals outside the public site by default.

**Important:** Adding this import helper does not upload any images or make them live. Do not claim the publication has succeeded until step 5 is confirmed.
