# GitHub Pages + Supabase: zero-token exposure

This site is static (Jekyll on GitHub Pages). To avoid exposing any Supabase tokens on a fully public site:

- Do not use the Supabase JS client in the browser.
- Call Supabase Edge Functions over HTTPS instead. Keep the `service_role` key only in the Edge Function environment (secure on the server side).
- For build-time needs (GitHub Actions), store secrets in GitHub Secrets; never commit them.

## 1) Immediately rotate exposed keys (if any)

If any keys were committed or shared:
- In Supabase Dashboard → Project Settings → API: Regenerate the anon key.
- If you’re unsure what was exposed, rotate the JWT secret (this rotates all keys). You must then update your clients/functions.

## 2) Enforce Row Level Security (RLS)

Enable RLS per table and create explicit policies for allowed actions.

Check RLS status in SQL Editor:

```sql
-- See if RLS is enabled on your tables
SELECT relname AS table_name, relrowsecurity AS rls_enabled
FROM pg_class
WHERE relkind = 'r'
  AND relnamespace = 'public'::regnamespace
ORDER BY relname;
```

List policies:

```sql
SELECT schemaname, tablename, policyname, cmd, roles, qual, with_check
FROM pg_policies
ORDER BY schemaname, tablename, policyname;
```

Enable RLS if needed:

```sql
ALTER TABLE public.your_table ENABLE ROW LEVEL SECURITY;
```

Add/adjust policies to strictly allow only the minimal operations you need.

Note: `service_role` bypasses RLS by design; use it only inside server-side code you fully control (Edge Functions).

## 3) Use Supabase Edge Functions (no client tokens)

Example workflow:
1. Create an Edge Function in Supabase (e.g., `get_public_data`).
2. In the function, use `service_role` via environment variable (set in the Supabase dashboard). Validate inputs and return only safe data.
3. From your GitHub Pages site, call:
   `fetch("https://<PROJECT>.supabase.co/functions/v1/get_public_data")`
   No keys are embedded in the site.

This keeps all secrets server-side while allowing a public site to read data.

## 4) Optional: Build-time data fetch (GitHub Actions)

If you need to pre-render content:
- Store `SUPABASE_URL` and `SERVICE_ROLE` (or a dedicated token) in GitHub Actions Secrets.
- In your workflow, fetch data (ideally via your Edge Function) and write JSON files under `assets/json/`.
- Never echo secrets in logs; never commit them.

## 5) Local env files

Use `.env` locally (not committed) for tools or scripts. See `.env.example`.

## 6) Docker local preview

To run locally with Docker:
```bash
docker compose up --build
```
Then visit http://localhost:8080

## Quick checklist
- RLS enabled on all user-facing tables with minimal policies.
- No Supabase keys in the repository, HTML, JS, or devtools.
- Any data access happens via Edge Functions (no tokens in browser).
- Any build-time access uses GitHub Actions Secrets.

