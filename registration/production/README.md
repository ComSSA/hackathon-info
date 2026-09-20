# Production deployment

Approved host: Linode 105210463, `comssa-hackathon-2026`, Sydney Nanode 1 GB, US$5/month before tax, no paid add-ons. Hosting is authorized through 29 November 2026. Export required records and delete the billable instance after the event. No automatic cancellation is configured.

The compose file deliberately binds CTFd to loopback until initial setup is complete. MariaDB and Redis have no published ports. Memory and log rotation limits suit the approved small instance; verify memory under real load before opening registration. Use the prior complete theme as `theme/` with this repository's template overlays, and this repository's plugin as `plugin/`.

Generate independent random hex values for SECRET_KEY, DB_PASSWORD and DB_ROOT_PASSWORD on the server in a mode-600 `.env`. Never commit that file or a database export. Start with `docker compose up -d` and complete initial CTFd setup over authenticated access. Select the hackathon theme, teams mode, admin-only account/score/challenge visibility, and private registration. Do not install the preview's synthetic terms, fields or dates.

Use CTFd 3.8.7, whose release includes a private-custom-field API disclosure fix. The former local 3.8.1 environment is insufficient evidence for production. Re-run `registration/verify.py` against 3.8.7 and check the running containers.

Installed 14 September 2026 at `/opt/comssa-hackathon`: CTFd 3.8.7, MariaDB 10.11 and Redis 7 are running with named persistent volumes. Independent random secrets were generated on the server in a mode-600 `.env`. SSH is restricted to the approved current source IP and the dedicated key expires at 2026-11-29 16:00 UTC (midnight after 29 November in Perth). The server host key was verified through the authenticated console. Deployment key and pinned known_hosts are temporarily held under `/tmp/comssa-deploy-access` on this Mac, outside version control.

The private production setup is accessible on this Mac at http://127.0.0.1:5187/setup while the SSH tunnel is running. Its prepared form selects the hackathon theme, team mode, six-member limit, private registration, admin-only account/challenge/score visibility, and no newsletter or social sharing. These form settings are not persisted until the user creates the admin account and submits Finish.

Remaining steps: native admin setup, HTTPS/domain routing, current committee fields/terms/window, production flow checks, and an off-server backup destination. Paid Linode backups are disabled per the chosen budget.

## Cutover preparation, 15 September 2026

Native setup is complete: one admin, hackathon theme, teams mode, maximum six members, private registration and admin-only account/challenge/score visibility were verified from production configuration. No synthetic terms or opening dates were installed.

Nginx and Certbot are installed. The existing public homepage and assets are copied to `/var/www/comssa-hackathon`. `nginx-app.conf` is installed as `/etc/nginx/snippets/comssa-app.conf`; it serves the static homepage and proxies CTFd routes. The HTTP bootstrap site serves certificate challenges and redirects other requests to HTTPS. The temporary loopback-only port 8080 server allows pre-cutover checks. Firewall still permits only the approved SSH source, with no public web ports.

Verified through loopback Nginx: homepage 200, favicon 200, login 200, register 403 with closed announcement, admin 302 to authentication. CTFd setup is completed and no longer accessible as a public setup wizard.

Cloudflare login works through ComSSA Google SSO. Current rollback DNS value: `hackathon.comssa.org.au CNAME comssa.github.io`, proxied, TTL Auto. No DNS changes made yet. Planned cutover: change only this hostname to A `192.46.221.150`, enable web firewall ports, issue trusted certificate with automatic renewal and nginx reload, verify Cloudflare origin TLS validation, then verify public pages. Other ComSSA hostnames must remain unchanged. This public-exposure change awaits action-time browser-policy approval.

## Registration opened by organiser instruction

On 15 September 2026 the user explicitly requested the previous year's registration behaviour. Enabled `hackathon_native_registration=True` and native `registration_visibility=public`. This mode uses CTFd's own registration switch instead of the additional date/terms gate introduced during this implementation. The recovered theme provides username, email, password, native configurable extra fields, and create/join teams; its terms checkbox was conditional on organiser configuration. The old database custom fields were not recovered, so no claim is made that those database-only fields are reproduced. Current production has no extra required fields or published participation terms. Registration remains an EOI, not acceptance. Admin can close registration using native CTFd configuration. Homepage CTA is now active.

HTTPS cutover is complete: proxied A record points to 192.46.221.150, ports 80/443 are open, trusted Let's Encrypt certificate expires 13 December 2026, automatic renewal dry run succeeded, and hostname-scoped Cloudflare strict TLS rule is active.

Correction immediately after opening: restored the earlier preview's Discord username, School/TAFE/university, and Current student declaration as required native UserFields in production. These fields are private and editable so participants can correct their details, including accounts created before the fields were restored. Verified all three render as required on the public registration page. The earlier missing-database observation did not justify omitting these known fields; the earlier statement that production has no extra fields is now superseded. Synthetic test participation terms were not copied.

Organiser supplied the exact collection list: Name, Username, Email, Phone, School, Dietary Requirements?, Course and Year, DOB, Student ID, Discord Username, Joined Discord?. Applied via `configure-fields.py`. Username and Email remain native account fields; Name is a separate private full-name field. Existing school/Discord field IDs were retained by renaming them, preserving entries. All custom fields are private and editable. Text fields are required; dietary requirements accepts None. Joined Discord is an optional checkbox so No is a valid response. The existing current-student declaration remains. Verified all 11 requested labels on the public form.
