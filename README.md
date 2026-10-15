# FPS Sensitivity Converter

An Agent Skill for converting **PC mouse sensitivity across FPS games**. It defaults to matching the same horizontal **cm/360** and accounts for source and target DPI. It asks for required inputs when a request depends on FOV, monitor-distance matching, or ADS/scopes, and calls out uncertain game data instead of presenting it as exact.

一个用于**跨 PC 鼠标 FPS 游戏换算灵敏度**的 Agent Skill。默认匹配水平 **cm/360**，支持不同来源和目标 DPI；FOV、屏幕距离或 ADS/瞄准镜匹配会先确认必要参数，并明确标出数据限制与冲突。

## Quick example

Ask your agent:

> Convert my Apex Legends sensitivity 1.74 at 800 DPI to VALORANT, keeping the same DPI and cm/360.

The skill should return a VALORANT sensitivity of about **0.547** and explain that this preserves turn distance, not necessarily perceived visual speed. VALORANT's listed yaw is marked approximate.

也可以直接问：

> 把 Apex 800 DPI、1.74 灵敏度换算到 VALORANT，沿用同 DPI 和 cm/360。

结果约为 **0.547**，并说明这是保持转身距离的结果，不保证视觉速度完全相同；VALORANT yaw 数据标注为近似值。

## Install

### Codex

```sh
gh skill install Alpherg951/fps-sensitivity-converter fps-sensitivity-converter --agent codex --scope user
```

Or use the cross-agent installer:

```sh
npx skills add Alpherg951/fps-sensitivity-converter --skill fps-sensitivity-converter --agent codex --global --yes
```

Manual install: copy `skills/fps-sensitivity-converter/` into `~/.codex/skills/fps-sensitivity-converter/`.

安装后可直接用自然语言提出游戏、灵敏度、DPI 和匹配目标。也可在对话中使用 `$fps-sensitivity-converter` 显式调用。

## What it does

- Converts the listed game's default PC mouse hipfire sensitivity using a yaw-based cm/360 model.
- Accounts for a different target DPI; if omitted, it assumes the target DPI is the source DPI and says so.
- Includes an offline Python CLI for the same yaw model and a local linear calibration formula.
- Chooses or explains a model for requests about cm/360, FOV/monitor distance, and ADS/scopes, and asks for missing required inputs.
- Preserves source confidence and conflicts in the result.

## Scope and limits

The bundled script calculates **horizontal hipfire cm/360 only**. It does not implement FOV/monitor-distance or ADS/scope conversion; for those requests, the skill asks for the model's required settings and uses a verifiable method when one is available. Do not interpret a formula result as an in-game measurement.

Included game profiles: Apex Legends, CS2, VALORANT, Overwatch 2, Call of Duty (BO6, MW2019, Warzone), Destiny 2, Deadlock, Fortnite, Delta Force PC, and Rainbow Six Siege. The profile notes are limited to specific versions and default settings where stated. Delta Force has conflicting public yaw values; its script result is explicitly provisional. See [`sources.md`](skills/fps-sensitivity-converter/references/sources.md) for attribution and qualifications.

## Offline converter

```sh
python3 skills/fps-sensitivity-converter/scripts/convert.py \
  --from apex --to valorant --dpi 800 --sens 1.74
```

Use `--to-dpi 1600` to specify a different target DPI. For calibration of a locally linear setting, use `--calibrate-current`, `--measured-cm`, and `--desired-cm`; keep DPI, FOV, MDC, and multipliers unchanged, then remeasure.

The game profile data was checked on 2026-10-13; recheck the cited sources before relying on it for a game update or custom configuration.

## Contents

- `skills/fps-sensitivity-converter/SKILL.md` — agent instructions and model-selection rules
- `skills/fps-sensitivity-converter/scripts/convert.py` — offline cm/360 converter
- `skills/fps-sensitivity-converter/references/games.json` — game aliases, yaw values, and confidence labels
- `skills/fps-sensitivity-converter/references/sources.md` — source notes and known conflicts

## License

MIT applies to the original files in this repository. External game data sources and third-party trademarks remain the property of their respective owners; see the source notes before reuse. See [LICENSE](LICENSE).
