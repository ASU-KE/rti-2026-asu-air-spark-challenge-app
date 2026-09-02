---
name: coding-standards
description: Baseline cross-project coding conventions — naming, readability, immutability, error handling, and code-smell review. Use when reviewing code quality or naming and no framework-specific skill (frontend-patterns, backend-patterns, api-design) applies.
metadata:
  origin: ECC
---

# Coding Standards & Best Practices

The shared floor for every project: baseline conventions that hold regardless of framework. For framework-specific depth, reach for the narrower skill:

- `frontend-patterns` — React, state, forms, rendering, UI architecture.
- `backend-patterns` / `api-design` — repository/service layers, endpoint design, validation, server concerns.
- [`FRAMEWORK-EXAMPLES.md`](FRAMEWORK-EXAMPLES.md) — worked React and REST API examples that pair with this baseline.

## Code Quality Principles

### Readability First

- Code is read more than written, so optimize for the reader.
- Name variables and functions for what they hold and do.
- Prefer self-documenting code over comments.
- Keep formatting consistent.

### KISS (Keep It Simple)

- Choose the simplest solution that works.
- Solve today's problem; add complexity only when it arrives.
- Optimize when measurements demand it.
- Favor understandable code over clever code.

### DRY (Don't Repeat Yourself)

- Extract common logic into functions.
- Create reusable components.
- Share utilities across modules.

### YAGNI (You Aren't Gonna Need It)

- Build features when they are actually needed.
- Start simple and refactor as requirements land.

## TypeScript/JavaScript Standards

### Variable Naming

```typescript
// PASS: GOOD: Descriptive names
const marketSearchQuery = "election";
const isUserAuthenticated = true;
const totalRevenue = 1000;

// FAIL: BAD: Unclear names
const q = "election";
const flag = true;
const x = 1000;
```

### Function Naming

```typescript
// PASS: GOOD: Verb-noun pattern
async function fetchMarketData(marketId: string) {}
function calculateSimilarity(a: number[], b: number[]) {}
function isValidEmail(email: string): boolean {}

// FAIL: BAD: Unclear or noun-only
async function market(id: string) {}
function similarity(a, b) {}
function email(e) {}
```

### Immutability Pattern (CRITICAL)

Create new objects with changes applied; spread the original rather than mutating it.

```typescript
// PASS: ALWAYS use spread operator
const updatedUser = {
  ...user,
  name: "New Name",
};

const updatedArray = [...items, newItem];

// FAIL: NEVER mutate directly
user.name = "New Name"; // BAD
items.push(newItem); // BAD
```

### Error Handling

Handle failures at every boundary: check responses, log context, and surface a clean message.

```typescript
// PASS: GOOD: Comprehensive error handling
async function fetchData(url: string) {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error);
    throw new Error("Failed to fetch data");
  }
}

// FAIL: BAD: No error handling
async function fetchData(url) {
  const response = await fetch(url);
  return response.json();
}
```

### Async/Await Best Practices

Run independent awaits in parallel with `Promise.all`.

```typescript
// PASS: GOOD: Parallel execution when possible
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats(),
]);

// FAIL: BAD: Sequential when unnecessary
const users = await fetchUsers();
const markets = await fetchMarkets();
const stats = await fetchStats();
```

### Type Safety

Give values precise types; reserve `any` for genuinely unknown shapes.

```typescript
// PASS: GOOD: Proper types
interface Market {
  id: string;
  name: string;
  status: "active" | "resolved" | "closed";
  created_at: Date;
}

function getMarket(id: string): Promise<Market> {
  // Implementation
}

// FAIL: BAD: Using 'any'
function getMarket(id: any): Promise<any> {
  // Implementation
}
```

## File Organization

Organize by feature/domain, with many small focused files.

### Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── api/               # API routes
│   ├── markets/           # Market pages
│   └── (auth)/           # Auth pages (route groups)
├── components/            # React components
│   ├── ui/               # Generic UI components
│   ├── forms/            # Form components
│   └── layouts/          # Layout components
├── hooks/                # Custom React hooks
├── lib/                  # Utilities and configs
│   ├── api/             # API clients
│   ├── utils/           # Helper functions
│   └── constants/       # Constants
├── types/                # TypeScript types
└── styles/              # Global styles
```

### File Naming

```
components/Button.tsx          # PascalCase for components
hooks/useAuth.ts              # camelCase with 'use' prefix
lib/formatDate.ts             # camelCase for utilities
types/market.types.ts         # camelCase with .types suffix
```

## Comments & Documentation

### When to Comment

Comment the WHY — the reasoning a reader cannot recover from the code itself.

```typescript
// PASS: GOOD: Explain WHY, not WHAT
// Use exponential backoff to avoid overwhelming the API during outages
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000);

// Deliberately using mutation here for performance with large arrays
items.push(newItem);

// FAIL: BAD: Stating the obvious
// Increment counter by 1
count++;

// Set name to user's name
name = user.name;
```

### JSDoc for Public APIs

````typescript
/**
 * Searches markets using semantic similarity.
 *
 * @param query - Natural language search query
 * @param limit - Maximum number of results (default: 10)
 * @returns Array of markets sorted by similarity score
 * @throws {Error} If OpenAI API fails or Redis unavailable
 *
 * @example
 * ```typescript
 * const results = await searchMarkets('election', 5)
 * console.log(results[0].name) // "Trump vs Biden"
 * ```
 */
export async function searchMarkets(
  query: string,
  limit: number = 10,
): Promise<Market[]> {
  // Implementation
}
````

## Performance Best Practices

### Memoization

```typescript
import { useMemo, useCallback } from "react";

// PASS: GOOD: Memoize expensive computations
// Copy before sorting - Array.prototype.sort mutates in place
const sortedMarkets = useMemo(() => {
  return [...markets].sort((a, b) => b.volume - a.volume);
}, [markets]);

// PASS: GOOD: Memoize callbacks
const handleSearch = useCallback((query: string) => {
  setSearchQuery(query);
}, []);
```

### Lazy Loading

```typescript
import { lazy, Suspense } from 'react'

// PASS: GOOD: Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'))

export function Dashboard() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart />
    </Suspense>
  )
}
```

### Database Queries

```typescript
// PASS: GOOD: Select only needed columns
const { data } = await supabase
  .from("markets")
  .select("id, name, status")
  .limit(10);

// FAIL: BAD: Select everything
const { data } = await supabase.from("markets").select("*");
```

## Testing Standards

### Test Structure (AAA Pattern)

```typescript
test("calculates similarity correctly", () => {
  // Arrange
  const vector1 = [1, 0, 0];
  const vector2 = [0, 1, 0];

  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2);

  // Assert
  expect(similarity).toBe(0);
});
```

### Test Naming

Name each test for the behavior it pins down.

```typescript
// PASS: GOOD: Descriptive test names
test("returns empty array when no markets match query", () => {});
test("throws error when OpenAI API key is missing", () => {});
test("falls back to substring search when Redis unavailable", () => {});

// FAIL: BAD: Vague test names
test("works", () => {});
test("test search", () => {});
```

## Code Smell Detection

Scan for these anti-patterns. The review is complete when every function has been checked against all three: length, nesting depth, and unnamed literals.

### 1. Long Functions

Keep functions under ~50 lines by extracting steps into named helpers.

```typescript
// FAIL: BAD: Function > 50 lines
function processMarketData() {
  // 100 lines of code
}

// PASS: GOOD: Split into smaller functions
function processMarketData() {
  const validated = validateData();
  const transformed = transformData(validated);
  return saveData(transformed);
}
```

### 2. Deep Nesting

Flatten with early returns.

```typescript
// FAIL: BAD: 5+ levels of nesting
if (user) {
  if (user.isAdmin) {
    if (market) {
      if (market.isActive) {
        if (hasPermission) {
          // Do something
        }
      }
    }
  }
}

// PASS: GOOD: Early returns
if (!user) return;
if (!user.isAdmin) return;
if (!market) return;
if (!market.isActive) return;
if (!hasPermission) return;

// Do something
```

### 3. Magic Numbers

Name literals as constants that state their meaning.

```typescript
// FAIL: BAD: Unexplained numbers
if (retryCount > 3) {
}
setTimeout(callback, 500);

// PASS: GOOD: Named constants
const MAX_RETRIES = 3;
const DEBOUNCE_DELAY_MS = 500;

if (retryCount > MAX_RETRIES) {
}
setTimeout(callback, DEBOUNCE_DELAY_MS);
```
