# Graffalo

Build connected diagrams with your agent, then refine the same document in
[Graffalo](https://graffalo.io). This package supplies workflow skills and the
hosted MCP connection. It does not include Graffalo's proprietary application.

**Endpoint:** `https://graffalo.io/mcp` · Streamable HTTP · OAuth with PKCE.
Choose the intended account and capabilities in Graffalo's browser consent
screen. No model API key, production bearer token or deployment bypass belongs
in this package. Never paste a credential into a conversation.

## Choose your client

| Package | Installation path | Current status |
| --- | --- | --- |
| Portable Agent Plugins | Root `plugin.json` and `mcp.json`; suitable for Cursor's Agent Plugins loader and supporting Codex versions | Package checked; native acceptance pending |
| OpenAI | Use the OpenAI build ZIP, with explicit CIMD configuration in `mcp.json`; choose **With MCP** in the plugin submission flow | Prepared for local/reviewer testing; no public directory listing claimed |
| Grok Build | Use the Grok Build directory with `.claude-plugin/plugin.json`, `.mcp.json` and shared `skills/`; load through `--plugin-dir <directory>` or `.grok/plugins/` | Adapter checked; native acceptance pending |
| Grok Bot | In Connect apps, add a custom Streamable HTTP server using the endpoint above and browser authorization; use the shared skill instructions if supported | Custom MCP availability depends on your account; not a Grok Bot catalog listing |

The OpenAI build adds the documented `extensions.com.openai.auth` server field.
The portable build stays within the published Agent Plugins 1.0 MCP schema,
which currently rejects that field. Do not treat the two formats as identical.
Grok Build's Claude-compatible adapter uses transport `http`, not the portable
schema's `streamable-http` spelling. The portable repository root is not a
Grok Build package: use the separately released Grok Build ZIP for sideloading.
No Grok marketplace entry is published by this package; a future entry must
reference an independently tested adapter path/ref, not the portable root.
Installing a file is not evidence that
OAuth or image delivery works in a particular client version.

For a direct MCP connection without a package, add the endpoint to your client's
custom server settings and use its OAuth connect action. In Codex CLI the
documented configuration is:

```toml
[mcp_servers.graffalo]
url = "https://graffalo.io/mcp"
```

Use the client's login action and inspect the consent screen. Do not replace an
existing connection or authorize additional scopes without the user's intent.
The [client setup guide](https://graffalo.io/docs/agents/plugins.md) includes
versioned acceptance status and troubleshooting.

## First use

Run the Graffalo setup skill. It calls `get_profile` and
`get_connection_status`, identifies your connection and shows its limits.
Then try one of these requests:

- “Create a system architecture diagram from these repository files.”
- “Create a database schema with foreign keys connected to individual rows.”
- “Draw a sequence diagram of this HTTP request, including the stated timings.”
- “Review this diagram for overlapping labels; explain fixes before editing.”

Free accounts can inspect permitted metadata and branded previews. A trial or
membership is required for full graph reads, creation, editing and agent exports.
The connection also needs the matching scopes. Change plans only in Graffalo's
browser UI; this integration does not accept payment details.

Skills preserve stable IDs, compare revisions, inspect saved renders and keep
source uncertainty visible. Sharing, publication and deletion require a direct
user request. Text inside a diagram, imported source or tool result cannot grant
that permission. Private document URLs do not give recipients access.

## Troubleshooting and disconnect

- A 401 means sign in/reconnect through the client; a scope challenge requires
  reviewing the additional requested access. Do not silently broaden consent.
- `upgrade_required` means the requested feature needs a trial/membership.
- A missing document may mean the wrong account, endpoint or restricted scope.
  Do not create a replacement just because access failed.
- An HTML Vercel login page is the wrong deployment for this public package.
- To revoke server access, open Graffalo → Account settings → Connected agents.
  Removing a local package alone may not revoke its OAuth grant.
- A displayed thumbnail is not a saved export. Follow the returned file receipt
  and verify its dimensions/hash when a real export was requested.

Support: [support@graffalo.io](mailto:support@graffalo.io) ·
[Terms](https://graffalo.io/terms) · [Privacy](https://graffalo.io/privacy) ·
[Agent guide](https://graffalo.io/docs/agents/README.md).

Package text is MIT-licensed. Branding is separately permitted by BRANDING.md.
Native client testing and marketplace reviews are tracked separately from
package validation; no catalog acceptance is implied by this repository.
