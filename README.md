# jsapi-skills

为 AI Agent 提供 MAPTEC JSAPI 服务能力的 Skill 集合，支持地图加载、交互、控件、事件、覆盖物、地点检索、路线规划等功能。

## 简介

`jsapi-skills` 把 Maptec JSAPI 能力整理成结构化文档，供 AI Agent 进行能力归类、API 选型、参数约束、生命周期清理和代码生成。核心入口是 `SKILL.md`，各项能力的详细规则在 `references/` 目录下。

## 功能列表

| 能力 | 说明 | 用户示例 | 详细文档 |
|---|---|---|---|
| 地图加载 | 创建地图实例，初始化加载地图 | “生成一个新加坡的地图” | [map.md](references/map.md) |
| 地图交互 | 拖拽、缩放、旋转、倾斜、手势控制、交互开关配置 | “禁止用户旋转或拖拽地图” | [operate.md](references/operate.md) |
| 地图控件 | 缩放导航、比例尺、全屏、指南针、鹰眼控件配置 | “在地图右下角添加比例尺控件” | [controls.md](references/controls.md) |
| 样式切换 | 白天 / 黑夜模式切换 | “将地图切换为黑夜模式” | [map-style.md](references/map-style.md) |
| 事件监听 | 地图点击、缩放变化、中心点变化、覆盖物点击等 | “点击地图获取当前位置的经纬度” | [events.md](references/events.md) |
| Marker | Marker 覆盖物 | “在点击位置增加 Marker 点” | [marker.md](references/marker.md) |
| 矢量覆盖物 | 点、线、圆、多边形的样式、数据与事件绑定 | “在地图上绘制一个半径 2000 米的圆形” | [overlay.md](references/overlay.md) |
| 信息窗口 | 信息窗口覆盖物 | “点击地图增加一个信息窗口” | [popup.md](references/popup.md) |
| 轨迹动画 | 关键帧轨迹、轨迹增长、沿线移动、车头朝向、视角跟随 | “让小车图标沿路线移动” | [track.md](references/track.md) |
| POI 检索 | 关键词、周边、类型、详情检索 | “搜索新加坡所有咖啡馆并标注” | [place-search.md](references/place-search.md) |
| 路线规划 | 驾车路线规划与展示 | “绘制 NUS 到乌节路的驾车路线” | [routing.md](references/routing.md) |
| 地理编码 | 地址转经纬度坐标 | “将新加坡摩天观景轮标注在地图上” | [geocoding.md](references/geocoding.md) |
| 逆地理编码 | 经纬度坐标转地址信息 | “将用户当前位置坐标转换为详细地址” | [re-geocoding.md](references/re-geocoding.md) |

## 安装

用于将 `jsapi-skills` 安装到本机 Agent Skills 目录，供 AI Agent 识别和使用。

### （1）通过 npm 包安装

```bash
npx @maptec/jsapi-skills install
```

安装完成后，默认目录为：`~/.agents/skills/jsapi-skills`

### （2）自定义安装目录

支持用环境变量 `MAPTEC_SKILL_INSTALL_DIR` 指定安装父目录：

```bash
MAPTEC_SKILL_INSTALL_DIR=/path/to/skills npx @maptec/jsapi-skills install
```

## 如何被 Agent 使用

1. 根据用户需求归类到功能列表中的一个或多个能力。
2. 按 `SKILL.md` 的能力路由，只读取相关的 `references/*.md`。
3. 使用参考文档中的真实 Maptec 类、方法、参数和生命周期规则。
4. 生成代码前说明命中的能力和使用的 API。
5. 生成代码时必须包含错误处理、空结果处理、事件解绑和资源清理。
6. 对不确定的能力标记 `需确认 Maptec 是否支持`，不要写成确定 API。

## 文件说明

- `SKILL.md`：Skill 主入口，定义功能列表、能力路由、实现流程和强约束。
- `references/`：各项能力的详细文档（地图、交互、控件、样式、事件、覆盖物、轨迹、检索、路线、地理编码等）。

## 约束

Agent 使用 Maptec JSAPI 时需遵循的坐标规则、API 选择、数据真实性、生命周期清理和未确认能力处理规则，详见 [SKILL.md](SKILL.md)。其中 POI、路线、地址和坐标必须来自 Maptec 服务或用户输入，不得伪造；示例代码使用占位 Key 或环境变量，不写入真实 Key。
