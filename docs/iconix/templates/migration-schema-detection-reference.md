# Migration Schema Detection Reference

> This file is loaded on-demand by `iconix-migration-semantic` during Phase 5c Step 1.
> It is reference material — lookup tables for schema/ORM/enum detection across all supported stacks.
> Do not embed these tables inline in the semantic agent; read this file before Phase 5c begins.

---

## Track A — SQL files (cross-stack, always run)

1. Glob for `*.sqlproj` → parse `<Build Include="...">` XML to enumerate `.sql` files.
2. Glob for `**/*.sql` at each container's resolved source root.

For each `.sql` file found, classify by statement type:
- `CREATE TABLE [schema.]<name>` — entity definition (primary target)
- `CREATE PROCEDURE` / `CREATE FUNCTION` — named operation (extracts domain verbs)
- `CREATE VIEW` — derived concept (secondary, informational only)

---

## Track B — ORM model classes (language-aware)

Use the entity registry signal for the resolved `stack.language` to locate entity classes, then read class-level signals. For multi-language containers apply all matching rows.

### B1 — Entity registry: where to look

| Language | Registry signal | Entity file pattern |
|---|---|---|
| C# / .NET | `class * : *DbContext` → `DbSet<T>` properties; also `IEntityTypeConfiguration<T>` | `**/*Context.cs`, `**/*Configuration.cs` |
| Java | `@Entity` classes on Spring component-scan path (`persistence.xml` / `application.properties`) | `src/main/java/**/*.java` |
| Python (Django) | `INSTALLED_APPS` in `settings.py` → `models.py` in each app | `**/models.py` |
| Python (SQLAlchemy) | `declarative_base()` call → subclasses of the returned Base | `**/*.py` |
| PHP (Doctrine) | `doctrine.yaml` `mappings:` paths → `@ORM\Entity` / `#[ORM\Entity]` classes | `src/**/*.php` |
| PHP (Eloquent) | All classes extending `Illuminate\Database\Eloquent\Model` | `app/Models/**/*.php` |
| Ruby (Rails) | All classes extending `ApplicationRecord` | `app/models/**/*.rb` |
| TypeScript / JS (TypeORM) | `DataSource` / `createConnection` `entities:` config → `@Entity()` classes | `**/*.entity.ts`, `**/*.entity.js` |
| Go (GORM) | Structs embedding `gorm.Model` or with `gorm:"..."` struct tags | `**/*.go` |
| Go (Ent) | Each `ent/schema/*.go` file defines one entity schema | `ent/schema/*.go` |

### B2 — Entity and field signals

| Signal | C# / .NET | Java | Python | PHP | Ruby | TypeScript / JS | Go |
|---|---|---|---|---|---|---|---|
| **Entity decl.** | `DbSet<T>` | `@Entity` | `class *(models.Model)` / `class *(Base)` | `@ORM\Entity` / `extends Model` | `< ApplicationRecord` | `@Entity()` | `gorm.Model` embed / `ent/schema` file |
| **Table name override** | `[Table("n")]` / `.ToTable("n")` | `@Table(name="n")` | `Meta.db_table` / `__tablename__` | `@ORM\Table(name="n")` / `$table` | `self.table_name` | `@Entity({name:"n"})` | `gorm:"table:n"` / `.StorageKey("n")` |
| **Required / NOT NULL** | `[Required]` / `.IsRequired()` | `@NotNull` / `@Column(nullable=false)` | `null=False` (Django default) / `nullable=False` (SA) | `@Column(nullable=false)` / migration | `null: false` | `@Column({nullable:false})` / no `?` (Prisma) | `gorm:"not null"` / no `.Optional()` (Ent) |
| **Skip (not persisted)** | `[NotMapped]` / `.Ignore()` | `@Transient` | not declared on model | `@ORM\Transient` / not in `$fillable` | `attr_accessor` | `{select:false}` / `@ignore` (Prisma) | `gorm:"-"` / `.StorageKey("")` (Ent) |

### B3 — Relationship signals

| Relationship | C# / .NET | Java | Python | PHP | Ruby | TypeScript / JS | Go |
|---|---|---|---|---|---|---|---|
| **belongs-to (FK)** | `[ForeignKey]` / `.HasOne().WithMany()` | `@ManyToOne` / `@JoinColumn` | `ForeignKey("T")` (Django) / `ForeignKey("t.id")` (SA) | `@ORM\ManyToOne` / `belongsTo(T::class)` | `belongs_to :t` | `@ManyToOne(()=>T)` | `gorm:"foreignKey:"` / `.From("t")` (Ent) |
| **has-many** | `ICollection<T>` nav prop | `@OneToMany` | `related_name=` (Django) / `relationship()` (SA) | `@ORM\OneToMany` / `hasMany(T::class)` | `has_many :ts` | `@OneToMany(()=>T)` | slice + `gorm:"foreignKey:"` / `.To("ts")` (Ent) |
| **many-to-many** | `ICollection<T>` + junction | `@ManyToMany` + `@JoinTable` | `ManyToManyField(T)` (Django) | `@ORM\ManyToMany` / `belongsToMany(T::class)` | `has_and_belongs_to_many` | `@ManyToMany(()=>T)` | `gorm:"many2many:"` |
| **value object / embedded** | `[Owned]` / `.OwnsOne()` | `@Embeddable` / `@Embedded` | (no direct — nested serializer) | `@ORM\Embeddable` | (no direct) | `@Column({type:'json'})` | struct embedding |

### B4 — Enum / status field signals

| Stack | Enum signal | State ordering | `[VERIFY]` on sequence? |
|---|---|---|---|
| C# / .NET | C# `enum` type as entity property | Declaration order | **No — authoritative** |
| Java | Java `enum` + `@Enumerated(EnumType.STRING)` | Declaration order | **No — authoritative** |
| Python Django | `TextChoices` / `IntegerChoices` class | Class definition order | **No — authoritative** |
| Python SQLAlchemy | `Enum("v1","v2",...)` / Python `enum.Enum` | Argument / declaration order | **No — authoritative** |
| PHP | PHP `enum` used in `$casts` / `@Column(enumType=)` | Declaration order | **No — authoritative** |
| Ruby Rails | `enum :field, { name: int, ... }` | Hash definition order | **No — authoritative** |
| TypeScript (TypeORM) | TS `enum` + `@Column({type:'enum', enum: E})` | Declaration order | **No — authoritative** |
| TypeScript (Prisma) | `enum Name { VAL1 VAL2 ... }` in `schema.prisma` | Declaration order | **No — authoritative** |
| Go (GORM) | `const (A Type = iota; B; C)` | `iota` value order | **No — authoritative** |
| Go (Ent) | `field.Enum("f").Values("a","b","c")` | `Values()` argument order | **No — authoritative** |
| SQL-only (no ORM enum found) | `CHECK (col IN ('A','B','C'))` | Heuristic only — see Step 2A-c | **Yes — `[VERIFY]`** |

For all ORM enum signals: **do not add `[VERIFY]` on state sequence**; only flag individual transitions `[VERIFY]` where it is unclear which UC triggers them.

### B5 — Application-layer enum lookup (integer status columns only)

Run this sub-track only when Track A finds `CHECK (<col> IN (1,2,...))` (integer values) **and** Track B4 finds no ORM enum type for that column. Goal: locate an enum or constant declaration anywhere in the application code that maps those integers to names.

For each integer-only CHECK constraint column, search using the column name (and its entity-name-prefixed form, e.g., `Status` → also search `OrderStatus`) as the matching target:

| Language | File scope | Patterns to match |
|---|---|---|
| C# / .NET | `**/*.cs` | `enum \w*<ColName>\w*` with explicit `= \d+` member values; `const int \w+ = \d+` inside a class whose name contains the column name |
| Java | `**/*.java` | `enum \w*<ColName>\w*` with either `(\d+)` constructor values or ordinal order; exclude classes already in B4 |
| Python | `**/*.py` | `class \w*<ColName>\w*\(.*IntEnum\)` or `\(int.*Enum\)`; dict literal `\{\s*\d+\s*:\s*'` with var name matching column; `CHOICES = \[\(\d+,` tuples |
| PHP | `**/*.php` | `class \w*<ColName>\w*` containing `const \w+ = \d+` members |
| Ruby | `**/*.rb` | `\w*<COL_NAME>\w* = \{` hash with integer values outside a model's `enum` call |
| TypeScript / JS | `**/*.ts`, `**/*.js` | `enum \w*<ColName>\w*` with `= \d+` members; `const \w*<ColName>\w* = \{[^}]+:\s*\d` as-const objects |
| Go | `**/*.go` | `type \w*<ColName>\w* int` with `const (` block using `= \d+` or `= iota` |

**Column-to-enum name matching (heuristic, tried in order):**
1. **Exact match** — `OrderStatus` column → `OrderStatus` enum/type — highest confidence.
2. **Suffix match** — `Status` column → any `*Status`, `*State`, `*StatusCode` enum in the same package/namespace as the entity — medium confidence.
3. **Substring match** — `Status` column → `StatusCode`, `OrderState` elsewhere — low confidence.

**Confidence tiers and `[VERIFY]` rules:**

| Confidence | Criteria | `[VERIFY]` on sequence? | Label |
|---|---|---|---|
| **High** | Exact name match + enum covers all integer CHECK values | **No** | `EXTRACTED (B5-enum)` |
| **Medium** | Fuzzy name match, or enum does not cover all CHECK values | **Yes — confirm match** | `INFERRED (B5-enum)` |
| **Ambiguous** | Multiple candidates with no clear winner | **Yes — list all candidates** | `AMBIGUOUS (B5-enum)` |
| **Not found** | No candidate in codebase | — fall back to Step 2A-c SQL secondary signals | `INFERRED (SQL heuristic)` |

When multiple candidates exist, record all under a `Candidates:` field in the glossary and let the human reviewer select the correct mapping.

---

## Track C — Schema / migration DSL (language-aware)

### C1 — Single source of truth files (supersede Tracks A and B for their stack)

| File pattern | Stack | Format | Primary signals |
|---|---|---|---|
| `**/schema.prisma` | TypeScript / JS (Prisma) | Prisma SDL | `model Name { ... }` + `enum Name { ... }` |
| `db/schema.rb` | Ruby (Rails) | Ruby DSL | `create_table "name" do \|t\| ... end` — canonical schema dump |
| `ent/schema/*.go` | Go (Ent) | Go code | `.Fields()` + `.Edges()` + `.Indexes()` per entity file |

When a C1 file is found for a container, it supersedes Track B ORM signals for that container. Merge with Track A only for stored-procedure verb extraction (C1 files do not include SP names).

### C2 — Migration DSL files (use when no C1 file and Track B yields < 2 entities)

| File pattern | Stack | Format | Entity signal |
|---|---|---|---|
| `alembic/versions/*.py` | Python | Python | `op.create_table("name", ...)` |
| `**/changelog*.xml` / `**/changelog*.yaml` | Java / Any | Liquibase | `<createTable tableName="...">` / `createTable: tableName:` |
| `database/migrations/*.php` | PHP (Laravel) | PHP | `Schema::create('name', function (Blueprint $table)` |
| `db/migrate/*.rb` | Ruby (Rails) | Ruby | `create_table :name do \|t\| ... end` (only when `db/schema.rb` absent) |
| `src/main/resources/db/migration/V*.sql` | Java (Flyway) | SQL | Track A already covers `.sql`; confirms Flyway context |

Mark C2 entries as `INFERRED (migration DSL)`. Add `[VERIFY]` to business constraints found in C2 files — DSL may include DBA-only constraints with no domain meaning.

### Active priority when multiple tracks have results for the same container

```
C1 (SoT file)  >  Track B (ORM classes)  >  C2 (migration DSL)  >  Track A (SQL)
```

### Skip conditions (two independent gates)

- **Steps 1–3 skip:** if Track A, B, and C all yield zero entity definitions after all containers are scanned: log `Phase 5c skipped — no SQL, ORM, or migration DSL source detected` in the survey and handoff report, then move to Phase 6.
- **Steps 4–6 skip:** evaluated separately at the Step 4 gate — does not affect glossary generation.

---

## Step 2A — SQL column analysis reference

### Table name normalization rules

- Strip schema prefix (`dbo.`, `app.`, `cfg.`, etc.)
- Strip common technical prefixes: `tbl`, `Tbl`, `TBL`, leading `_`
- Convert `snake_case` → `PascalCase` (`order_line_items` → `OrderLineItem`)
- Singularize plural PascalCase names (`Orders` → `Order`, `Customers` → `Customer`)
- Mark as technical table (skip from glossary) when name matches:
  `(?i)(audit|log|history|migration|__EF|sysdiagram|dbo\.__)`

### SQL column attribute extraction

| Column attribute | What to extract |
|---|---|
| `PRIMARY KEY` / `IDENTITY` | Identity — skip (infrastructure, not domain attribute) |
| `FOREIGN KEY REFERENCES <T>(<C>)` | Relationship: this entity → referenced entity (becomes Given precondition) |
| `NOT NULL` (non-PK/FK) | Required attribute → business invariant |
| `CHECK (<col> IN ('A','B',...))` | Status/type enum → state machine candidate |
| `CHECK (<expression>)` | Business constraint (e.g., `Amount >= 0`) |
| `DEFAULT <value>` | Initial state / business default |
| `DECIMAL / MONEY / NUMERIC` | Monetary or numeric domain attribute |
| `DATETIME / DATE` | Temporal domain attribute |
| `BIT` | Boolean flag |

Drop columns matching `(?i)(CreatedAt|CreatedBy|UpdatedAt|UpdatedBy|ModifiedAt|ModifiedBy|RowVersion|Timestamp|IsDeleted|DeletedAt|DeletedBy|ConcurrencyToken)` — infrastructure, not domain vocabulary.

### State machine extraction rules

**String CHECK — `CHECK (<col> IN ('A','B','C',...))`:**
- Extract the enum values as candidate states.
- Attempt logical ordering using two signals (both `[VERIFY]`):
  1. `CREATE PROCEDURE` names: `sp_ApproveOrder` → verb `Approve` suggests a transition *to* `Approved`.
  2. Common state-name heuristics: `Draft` / `Pending` → early; `Active` / `Approved` / `Processing` → middle; `Completed` / `Done` / `Delivered` → end; `Cancelled` / `Rejected` / `Archived` → terminal.
- Mark ordering `[VERIFY]`. Drop this `[VERIFY]` if an ORM enum for the same column is found in Track B or C.

**Integer CHECK — `CHECK (<col> IN (1,2,3,...))`:**
- Record the integer set as candidate states; names not available from SQL alone.
- Delegate to Track B5 lookup; if B5 found a mapping, apply it using the B5 confidence tier.
- If B5 not found, attempt partial name recovery from secondary SQL signals:
  - **Named views:** `CREATE VIEW vw_<StateName><Entity> AS ... WHERE <col> = N` → `N` maps to `<StateName>`. Mark `[VERIFY — name inferred from view naming]`.
  - **Named stored procedures:** `sp_Set<Entity>To<StateName>` or `sp_<Entity><StateName>` → transition hint. Mark `[VERIFY — inferred from SP name]`.
- If no names recoverable: record states as `State_1`, `State_2`, ... with `[VERIFY — integer status, semantic names unknown]`.

---

## Step 2B — ORM entity analysis reference

### ORM entity name normalization

- Use the class / model name directly (ORM frameworks follow PascalCase singular naming).
- **Python:** convert lowercase model names to PascalCase.
- **Ruby (Rails):** use class name (`Order`), not table name (`orders`).
- **Go (Ent):** use the schema file name (PascalCase).

Filter technical entities: base classes not in the entity registry, `*Configuration` / `*Migration` / `*Base` / `*Mixin` / `*Abstract` classes, test fixtures, abstract classes.

### ORM enum state machine rules (B4 application)

- **ORM enum (any stack)** → **no `[VERIFY]` on sequence** — use declaration / argument / definition order as authoritative.
- **SQL `CHECK IN` only** → `[VERIFY]` on sequence (heuristic only).
- **Both ORM enum and SQL `CHECK IN` present** → ORM wins; drop sequence `[VERIFY]`.

Identify terminal states by name regardless of stack: `Cancelled`, `Rejected`, `Archived`, `Deleted`, `Failed`, `Expired`, `Closed`, `Void`.

Glossary format for ORM enum state machines:
```
**States (from <EnumTypeName> via <framework>, declaration order):**
Pending → Processing → Shipped → Delivered | Terminal: Cancelled
Source: <file>:<line> — EXTRACTED
```

### Value objects / embedded types

Using the "value object / embedded" signal from Table B3:
- The owned/embedded type is **not** listed as a standalone entity in the glossary.
- Its attributes are nested under the owning entity with a `(value object)` marker.
- Example: `Order.ShippingAddress` (value object) → Street, City, PostalCode, Country.
- **Stacks with no direct value object support** (PHP Eloquent, Ruby ActiveRecord, plain GORM): check for JSON column patterns that store a nested object; flag as `[VERIFY — confirm if value object or separate entity]`.

---

## Step 2C — Merge conflict resolution

| Conflict | Resolution |
|---|---|
| SQL table exists, no ORM entity | Check if junction or audit table — mark `[VERIFY]` |
| ORM entity exists, no SQL table | Migration not yet applied or code-first pending — mark `[VERIFY — schema not yet applied]` |
| SQL `CHECK IN` vs ORM enum for same column | **ORM enum wins** for state sequence; SQL CHECK IN is secondary confirmation; drop sequence `[VERIFY]` |
| SQL column name ≠ ORM property / field name | Use ORM name as domain vocabulary; note SQL column as alias |
| ORM skip marker on a SQL column | Skip from glossary (ORM intent overrides) |
| C1 file (SoT) conflicts with Track B ORM | C1 wins — use C1 entity definition exclusively |
| SQL integer `CHECK IN (1,2,...)` + B5 High (exact match) | Use B5 enum names in declaration order; no `[VERIFY]` on sequence; label `EXTRACTED (B5-enum)` |
| SQL integer `CHECK IN (1,2,...)` + B5 Medium (fuzzy match) | Use B5 enum names; add `[VERIFY — confirm enum-to-column match]`; label `INFERRED (B5-enum)` |
| SQL integer `CHECK IN (1,2,...)` + B5 Ambiguous | List all candidate enums; add `[VERIFY — multiple candidates]`; do not auto-select |
| SQL integer `CHECK IN (1,2,...)` + B5 not found | Fall back to view/SP heuristic names or `State_N` placeholders; `[VERIFY — integer status, semantic names unknown]` |

Record the merge decision per entity in the glossary under a `Source` field: `SQL`, `ORM (<framework>)`, `B5-enum (<file>)`, `schema.prisma`, `db/schema.rb`, `ent/schema`, or `merged`.
