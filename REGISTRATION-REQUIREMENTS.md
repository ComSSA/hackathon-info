# Hackathon 2026 registration requirements

Reviewed 14 September 2026 through the user's signed-in Chrome session. This is a local implementation brief, not approved public website copy. Raw source exports remain in temporary storage. No private contact lists, staffing records, budgets, or unpublished problem statements are included here.

## Repository and implementation boundary

- This checkout is `https://github.com/ComSSA/hackathon-info`, serving `hackathon.comssa.org.au` according to `CNAME`.
- It contains a static `index.html`, CSS, images, and fonts. No application backend, authentication, database, package manifest, or `/register` implementation was found.
- The current registration link points to `/register` and is disabled with “Registrations Opening Soon!”. A comment proposes opening on September 18, but supplies no opening time or closing deadline.
- The user supplied `https://github.com/ComSSA/svelte.comssa.org.au`. Its main branch is an informational SvelteKit site on Cloudflare Pages; it does not own hackathon registration.
- After the user clarified that prior registration must be reused, the existing CTFd theme was located at `https://github.com/ComSSA/hackathon-theme` (commit `e08599c`). It includes registration, login, custom fields, and native create/join team templates. CTFd owns the database, authentication, validation, and organiser administration.
- The local CTFd checkout at `/Users/thomas/Desktop/Projects/CTFd` supplies version 3.8.1 for isolated testing. This is not verification of the deployed server version.
- Implementation is the overlay and small CTFd guard in `registration/`. No new Svelte account/database implementation is included.

## Sources

| ID | Source | Evidence and limitations |
| --- | --- | --- |
| S1 | [Hackathon 2026 folder](https://drive.google.com/drive/u/1/folders/1LjWVI_1QPq7iz-iV4ghOpXYHtHsKZwgL) | Current planning folder inspected. |
| S2 | [ComSSA Hackathon Documentation](https://docs.google.com/document/d/1scPhwzx_NPow2Z8qFAxeIVzrmfTk5ktUADDasxQ1M6U/edit) | Read text and embedded registration flowchart. Header says created July 2025, modified December 2025. Contains “Things to change from 2025” alongside December 2024 New Light templates. Folder location does not make every rule current. |
| S3 | [29 July 2026 initial meeting minutes](https://docs.google.com/document/d/1FQjXK6hwTV10WS8kpl837Mk3TNfLp3qzX9LELbAGx7E/edit) | Current meeting; venue plan and $4,500 prize pool recorded. Does not settle registration fields or deadlines. |
| S4 | [November 2026 logistics runsheet](https://docs.google.com/spreadsheets/d/1VHRlhN-n42XnkXB0FNjpqTeR-nF2_VlibD0MIrfiubw/edit) | Workbook exported read-only. “Hackathon Details” C7 gives 27/11–29/11; C11 says free and students only, no graduates; capacity row B10 has no value. Detailed day schedules show apparent carryover material and should not automatically become current requirements. |
| S5 | [2026 Tech folder](https://drive.google.com/drive/u/1/folders/1p-W00Lqwbvh92zYrEc96uhosLxVrZfRL) | Opened and found empty. No current field specification available here. |
| S6 | Local `index.html` | Existing public-facing copy, inspected directly; not independently confirmed as the live deployed version. |

## Requirements and confidence

| Topic | Evidence | Implementation consequence |
| --- | --- | --- |
| Event identity | S6: Chain of Collapse, ComSSA Hackathon 2026, Curtin University Bentley. | Reuse the existing event identity and branding. |
| Event dates | User confirmed November 27–29, 2026, Friday through Sunday. S4 agrees. | Confirmed; corrected local `index.html`. |
| Venue | S3: Clubs Hub on day 1; library level 7 Lantern/kitchen and level 4 rooms 434A/B on days 2–3. S4 summary location is blank; detailed schedules differ. | Use general Curtin location until the detailed venue schedule is confirmed. |
| Entry cost | S4 C11 explicitly says free. | No payment flow supported or needed by current evidence. |
| Eligibility | S4: current students, no graduates. S6: high school, university, TAFE etc., “above 16 years old”; no coding knowledge required. | Collect student eligibility; clarify whether 16-year-olds qualify and the date used to determine age before enforcing an age boundary. |
| Application meaning | S2 explicitly says register an expression of interest; acceptance must be processed and is not guaranteed. | Submission confirmation should say EOI received, pending review. Do not auto-accept applicants. |
| Solo/team entry | S6 permits solo applicants and says organisers can assign/help find teams. Teams are 3–6. | Support solo applicants and team affiliation, subject to existing platform workflow. Do not require solo applicants to invent a team. |
| Existing process | S2 historical flowchart: join Discord, enter Discord username, find/create a website team, then post name/team in Discord; solo applicants post an individual signup. | Evidence of the previous workflow, not approval to retain manual Discord steps or add Discord integration. |
| Registration window | S6 source comment: open September 18. S2 says do not accept after the deadline, but provides no current exact cutoff. | Confirm exact opening/closing date and time in Australia/Perth. Enforce on the server, including direct POST requests. |
| Capacity | S4 current capacity is blank. S2 historical terms refer to 12 teams. | Current limit and whether it limits EOIs or accepted places remain unknown. Do not assume 12 teams or 72 applicants. |
| Attendance | S6 requires at least one member at opening and the whole team at final presentations. S2 proposed changes say more than half at Friday finals; older templates require everyone at Sunday finals. | Confirm the current obligation before presenting mandatory consent language. |
| Terms and media | S2 includes old New Light terms and media consent language. | Obtain the current event terms; do not relabel old legal text as approved 2026 terms. |
| Organiser work | S2: process applications, organise teams, send acceptance/rejection messages. S4 Roles C7: manage sign-in/out and teams. | Reuse existing restricted organiser access for EOI review and team management. Event-day check-in can remain outside the first registration increment. |

## Fields

No complete current mandatory-field specification was found. S2's section called “Registration Fields” is an image of a historical workflow, not a field list.

Existing CTFd registration provides username, email, password and database-configured custom fields. The actual deployed custom-field configuration has not been inspected. Candidate additional fields for that existing mechanism:

- Participant name and email for identification and decision communications.
- Discord username, supported by S2's explicit tech task and flowchart.
- Current student declaration and institution/category sufficient to apply the approved eligibility rules.
- Solo/team choice and team association using the existing platform's team mechanism.
- Acceptance of the current approved event terms, recording the terms version and timestamp.
- Dietary requirements only if organisers need them at EOI time; current website promises dietary accommodation, but does not specify when to collect this information.

Do not collect date of birth, home address, student ID, emergency contacts, or third-party teammates' personal information by default. Check the existing workflow and actual organiser requirements first.

## Implementation using the prior registration system

- Reuse `ComSSA/hackathon-theme` registration and create/join team templates, including CTFd forms and CSRF nonce.
- Updated copy explains that an account/team is an EOI, not an accepted place, and supports solo applicants via the existing Discord organiser workflow.
- Passwords are not echoed into the form after server-side validation failure.
- A small CTFd plugin gates GET and POST registration on explicit timezone-aware opening/closing times, published terms, and a private required native terms field. No new authentication or database is introduced.
- Versioned terms acceptance is stored as a native CTFd custom-field entry; the CTFd account creation timestamp records when initial registration occurred.
- Native CTFd admin Users/Teams screens remain the organiser workflow. Use existing admin comments to record manual EOI decisions. This patch does not add an automated acceptance system or send emails.
- Global team size can be set to 6 through CTFd. A minimum size of 3 is an acceptance check rather than a creation constraint, allowing teams to assemble one member at a time.

## Verification

Tested against a clean copy of local CTFd 3.8.1 with the prior theme and isolated synthetic SQLite data. Seven integration tests passed: account/custom-field persistence and native create/join team flow; duplicate email rejection including case normalisation; invalid email and missing required fields; missing/stale terms; registration cutoff; CSRF; unauthorised admin access. Inspected desktop and narrow mobile screenshots; no horizontal overflow was detected at the observed 487 CSS-pixel mobile width. An empty browser submission focused the first required field. Live production behaviour and server version are unverified.

## Remaining configuration

### Hosting discovery, 14 September 2026

Read [Documentation - Tech Team](https://docs.google.com/document/d/1NaCG29-ow-qQb2SuXrnRxof85hqUpJEPhy_PwyUWasI/edit), whose Google Docs UI reports an edit two days ago. Individual sections include older material, so document recency does not prove every hosting detail is current.

- The Linode section says ComSSA generally hosts event servers on Linode, obtains its login from Bitwarden, and administers the VM over SSH with Docker Compose. It describes Kai deploying a Sydney Nanode for hackathon development, but gives no current instance ID or IP address.
- Cloudflare manages domain routing. The HTTPS section describes routing the hackathon subdomain to the server using an A record. The currently deployed public landing site is GitHub Pages; registration remains unavailable there.
- After the user signed in, the ComSSA Linode account was inspected: the Linodes inventory is empty, Owned by me has no custom images, and Recovery images has no recovery images. This does not rule out an exported CTFd backup elsewhere. No new server was purchased or created.
- User subsequently approved a 1 GB Linode until the end of the hackathon, with personal payment to be reimbursed. The unsubmitted creation form is now `comssa-hackathon-2026`: Sydney, Ubuntu 24.04 LTS, Nanode 1 GB / 1 CPU / 25 GB storage, disk encryption enabled, US$5/month before applicable taxes. Paid backups and other add-ons are off. No further spending approval is needed within this scope.
- Created and selected the free `comssa-hackathon-2026` firewall with default inbound DROP and outbound ACCEPT. It currently has no inbound allow rules. The server has NOT yet been created: root credential entry is pending user handoff, as required by the browser computer-use policy. No SSH key or cloud-init payload has been installed.
- Hosting is authorized through 29 November 2026. No automatic cancellation/deletion has been configured. Export required records and remove the billable instance after the event; powering it off alone must not be represented as cancellation.
- The handover confirms `hackathon-theme` is installed inside CTFd and annual `hackathon-202x` HTML is entered as CTFd pages.
- Its registration-only section also requires newly created users and teams to be hidden, and redirects successful authentication/team actions to an existing `/welcome` page. These requirements were not covered by the earlier seven local integration tests and must be reconciled with the real server configuration before release. The local overlay alone must not be described as a complete reproduction of the previous setup.
- The handover describes optional API-to-Google-Sheets synchronization. Inspect the existing deployment before deciding whether that organiser integration is required.
- Do not reuse example credentials or example secret keys from the installation tutorial in production.

Production update already completed: confirmed date and year correction deployed through GitHub Pages in commit `de596c22933b429868367c641e978746a1722397`. This did not deploy the CTFd overlay or enable registrations.

Use the existing CTFd deployment, theme and organiser accounts. Before opening real registration, confirm its URL/version, existing custom-field configuration, exact EOI window, age boundary (16 inclusive or strictly older), capacity/selection policy, current terms and attendance obligations. Event dates are now resolved. Keep native registration visibility private until configuration is complete. See `registration/README.md` for the concrete installation and preview instructions.

### Provisioning status

The user created Linode `105210463`, `comssa-hackathon-2026`, at `192.46.221.150`; verified running in Sydney on the Nanode 1 GB plan, 14 September 2026 at 23:29 AWST. Its firewall is `165215309` with inbound default DROP. CTFd is not installed yet. Weblish is open and waiting for the user to log in as root. Billing is on the existing ComSSA account and its existing default payment method, not a newly added personal payment method. No billing details were changed.

The local plugin now implements the handover privacy requirements before insertion and redirects challenge-screen destinations to an authenticated welcome route. Eight integration tests pass, including public profile denial for hidden users/teams and the login welcome redirect. These changes are local only and the earlier temporary release archive is stale.

### Installation progress after server login

Docker 29.1.3, Compose 2.40.3 and git installed successfully through the authenticated Weblish root console. Downloaded `ctfd/ctfd:3.8.7`, `mariadb:10.11` and `redis:7-alpine` successfully. Set hostname and added 1 GiB swap; observed total swap 1519 MiB. No application containers have been started and inbound firewall rules remain closed.

CTFd 3.8.7 at `ba53a21e53d1580f75e5186221563e030b839434` includes the upstream private-custom-field API disclosure fix. All eight registration integration tests pass against its source and pinned dependencies in `/tmp/comssa-ctfd-prod-venv`. Production compose syntax validation passed. Prepared `/tmp/comssa-production-release.tar.gz` (private full theme, current plugin, compose).

Pending user confirmation: install dedicated deployment SSH key from this Mac, restricted to current client IP and expiring after 29 November 2026. Public-key fingerprint `SHA256:2HsIQUzPB0q92OQlOo7Atd2Qkq+k6FFz+ieSs13JnxU`. The key has NOT been added to the server or Linode account. The local key pair is under `/tmp/comssa-deploy-access/`, not the repository. No firewall access has been opened.
