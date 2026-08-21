# Implementation Gotchas

Common technical traps in fullstack projects. Read this when writing §04 (Backend), §05 (Frontend), or §06 (LLM). Address applicable gotchas proactively — do not wait for the developer to discover them.

Each entry: what the trap is, why it happens, the fix. Examples use Python/TypeScript but the principle applies across stacks.

---

## Backend

### Middleware Order Is Counterintuitive

Most frameworks apply middleware in reverse registration order (last registered = outermost). This means CORS and auth middleware must be registered in a specific order or preflight/auth checks will fail silently. Always document the intended middleware stack order in the plan with a comment explaining why.

### ORM Async + Migration Tool Mismatch

When using an async ORM driver (asyncpg, aiomysql, motor), migration tools (Alembic, Flyway) default to synchronous connections and will fail or silently skip tables. The async engine must be explicitly bridged for migrations. Also: migration tools only discover models that have been imported — a missing import in the model registry means the table is invisible to autogenerate.

### Cached Config Breaks Tests

Singletons or cached config objects (e.g. `@lru_cache` on a settings loader) capture environment variables at first call. Tests that set env vars after import will silently use the wrong config — including connecting to the wrong database. Fix: mutate the cached instance in a test fixture before any test runs, or clear the cache between tests.

### Sequential ID / Index Assignment Under Concurrency

`SELECT MAX(n) + 1` without a row lock allows two concurrent transactions to compute the same next value. Use a database sequence, auto-increment column, or `SELECT FOR UPDATE` inside a transaction whenever assigning ordered identifiers.

### Resource Ownership: 403 Not 404

Returning 404 when a resource exists but belongs to another user leaks its existence. Always return 403 (or consistently 404 for both cases) — never 404 specifically for "exists but not yours".

### Implicit Resource Creation Race

Creating a resource on the first dependent action (e.g. creating a session when the first message is sent) leaves a window where a second concurrent action arrives before the resource exists. Create resources as an explicit user action; trigger dependent operations after creation confirms.

---

## Frontend

### Stable References for Framework Config Objects

Frameworks that accept component registries or config objects (graph libraries, data grid libraries, rich text editors) compare them by reference. Defining these objects inside a component means a new object is created on every render, causing the framework to tear down and remount all children. Define them at module level, outside any component.

### httpOnly Cookie Cross-Origin

Cookies set by the API are not sent by the browser on cross-origin requests unless `withCredentials: true` (or equivalent) is set on the HTTP client. Missing this causes auth to silently fail on every request.

### SSE: Native EventSource Limitations

The browser's `EventSource` API only supports GET requests and cannot send custom headers. Endpoints that require a POST body or auth header must use `fetch()` with `ReadableStream` parsing instead.

### React StrictMode Double-Invocation

In development, React 18 StrictMode intentionally mounts components twice. Any `useEffect` that triggers a one-time action (auto-send, session init, analytics event) will fire twice. Guard with a `useRef(false)` flag that is set on first invocation.

### Volume Mounts Shadow Installed Packages

Mounting a source directory into a container overwrites the container's package directory with the host's (which has none). Add an anonymous volume for `node_modules` (and `.venv` for Python) to shield them from the host mount.

---

## Auth & Sessions

### Token Refresh Race Condition

Multiple concurrent requests that each receive a 401 will each independently attempt a token refresh. The second refresh call typically fails (token already rotated) and logs the user out. Queue concurrent 401s and resolve them all with the result of a single refresh call.

### Refresh Cookie Parameter Mismatch

A refresh cookie set with different parameters in register vs login (different `path`, `samesite`, or `secure` values) results in two separate cookies — one of which is never sent. Set cookie parameters identically across all endpoints that issue it.

---

## LLM Integration

### API Role Constraints

Most LLM APIs only accept specific role values in the messages array (e.g. `user` and `assistant` only — no `system` role in the array). Messages stored with other roles in the database must be transformed before sending to the API. Plan this transformation in the build-messages function.

### Context Window Overflow

Long-running sessions will eventually exceed the model's context limit. Plan a truncation or summarisation strategy upfront: sliding window, summarise-and-replace, or drop oldest. Deciding this after the fact requires retrofitting the message model.

### SSE Heartbeat Composition

Composing a keep-alive heartbeat with a streaming LLM response is error-prone if done via task cancellation/restart. Use a shared async queue: one producer task writes LLM tokens, a second writes periodic pings, a single consumer reads from the queue and yields to the client.
