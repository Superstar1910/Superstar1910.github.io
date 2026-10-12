# legesi.xyz

Public professional website for Kenneth Legesi. Static HTML and CSS; deployed by GitHub Pages. No build or JavaScript runtime required.

## Preview

Run `python3 -m http.server 8000` from the repository root and open http://localhost:8000. Check desktop and narrow mobile layouts, navigation, contact links, and the writing archive before merging.

## Content

`index.html` contains public biography, selected work, investment themes, and writing/media links. `static/css/storefront.css` styles the refreshed site. The existing portrait and favicon are reused. Older styles are retained but no longer loaded.

The redesign is proposed content for review, especially the selected-work role descriptions. Historical article titles retain the former Ortus name. No transaction details, financial values, family records or journal content belong in this repository.

## Deployment and rollback

Changes should use a feature branch and reviewed pull request. Preserve `CNAME` as `legesi.xyz`; confirm the existing Pages branch/source and HTTPS settings before merging. A merge may trigger the live deployment. Revert the redesign commit through a reviewed PR to restore the previous site. The pre-redesign source commit is `80075f22b6c6132ca3a58be054d3a37b1a2eb36f`.

The Personal Vault requires a separate private repository, deployment, authentication boundary and datastore. It is not implemented here.
