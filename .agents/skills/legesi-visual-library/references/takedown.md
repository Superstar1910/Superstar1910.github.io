# Removal from public and private retention

1. Identify the exact requested URL, catalogue ID, thumbnails, related pages and other current references. Treat withdrawal request as immediately overriding prior publication approval.
2. Ensure the original and thumbnails are transferred to an *existing verified private repository* outside any published/deployable path, with matching Git blob hashes; if no private destination is available, preserve in a non-public authorised export until it is.
3. Remove public catalogue records and corresponding derivative image files on a controlled branch. Do not create broken references or accidentally remove unrelated visuals.
4. Run validator/site-quality and merge after checks. Verify private archive exists and public `main` no longer contains either blob or catalogue entry.
5. Check the actual deployed URL and gallery, and document browser/CDN caches, Git history and forks separately. A public GitHub deletion does **not** erase earlier commits or previously downloaded copies. For urgent/sensitive data exposure consider repository history rewriting/security remediation, with explicit authorisation.
6. Record withdrawal, effective commit, private archive path and evidence in a restricted audit trail. Do not link private asset contents in the public gallery.
