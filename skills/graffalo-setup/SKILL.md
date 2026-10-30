---
name: graffalo-setup
description: Check an installed Graffalo connection, identify the connected account and explain its capabilities. Use for first setup, wrong-account questions or connection troubleshooting; does not create a diagram by itself.
---

# Connect Graffalo

Use the installed Graffalo MCP connection. The public endpoint is
`https://graffalo.io/mcp`; a user-selected development or self-hosted connection
is a separate environment. Do not overwrite another connection or silently switch
accounts. This package does not require a model API key.

Discover `get_profile` and `get_connection_status`, then call both with `{}`.
The profile identifies the account represented by this connection; no user ID or
email selector is accepted. If multiple connections exist, use the one the user
requested. Show its display name and effective action categories, not credentials.
On an older server without these tools, say identification is unavailable and use
`get_schema` for compatibility; do not infer an account from diagram titles.

If authorization is required, use the client's native browser connection flow.
The user signs in and reviews the requesting client, scopes and document access.
Do not request passwords, authorization codes or bearer tokens in conversation.
Additional scopes require the user's consent; do not broaden access automatically.
An HTML Vercel login page means a protected/wrong deployment, not a Graffalo OAuth
response. The public plugin has no bypass header.

Free accounts can create and edit five custom diagrams plus built-in demos in the browser and through MCP/plugins. Unchanged demos do not count. The first saved edit turns a demo into a custom diagram using one slot, and a fresh original remains available. Further edits do not use more slots. Deleting a custom diagram frees a slot only once fewer than five remain. Existing work remains readable and editable after downgrade, even above five; new creation waits until below the limit. PNG, SVG and PDF support unlimited branded output. Set `branded:false` for a clean file: Free has one clean export per rolling 24 hours, shared across formats, browser and MCP. Exact-file retries and chunk retrieval do not spend twice. Mermaid source exports use the clean allowance. Imports and built-in chat still require trial/Pro. Matching OAuth scopes and document permissions always apply; existing preview-only grants must reconnect to authorize graph reads and edits. A read-only grant cannot edit. A document-restricted grant cannot create new documents.
The user can manage their plan in Graffalo's browser UI; do not collect payment
details, create checkout sessions or promise an automatic upgrade.

Report a concise connection result and ask which diagram task they want only if
they have not already supplied one. Do not create a disposable example merely
to prove setup. For a requested task, get the schema, use authorized documents,
and inspect the actual saved `render` result before claiming visual success.

To disconnect server access, point to Account settings → Connected agents in
Graffalo. Removing the plugin alone may leave the OAuth grant active. Revocation,
deletion and other account changes require the user's direct request.
