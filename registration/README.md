# Reuse the existing CTFd registration

This package extends [ComSSA/hackathon-theme](https://github.com/ComSSA/hackathon-theme/tree/e08599c), rather than creating a separate Svelte or TidyHQ registration system. The general ComSSA site is informational. The prior registration code lives in the CTFd theme; CTFd itself owns accounts, required custom fields, team creation/joining, storage, email verification, and admin access.

## Included changes

- `theme/templates/`: overlays on the existing registration and team templates. They retain CTFd forms and CSRF, clarify EOI versus admission, show 27–29 November 2026, and do not echo passwords back after errors. Shared presentation includes use the latest 2026 logo/poster, charcoal/orange palette and Aldrich headings from this site's `99708aa` revamp, with clearer form borders, spacing and responsive layout. No registration rules or field configuration changed in this visual update.
- `plugin/__init__.py`: a CTFd guard for the registration window and current terms, plus the documented registration-only behaviour: new applicants/teams are hidden before insertion, and challenge-screen redirects go to an authenticated `/welcome` page. Unconfigured or incomplete setup stays closed. CTFd still creates and stores the actual accounts and fields.
- `preview.py`: isolated, localhost-only CTFd preview with synthetic terms and custom fields. Creates a fresh temporary SQLite database, disables mail, and does not read existing applicant databases.
- `verify.py`: eight integration tests of actual CTFd registration, team, and admin routes.

## Install into the existing CTFd deployment

Do this first in a staging copy of the existing deployment. The Linode VM and its firewall have been created, but CTFd has not been installed there yet.

1. Keep CTFd **registration visibility private** while configuring. Confirm the deployed CTFd version and theme folder. The overlay was tested with CTFd 3.8.1 and the linked theme commit.
2. Copy all files under `theme/templates/`, including the two `components/` includes, onto the corresponding paths in the installed hackathon theme. Preserve its other templates and built assets. These template edits do not require rebuilding JavaScript or CSS.
3. Copy `plugin/` to `CTFd/plugins/hackathon_registration/`, and restart CTFd to load it. The guard deliberately fails closed until the following configuration is ready.
4. Reuse the current custom registration fields from CTFd Admin → Config → Custom Fields. Do not recreate fields if they already exist. Discord username, institution and current-student declaration are demonstrated locally, but the actual existing deployment must be inspected before choosing new required fields. Make personal fields non-public. Confirm the age rule before adding an age declaration.
5. Publish the approved event terms at `/terms`, with `draft=False`, and ensure it is readable without signing in. Set the CTFd config key `hackathon_terms_version` to the approved version identifier, for example an organiser-approved dated version.
6. Through native custom fields, add a **required boolean user field** named exactly `Participation terms (<version>)`, where `<version>` matches that config value. Set `public=False` and `editable=False`. Its description should state that the applicant accepts the current participation terms. This replaces the old browser-only `fields[tos]` checkbox and causes consent to be stored by CTFd with the account's other field entries. Retain previous version fields/entries for audit, but do not leave obsolete versions required for new applicants.
7. Set CTFd config keys `hackathon_registration_opens` and `hackathon_registration_closes` to confirmed ISO timestamps including `+08:00`. Opening is inclusive; closing is exclusive. Dates without timezone offsets or missing values are rejected. These keys are separate from competition start/end times. They can be set with the existing authenticated config API or `set_config` in the deployment's Flask shell, as appropriate to its operation.
8. Reuse teams mode and set `team_size=6` if that is not already configured. Teams can be created with one member and grow to 4–6; minimum size is checked by organisers at acceptance. Leave the applicant cap unset until organisers confirm whether the limit applies to EOIs or accepted participants.
9. Confirm existing mail delivery and verification settings, account/profile visibility, terms, and fields on staging. Use native admin Users and Teams screens to review records, reconcile solo applicants, and record decisions in admin comments. Account creation and team creation must not be treated as automatic acceptance. This package does not introduce a new review state machine or send decision emails.
10. After the deployment is ready and opening is authorised, enable native registration visibility. Keep this static site's CTA closed until `/register` is actually served by the existing CTFd host; do not assume GitHub Pages can serve CTFd routes. The final CTFd URL/reverse-proxy routing is not yet verified.

## Local preview and checks

The current test environment is `/tmp/comssa-ctfd-preview` with Python dependencies in `/tmp/comssa-ctfd-venv`. The original local CTFd source and databases were left untouched. Preview data is synthetic and stored under a new `/tmp/comssa-registration-demo-*` directory on each launch.

```sh
PYTHONPATH=/tmp/comssa-ctfd-preview /tmp/comssa-ctfd-venv/bin/python registration/verify.py
PYTHONPATH=/tmp/comssa-ctfd-preview /tmp/comssa-ctfd-venv/bin/python registration/preview.py
```

Open `http://127.0.0.1:5186/register`. It uses deliberately broad **test-only** registration dates and a `LOCAL-TEST-v1` terms field. These fixtures are never installed automatically into a real CTFd database.

To reproduce elsewhere, use an isolated CTFd 3.8.1 checkout and Python 3.11 environment, install its pinned `requirements.txt`, copy the prior theme into `CTFd/themes/hackathon`, apply this package's template overlays, and point `PYTHONPATH` at that checkout. The preview loads the guard directly while CTFd safe mode excludes other plugins.

## Limits to resolve before production

The user confirmed the event dates only. Exact EOI cutoffs, minimum-age interpretation, selection/capacity policy, current terms, and attendance obligations remain open. The former Linode server is absent. A fresh 1 GB Sydney VM now exists; CTFd installation is pending server login. Native sequential duplicate checks were exercised; concurrent load against the production database was not tested. Existing accounts on a reused event database may need an organiser-managed new-year EOI process because this overlay intentionally does not duplicate the existing account system.
