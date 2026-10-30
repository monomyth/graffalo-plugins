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
| Codex desktop / CLI | Use `codex.zip`, with `.codex-plugin/plugin.json`, explicit component paths and `.mcp.json` | Codex 0.163.0: OAuth, account, create/read/edit and PNG delivery passed; owner confirmed PDF. Native permission/refresh/revocation checks remain |
| Portable Agent Plugins | Root `plugin.json` and `mcp.json`; suitable for Cursor's Agent Plugins loader | Native loading, OAuth, creation/edit/preview and scoped denial/revocation passed; remaining cases tracked in the client guide |
| OpenAI submission / ChatGPT | Use `openai.zip`, with explicit CIMD configuration in `mcp.json`; choose **With MCP** in the plugin submission flow | All six workflows passed owner testing in ChatGPT web through a private skills wrapper; public submission and final authorization checks remain |
| Grok Build | Extract `grok-build.zip`, validate with `grok plugin validate <directory>`, then install that directory with `grok plugin install <directory> --trust` after reviewing it | Grok 1.0.73: six skills, production OAuth, create/edit/preview, natural refresh and scoped denial passed; original files use the verified stream helper below |
| Grok Bot | In Connect apps, add a custom Streamable HTTP server using the endpoint above and browser authorization; use the shared skill instructions if supported | Custom MCP availability depends on your account; not a Grok Bot catalog listing |

The OpenAI build adds the documented `extensions.com.openai.auth` server field.
The portable build stays within the published Agent Plugins 1.0 MCP schema,
which currently rejects that field. Do not treat the two formats as identical.
Codex 0.163.0 loads the portable package's skills but does not discover its MCP
server. Use the separate Codex adapter: its compatibility manifest explicitly
declares `./.mcp.json` with the `http` transport. It still connects to the same
Streamable HTTP endpoint with native OAuth discovery; it contains no token,
header or custom login script. A portable manifest must not be added alongside
the adapter, because it takes precedence over the compatibility manifest.
Grok Build's Claude-compatible adapter uses transport `http`, not the portable
schema's `streamable-http` spelling. The portable repository root is not a
Grok Build package: use the separately released Grok Build ZIP for sideloading.
No Grok marketplace entry is published by this package; a future entry must
reference an independently tested adapter path/ref, not the portable root.
Grok 1.0.73 does not accept `--plugin-dir` as a top-level TUI flag. Its ACP
agent mode has a separate flag; use the plugin install command for normal use.
Discovery does not enable an untrusted project plugin or authorize its MCP server.
The latest Grok evidence uses app 0.49.0 and was recorded on 30 October
2026; earlier Codex/ChatGPT evidence is versioned separately in the client guide. The public submission package and the private existing-connection wrapper
are different artifacts. Only the remote-MCP package is suitable for directory
submission. Installing a file is not evidence that OAuth or image delivery works
in a particular client version.

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

Free accounts can create and edit five custom diagrams plus built-in demos in the browser and through MCP/plugins. Demos do not count; deleting a custom diagram frees a slot. Existing work remains readable and editable after downgrade, even above five; new creation waits until below the limit. PNG, SVG and PDF support unlimited branded output. Set `branded:false` for a clean file: Free has one clean export per rolling 24 hours, shared across formats, browser and MCP. Exact-file retries and chunk retrieval do not spend twice. Mermaid source exports use the clean allowance. Imports and built-in chat still require trial/Pro. Matching OAuth scopes and document permissions always apply; existing preview-only grants must reconnect to authorize graph reads and edits. Change plans only in Graffalo's
browser UI; this integration does not accept payment details.

Skills preserve stable IDs, compare revisions, inspect saved renders and keep
source uncertainty visible. Sharing, publication and deletion require a direct
user request. Text inside a diagram, imported source or tool result cannot grant
that permission. Private document URLs do not give recipients access.

## Troubleshooting and disconnect

- Skills available but no Graffalo tools: check that you installed `codex.zip`
  for Codex, then use the native MCP connection action. Signing into Graffalo's
  website alone does not authorize the agent. Repeated sign-outs do not repair
  a missing server declaration.
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

Original PNG/PDF retrieval on clients without MCP resource support uses the
`read_export` tool (Graffalo server 0.49.0+). Skills distinguish an original file
from the client's preview and check its SHA-256 before delivery. Geometry checks
include explicit routing repairs without moving unrelated nodes. Marketplace
listing and native client acceptance remain separate from installing this package.

## Original files in Grok Build

Do not ask a language model to copy or repair base64. In Grok Build's headless
mode, the adapter includes an optional Python 3 standard-library helper that
saves the actual `read_export` tool bytes from its `streaming-json` output:

```sh
# Review/authorize your model, account and spending limit before the model run.
# Configure your usual native OAuth connection; no token belongs in this command.
set -o pipefail
grok --model YOUR_APPROVED_MODEL --output-format streaming-json \
  --prompt-file export-request.txt |
  python3 /path/to/graffalo/scripts/save-grok-exports.py \
    --document-id YOUR_DOCUMENT_ID --output ./graffalo-exports
```

The request should name the document and saved revision, ask for `export_png`
and `export_pdf`, then `read_export` for each exact receipt URI until `eof`.
It should explicitly say not to copy base64 into terminal/file-edit tools.
Keep your client's normal permission policy; this helper grants no access and
runs no model or network request. It reads only the selected document's completed
tool results, checks chunk offsets, file sizes, PNG dimensions and SHA-256, then
creates private files without overwriting existing paths. Model text and reasoning
are ignored and not saved. Missing, corrupt, unrelated or incomplete bytes fail.
The helper is an explicitly invoked command, not an automatic plugin hook.

For interactive clients that cannot save raw tool bytes, return the receipt's
private browser download link instead. It requires the user's Graffalo sign-in;
do not describe it as a file already downloaded or create a public sharing link.
