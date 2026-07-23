# Agent quick reference — Trading repo

| I want to… | Do this |
|------------|---------|
| Run the overlay | Prompt: `Run covered-call delta band check` |
| Dry-run (closed markets) | Prompt: `Dry-run covered-call delta band check` |
| Change bands / gates | Edit `docs/strategy.md` |
| Change savings sweep ($ / date / bank) | Edit `docs/income-sweep.md` (manual monthly withdraw in Robinhood) |
| Change agent procedure | Edit `.cursor/skills/robinhood-delta-band-cc/SKILL.md` |
| Slack daily report / continue-stop | Edit prompts in `docs/slack-automations.md`, paste into [Automations](https://cursor.com/automations) (morning scoreboard + overlay actions) |

Skill: **robinhood-delta-band-cc** (Tier C auto-place within gates).

Slack: **two** automations — daily check (report only) + continue/stop (place). See `docs/slack-automations.md`.

Income sweep: **$3k/month → Amex savings on the 15th** if cash allows — see `docs/income-sweep.md`.

MCP: `user-robinhood-trading` · Account: Agentic `420763765` only.
