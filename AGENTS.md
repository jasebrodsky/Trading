# Agent quick reference — Trading repo

| I want to… | Do this |
|------------|---------|
| Run the overlay | Prompt: `Run covered-call delta band check` |
| Dry-run (closed markets) | Prompt: `Dry-run covered-call delta band check` |
| Change bands / gates | Edit `docs/strategy.md` |
| Change agent procedure | Edit `.cursor/skills/robinhood-delta-band-cc/SKILL.md` |

Skill: **robinhood-delta-band-cc** (Tier C auto-place within gates).

MCP: `user-robinhood-trading` · Account: Agentic `420763765` only.

## Cursor Cloud specific instructions

- This is a **docs + MCP-driven agent** repo, not a compiled app. It contains only Markdown (`README.md`, `docs/strategy.md`, `runbooks/`, the skill). There is **nothing to install** — no package manager, build, tests, or linters. The startup update script is intentionally a no-op.
- The "application" is the `robinhood-delta-band-cc` skill run by the agent against the `user-robinhood-trading` MCP server. There is no server/dev process to start.
- Running the strategy (even a dry-run) **requires the `user-robinhood-trading` MCP server to be connected/authenticated in Cursor**. It is not available by default in a fresh Cloud Agent VM; if `GetMcpTools` shows no Robinhood tools, the run is blocked until the user connects it.
- Trigger prompts: `Run covered-call delta band check` (markets open) or `Dry-run covered-call delta band check` (markets closed → report only, never `place_option_order`).
- Real money. Trade the Agentic account `420763765` only; mask as ••••3765 in prose.
