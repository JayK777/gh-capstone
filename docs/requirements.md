# Requirements — As a user, I want to reset my password via email so that I can regain access to my account

> Generated: 2026-08-03 | JIRA: EPMCDMETST-57902 | Priority: Low | Story Points: None

## User Story
**EPMCDMETST-57902**: As a user, I want to reset my password via email so that I can regain access to my account

*Description:*

*User Story*



As a registered user,

I want to receive a password reset link via email,

So that I can regain access to my account when I forget my password.



*Acceptance Criteria*



- Given I am on the login page, when I click "Forgot Password", then I see a form to enter my email address.

- Given I enter a valid registered email, when I submit the form, then I receive a password reset email within 2 minutes.

- Given I click the reset link in the email, when the link is valid (not expired), then I am taken to a page to enter a new password.

- Given the reset link is older than 24 hours, when I click it, then I see an "Link expired" error message.

- Given I enter a new password that meets complexity requirements, when I submit, then my password is updated and I am redirected to the login page.



*Notes*



- Password must be at least 8 characters, include 1 uppercase, 1 number.

- Reset link should expire after 24 hours.

- Only one active reset link per user at a time.

## Functional Requirements

- FR-01: The system shall fetch the JIRA user story identified by `EPMCDMETST-57902` and parse its fields.
- FR-02: The system shall scan all Python source files and extract module, class, and function docstrings.
- FR-03: The system shall generate a Markdown documentation file for each discovered module under `docs/api/`.
- FR-04: The system shall maintain a `docs/api_index.md` listing all generated module docs.
- FR-05: The system shall create a feature branch, push all generated artefacts, and open a GitHub PR.

## Non-Functional Requirements

- NFR-01: **Performance** — The full pipeline must complete within 120 seconds for a repository containing ≤ 500 Python files.
- NFR-02: **Security** — No credentials shall appear in generated documents, logs, or committed files.
- NFR-03: **Reliability** — All external API calls (JIRA, GitHub) shall retry up to 3 times on transient failure before raising.
- NFR-04: **Maintainability** — Each pipeline step is encapsulated in its own module; no step exceeds 200 lines.
- NFR-05: **Observability** — The pipeline emits structured log messages at INFO level for each step start/end.

## Acceptance Criteria

- AC-01: Given I am on the login page, when I click "Forgot Password", then I see a form to enter my email address.
- AC-02: Given I enter a valid registered email, when I submit the form, then I receive a password reset email within 2 minutes.
- AC-03: Given I click the reset link in the email, when the link is valid (not expired), then I am taken to a page to enter a new password.
- AC-04: Given the reset link is older than 24 hours, when I click it, then I see an "Link expired" error message.
- AC-05: Given I enter a new password that meets complexity requirements, when I submit, then my password is updated and I am redirected to the login page.

## Labels
None

## Out of Scope

- Confluence page sync
- Automatic code generation from requirements
- Non-Python source file parsing
