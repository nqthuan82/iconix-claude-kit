# Test Plan — `<Release / Sprint>` — `<Date>`

## 1. Scope

| UC ID | Title | In scope? |
|---|---|---|
| UC-XXX | `<title>` | Yes / No |

## 2. TC inventory

| Type | Count | Notes |
|---|---|---|
| Unit (one per RB controller) | 0 | |
| Integration (boundary↔entity data flow) | 0 | |
| System (full UC scenarios) | 0 | |
| Acceptance (stakeholder-reviewed scenarios) | 0 | |
| **Total** | **0** | |

## 3. Automation status

| TC ID | Title | Type | Automated? | Test file |
|---|---|---|---|---|
| TC-XXX | `<title>` | unit / integration / system / acceptance | Yes / No | `<path/to/test_file>` |

## 4. Coverage status

Summary from `test-matrix.md`:

| UC ID | TCs exist? | All courses covered? | Blocker? |
|---|---|---|---|
| UC-XXX | Yes / No | Yes / No | Yes / No |

> Any UC with no TC is a **gate blocker** — the M3 gate will not pass until it is resolved.

## 5. Outstanding risks

| Risk | Affected TCs | Mitigation / Owner |
|---|---|---|
| `<e.g. test environment not ready>` | TC-XXX, TC-YYY | `<action / owner>` |
| `<e.g. TC not yet written>` | TC-ZZZ | `<owner — target date>` |

## 6. Test framework / dependencies

> Declare the libraries and infrastructure tests in this plan rely on.
> Read by the Reviewer at Phase 9 to verify TC implementation notes
> match what's actually in use. Drives docker-compose / CI configuration
> for integration and system tests.

| Layer | Library / tool | Source / version | Used by |
|---|---|---|---|
| Primary test framework | `<from iconix.config.yaml.stack.test_framework — e.g., xUnit>` | `<package + version>` | All TC types |
| Mocking / test doubles | `<NSubstitute / Moq / Mockito / Jest mocks>` | `<package + version>` | Unit TCs |
| Integration-test infrastructure | `<WebApplicationFactory<T> / TestServer / Testcontainers>` | `<package + version>` | Integration / system TCs |
| BDD framework | `<Reqnroll / SpecFlow / Cucumber / behave>` (or `(none)` if no acceptance-bdd TCs) | `<package + version>` | acceptance-bdd TCs only |
| Test data builders / fixtures | `<bogus / AutoFixture / factory-boy / faker.js>` | `<package + version>` | Unit / integration / system TCs |
| Database / persistence test doubles | `<Testcontainers SQL Server / sqlite-in-memory / EF Core InMemory>` | `<package + version>` | Integration / system TCs |
| HTTP client / browser automation | `<HttpClient / Playwright / Selenium / Cypress>` | `<package + version>` | System / acceptance TCs |

> If `iconix.config.yaml.stack.bdd` is `false` but you still have one
> or more `acceptance-bdd` TCs (per Tester agent's per-TC BDD
> convention), document the rationale here:
>
> *"This project's default is xUnit (`bdd: false`), but the
> stakeholder-signed acceptance TC BS-TC-101 uses Reqnroll for
> Given/When/Then readability during sign-off ceremonies. The
> Reqnroll dependency is scoped to the acceptance test project only
> and does not affect unit / integration / system test compilation."*
