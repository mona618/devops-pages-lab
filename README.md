# Mona's DevOps Activity Lab

[![Activity, validation and Pages deployment](https://github.com/mona618/devops-pages-lab/actions/workflows/activity-log.yml/badge.svg?branch=main)](https://github.com/mona618/devops-pages-lab/actions/workflows/activity-log.yml)

**Owner:** HO TSAI-NI (`mona618`)  
**Course:** Software Development and Operations (DevOps)  
**Live site:** https://mona618.github.io/devops-pages-lab/

This site turns recent public GitHub activity into a published page. GitHub Actions validates the source, updates this README on a daily schedule or manual run, and deploys the rendered page to GitHub Pages.

## Recent public GitHub activity

<!--START_SECTION:activity-->
The first workflow run will add recent public events here.
<!--END_SECTION:activity-->

## How the page is produced

1. `scripts/update_activity.py` reads recent public events for `mona618` and updates the marked section above. When GitHub's public event feed is delayed, it uses verifiable public commits from this repository.
2. `index.md` includes this README, so the repository description and the Pages homepage use the same content.
3. A validation job checks the markers, homepage include, and basic HTML page.
4. A Jekyll build and the official Pages actions publish the tested site.

The workflow runs at **02:17 UTC (10:17 Taiwan time) each day** and also supports manual execution. A daily schedule keeps the page current without making frequent GitHub API requests. The Pages deployment runs in the same workflow as the activity update, so the published page is refreshed even when the update commit uses the built-in `GITHUB_TOKEN`.

Only public events are shown. The workflow accepts an optional repository secret named `TOKEN` for a user-owned PAT; without it, the built-in `GITHUB_TOKEN` is used. Private repository names and branch details are not published.

[Basic HTML example](https://mona618.github.io/devops-pages-lab/docs/) · [Workflow runs](https://github.com/mona618/devops-pages-lab/actions/workflows/activity-log.yml) · [Source repository](https://github.com/mona618/devops-pages-lab)

