# 来源与交叉核对

核对日期：2026-10-13。以下是网站模型检查，并未运行实际游戏；“一致”仅指独立站点公开数据一致。训练器开发者为自己转换器实现的一手来源，不是游戏厂商认证。

- [KovaaK 官方转换器](https://kovaaks.com/kovaaks/sens-converter)：读取页面公开加载的 JS `/_next/static/chunks/7328-bdd2fcbc13d9681d.js` 的 `ag` 游戏数据与 `incrementFormula`。chunk 文件名可能变；更新时从页面重新找脚本。
- [Aiming.Pro 官方转换器](https://aiming.pro/mouse-sensitivity-calculator)：HTML 内嵌游戏 JSON 的 `name`、`yawdeg`、`yawrad`、`calculation`、`affectedByFov`。不能把弧度直接当角度，也不能跳过特殊 calculation。
- [KovaaK 原始原理说明](https://www.kovaak.com/sensitivity-matcher/)：鼠标计数×灵敏度×yaw 的转角模型。
- [Mouse-Sensitivity：Apex 与 CS 的测量讨论](https://www.mouse-sensitivity.com/forums/topic/5093-apex-legends-to-csgo/)：Drimzi 指出 Apex 腰射 0.022，ADS 另有缩放。

## 可用数据表

单位：灵敏度为 1 时，每鼠标计数旋转的水平角度；仅默认 PC 鼠标腰射。完整可执行数据见 games.json。

| 游戏 | KovaaK | Aiming.Pro | 结论 |
|---|---:|---:|---|
| Apex Legends | 0.022 | 0.022 | 一致 |
| CS2 / CS:GO | 0.022 | 0.022 | 默认 yaw 一致 |
| VALORANT | 0.06996 | 0.07 | 差 0.057%，采用前者并标近似 |
| Overwatch 2 | 0.0066 | 0.0066 | 当前转换器一致；不套用测试版测量 |
| COD BO6 / MW2019 / Warzone | 0.0066 | 0.0066 | 仅列明版本，不泛化整个系列 |
| Destiny 2 | 0.0066 | 0.0066 | 一致 |
| Deadlock | 0.044 | 0.044 | 一致；部分聚合站误写 0.022 |
| Fortnite | 0.005555 | 0.005555 | 百分数数值尺度 |
| Rainbow Six Siege | 0.018/π | 0.0001 rad = 0.018/π | 默认配置倍率下约 0.00572958 |
| Delta Force PC | 0.03 | 0.01 | 冲突，不能称准确 |

## 三角洲：不可丢失的条件

[KovaaK CS2→三角洲页面](https://kovaaks.com/kovaaks/sens-converter/cs2-to-delta-force)明确采用 0.03 和 0.7333 换算比例，与其公开 JS 一致。Aiming.Pro 的 Delta Force JSON 却为 0.01。未发现能证明差异由哪个具体版本或设置造成的资料，不猜原因。

[Mouse-Sensitivity 参数化转换器](https://www.mouse-sensitivity.com/n/cs2-to-delta-force/)列出主灵敏度、水平灵敏度、Monitor Distance Coefficient、FOV、分辨率。其中水平灵敏度默认 1，MDC 默认 1.33，FOV 默认 90；这是网站默认值，不能当用户当前值。[该站维护者的实测讨论](https://www.mouse-sensitivity.com/forums/topic/9303-delta-force-%E4%B8%89%E8%A7%92%E6%B4%B2%E8%A1%8C%E5%8A%A8/page/4/)指出 MDC 会影响腰射。仅拿固定 yaw 忽略这些参数不足以确认实际结果。部分页面直接打开会 403，搜索索引可读；不能声称运行过该动态计算器。

冲突网站已检查，但不作为通过校验的数据：

- [MouseTester](https://mousetester.io/sensitivity/delta-force-to-apex-legends/)写 0.022。
- [SensConvert.site](https://sensconvert.site/delta-force-to-apex/)写 0.0066，其示例表也有内部算术偏差，例如 DF 0.95 按该公式应为 Apex 0.285、800 DPI 下约 182.30 cm。
- [SensConverter.info](https://sensconverter.info/mouse-sensitivity-converter/delta-force-to-apex-legends/)也写 0.0066；两个站点相同数字不证明独立测量。

例：Apex 800×1.74 → 腰射目标 29.858934 cm/360。相同 DPI 下，KovaaK 模型给三角洲 1.276，Aiming.Pro 给 3.828。前者只能作为试用起点。若输入框只允许两位，可试 1.28，舍入会使模型转身距离约变为 29.77 cm；实际必须测量。

如用户要真正准确结果，获取当前参数后使用支持这些参数的可信转换器并交叉验证，或保持当前参数不变用三次手动 360° 测量校准。只有用户实际测量能检验其客户端实际表现。不要给未核实的“统一 MDC=0 即绝对准确”规则。
