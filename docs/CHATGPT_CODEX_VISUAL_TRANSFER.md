# ChatGPT → Codex visual publishing bridge

## Access boundary
The GitHub connector can commit repository text and Git blobs but cannot read the bytes of an image generated in a separate ChatGPT execution environment. A repository script cannot grant Codex access to ChatGPT conversation attachments. Do not claim direct transfer is working without a tested shared file source or authenticated upload endpoint.

## Supported workflow (Codex with file access)
1. Obtain the approved original image as an attached file or a file mounted in the Codex workspace.
2. Identify the exact approved file by preview and checksum; never select by filename alone.
3. Run `python scripts/import_visual.py --source /path/to/image.png --slug coffee-bean-economics --title "Who Captures the Economics of a Coffee Bean?" --project coffee-pricing-engine --caption "Illustrative Uganda-to-London coffee value-chain economics; gross receipts are not profits." --related-url /writing/who-captures-the-economics-of-a-coffee-bean/`.
4. Run `python scripts/validate_visual_library.py` and all existing site checks. Generate a thumbnail if desired, then update the catalogue thumbnail path to the real file.
5. Commit both the binary image and catalogue update on a feature branch, open a PR, review and merge.
6. Verify the public image, visual gallery, and article URLs after deployment.

## Future zero-click direct transfer
Requires a first-party supported ChatGPT attachment-to-Codex handoff, or an authenticated service with a short-lived upload URL and strict access control. Implementing only a GitHub Action or a Python importer does not solve this access boundary. Never expose GitHub tokens or make private conversation files publicly downloadable.
