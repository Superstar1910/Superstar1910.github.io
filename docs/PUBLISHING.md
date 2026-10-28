# Publishing and distribution

Legesi.xyz is a static, Git-reviewed publication. It has no authenticated author
console or stored credentials for Substack, Medium, LinkedIn or X.

## Publish on Legesi.xyz

1. Add the article HTML and its reviewed record to `static/data/articles.json`.
2. Preserve the actual first-publication date and original source. Record
   alternate-platform dates in `syndications`, rather than changing history.
3. Relate it to one or more Work pages with `workUrls` and, where applicable, a
   verified `research.repository`. Mark externally hosted articles `native:false`.
4. Run `build_site.py`, `build_article_feeds.py` and all publication/editorial
   audits. Review and merge the PR. Publication waits for the exact-revision CI gate.

## Distribute

- RSS: `/writing/feed.xml` contains full HTML for 55 locally hosted publications,
  canonical links and stable item GUIDs. External-only entries are omitted.
- Medium: use its **Import a story** workflow with the Legesi.xyz article URL;
  review the imported content and canonical reference before publishing.
- Substack: its account **Settings → Import/Export → Import posts** accepts RSS
  imports. Review selected posts, publication dates and audience/email options.
  RSS availability alone does not create a continuously connected publishing job.
- LinkedIn and X: each native article has share links that open a composer. The
  signed-in person reviews and publishes there. Sharing a link is distinct from
  reproducing a long-form article; full LinkedIn articles still use its editor.

No account posts, newsletter emails or messages were sent during this review.
Automatic cross-posting is **not configured**. It would require an explicit
workflow, supported platform permissions and secure server-side credentials.
Do not put publishing tokens in client JavaScript or public repository files.

## Discovery and historical imports

The existing review-only discovery job checks Substack and Medium RSS and records
source failures explicitly. A truncated feed cannot prove lifetime completeness.
LinkedIn has no configured ingestion connection. Reconcile a complete author
export/list before claiming full coverage. Imported source snapshots stay under
`imports/`, which is excluded from the published artifact.

Official platform guidance checked 28 October 2026:

- https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium
- https://help.medium.com/hc/en-us/articles/214874118-Using-RSS-feeds-of-profiles-publications-and-topics
- https://support.substack.com/hc/en-us/articles/360037830351-How-do-I-import-my-posts-from-another-platform-such-as-Mailchimp-WordPress-Medium-or-Ghost
- https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin
