# Migration Stack-Patterns Reference

> This file is loaded on-demand by `iconix-migration-structural` (graph-assisted and code-walking modes both).
> It is reference material — stack-specific detection patterns and mapping conventions
> for Phases 1, 1b, 3, and 4. Do not embed these tables inline in the structural agent;
> read this file when entering the phase that cites the relevant block.
>
> Methodology rules (boundary/entity/controller stereotypes, noun-verb-noun, alternate
> courses, etc.) stay in the agent. This file holds **how to detect** these patterns
> in real codebases per stack — implementation aid, not ICONIX rule content.

---

## Block A — Entry-point taxonomy (Phase 1, both modes)

An entry point is a class where actor input (human, time, queue, system) crosses into
the system. Detect by **responsibility shape**, not class-name patterns. A candidate is
an entry point if **either** signal holds:

- **Inbound dispatch.** The class implements a framework's request-handler / consumer /
  hub / scheduled-job / CLI-command interface, or is decorated with a routing annotation.
- **No inbound graph edges / code calls.** Other code in the system does not import or
  call it; the framework reaches it through routing, configuration, or DI.

Read `iconix.config.yaml` `stack.language` and weight the most likely column first.

### Cross-stack pattern matrix

| Pattern | C# / .NET | Java | Python | Node.js / TS | Go | Ruby |
|---|---|---|---|---|---|---|
| Inbound HTTP | MVC `Controller`, `[ApiController]`, Razor Page, SignalR Hub, gRPC service | `@RestController`, `@Controller`, gRPC service | FastAPI / Flask routes, Django views, DRF `APIView` | Express/Koa/Fastify route, Nest `@Controller` | `http.Handler`, gin handler, gRPC service | `ApplicationController` subclass, Grape API |
| Inbound async / scheduled | `BackgroundService`, `IHostedService`, `IConsumer<T>`, Azure Function, Lambda | `@Scheduled`, `@KafkaListener`, `@JmsListener`, Spring Cloud Function | Celery task, FastStream consumer, APScheduler job | BullMQ worker, Lambda handler, KafkaJS consumer | goroutine workers, Sarama consumer | Sidekiq worker, ActiveJob |
| CLI / one-shot | `IHostApplicationLifetime` console app, `System.CommandLine` command | Spring `CommandLineRunner`, picocli command | Click / Typer command, `argparse` `main` | `commander` action, `yargs` handler | `cobra.Command`, `urfave/cli` | Thor command, Rake task |

### Graph node-type strings (graph-assisted mode)

Node-type strings produced by Graphify for entry-point candidates:
`controller`, `handler`, `route`, `endpoint`, `view`, `page`, `hub`, `cli`, `screen`,
`background_service`, `hosted_service`, `consumer`, `function_handler`, `worker`,
`listener`, `subscriber`, `job`.

Any `*_service` / `*Service` node with no inbound code calls is a candidate entry point;
mark for `[VERIFY]` review.

### Actor identification by entry-point type

For non-HTTP entry points the actor is typically *Time*, *Clock*, *MessageBus*,
*FileSystem*, or *another System* — name it explicitly in the UC, never default to
"User" silently.

---

## Block B — Cross-container boundary correlation (Phase 1b)

Three tables used at Steps 1, 2, and 3 of Phase 1b.

### B.1 — Inbound boundaries (Step 1: collect per container)

| Protocol | What to collect |
|---|---|
| HTTP | URL route pattern + HTTP method (normalize path params: `/orders/{id}` and `/orders/{orderId}` → `/orders/{param}`) |
| gRPC | Service name + method name |
| Message bus (consume) | Topic / queue / exchange name + consumer class |
| CLI | Command name |

### B.2 — Outbound cross-container calls (Step 2: collect per container)

| Protocol | What to collect |
|---|---|
| HTTP | Target URL pattern + HTTP method (from HTTP client usage) |
| gRPC | Stub service + method called |
| Message bus (publish) | Topic / queue published to |

**Graph-assisted mode:** query for outbound boundary nodes; filter to calls whose target
URL/topic is also an inbound boundary of another surveyed container.
**Code-walking mode:** grep for HTTP client usage patterns (`HttpClient`, `axios`,
`requests.post`, `fetch`, etc.) and extract literal or templated URLs; grep for message
publisher calls and extract topic names.

### B.3 — Match conditions (Step 3: pair inbound ↔ outbound)

| Protocol | Match condition | Confidence |
|---|---|---|
| HTTP | Exact normalized URL + method | HIGH |
| HTTP | Normalized URL match, method differs | MEDIUM |
| HTTP | URL prefix match (≥ 2 non-trivial path segments) | MEDIUM |
| gRPC | Exact service + method | HIGH |
| Message bus | Exact topic/queue name | HIGH |
| Message bus | Topic pattern (prefix/wildcard) | MEDIUM |

Unmatched outbound calls (no inbound in any surveyed container) → record as
**unmatched outbound**.
Unmatched inbound boundaries (no outbound caller found) → record as **unmatched inbound**.

---

## Block C — Source-construct → PlantUML mapping (Phase 3 Step 3)

Used by Phase 3 to turn source control flow into SD groups.

| Source construct | PlantUML construct |
|---|---|
| `if (cond) { A } else { B }` | `alt cond` / `else` block |
| `try { A } catch (Ex) { B }` | `alt happy path` / `else <Ex>` block; shade catch as alternate course |
| `foreach`, `while`, `do { … } while` | `loop` block |
| `Task.WhenAll(a, b)` | `par` block with `and` separator |
| `Task.WhenAny(a, b)` | `alt first-completes` block |
| `await a; await b;` (serial) | two sequential messages, no group |
| Fire-and-forget (`_ = task;`, not awaited) | message annotated `<<async / fire-and-forget>>`; flag `[VERIFY]` |
| Polymorphic dispatch on an interface | one message per known implementation each marked `[VERIFY]`, or a single message `<<polymorphic>>` if implementation set is open |

---

## Block D — Outbound boundary cross-stack patterns (Phase 4)

Used by Phase 4 to classify a class as **Outbound Boundary** when its imports indicate
external-system reach. Read `iconix.config.yaml` `stack.language` to weight the
relevant column.

### Universal signals (apply before falling back to the table)

- Imports an infrastructure namespace (HTTP client, DB driver, vendor SDK, message-bus
  client, blob storage, OS file system, email/SMS sender).
- Class name suffix matches an adapter pattern (`*Client`, `*Gateway`, `*Repository`,
  `*Store`, `*Dao`, `*Adapter`, `*Publisher`, `*Sender`, `*Driver`, `*Connector`, `*Provider`).
- Minimal conditional logic over domain values; mostly forwards / translates / serialises.

### Cross-stack illustration

| Pattern | C# / .NET | Java | Python | Node.js / TS | Go | Ruby |
|---|---|---|---|---|---|---|
| Outbound HTTP | typed `HttpClient`, Refit, RestSharp | `RestTemplate`, `WebClient`, Feign | `requests`, `httpx`, `aiohttp` | `axios`, `fetch`, `got` | `net/http.Client`, `resty` | `Net::HTTP`, Faraday, HTTParty |
| Database | `DbContext`, EF Core, Dapper, `IMongoCollection` | JPA `Repository`, `JdbcTemplate`, MyBatis | SQLAlchemy `Session`, Django ORM | Prisma, TypeORM, Mongoose, Sequelize | GORM, `database/sql`, sqlx | ActiveRecord, Sequel |
| Message publisher | `IBus` (MassTransit), `ServiceBusSender` | `KafkaTemplate`, `JmsTemplate` | `kafka-python`, `pika`, Celery `.delay()` | `kafkajs`, `amqplib` | Sarama producer, NATS client | `Bunny`, ruby-kafka |
| Vendor SDK | `StripeClient`, `BlobContainerClient`, `IAmazonS3` | AWS SDK, Twilio, Stripe | `boto3`, `stripe`, `sendgrid` | `aws-sdk` v3, `stripe` | AWS SDK Go, GCP client libs | AWS SDK Ruby, Stripe |
| File / blob | `File.WriteAllText`, `Stream`, `BlobClient` | `Files.write`, `S3Client` | `open(...)`, `boto3.S3.Client` | `fs.writeFile`, S3 SDK | `os.OpenFile`, AWS S3 SDK | `File.write`, AWS SDK |

**Rendering on diagrams:** stereotype outbound boundaries `<<outbound>>` on the RB;
place on the right side of their controller on the SD.

### Entity vs Controller (companion classifications)

These are listed here so the agent has a single Block-D read for stereotype classification:

**Entity (the domain object itself):**
- Persistence metadata native to the stack (annotations, attributes, decorators, struct
  tags, schema-derived models); methods (if any) operate only on the object's own state;
  no imports from infrastructure namespaces.
- Stack examples: C# `[Table]` / `[Key]` / EF POCO; Java `@Entity` / `@Table` /
  `@Document`; Python dataclass / Pydantic model / Django Model / SQLAlchemy declarative;
  TS TypeORM `@Entity` / Prisma model / Mongoose schema; Go struct with persistence tags;
  Ruby ActiveRecord model.

**Controller (logical software function):**
- Takes domain inputs, decides domain outcomes, only imports domain types — **no
  infrastructure imports**.
- Stack examples: `*Service` / `*Handler` / `*Validator` / command handlers / use-case
  classes / interactors / service objects.

**Disambiguation rule:** when a node's name suggests one stereotype but its imports
suggest another, trust the imports. A class named `OrderService` that imports `Stripe`
and `DbContext` is two outbound boundaries' worth of work, not a controller.
