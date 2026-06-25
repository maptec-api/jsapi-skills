---
name: jsapi-skills
description: 为 AI Agent 提供 MAPTEC JSAPI 服务能力的 Skill 集合，支持地图加载、交互、控件、事件、覆盖物、地点检索、路线规划等功能，让AI能够精准选择类、方法、参数、生命周期和清理方式。
---

# Maptec JSAPI Skill

为 AI Agent 提供 MAPTEC JSAPI 服务能力的 Skill 集合，支持地图加载、交互、控件、事件、覆盖物、地点检索、路线规划等功能，让AI能够精准选择类、方法、参数、生命周期和清理方式。

## 安装接入

支持 Script 和 npm 两种方式接入 MAPTEC JSAPI，Script 适合用于 HTML 页面使用，npm 适合用于工程化项目使用。

### Script 接入

```html
<script src="https://test-lbs.maptec.com/demo/lib/Maptec-dev.js"></script>
```

Script 加载完成后，通过全局对象 `Maptec` 使用 JSAPI。

### npm 接入

```bash
npm i @maptec/maptec-js
```

安装完成后，可执行以下命令检查依赖是否安装成功：

```bash
npm ls @maptec/maptec-js
```

## 鉴权

- Header：`Authorization: Bearer $MAPTEC_JSAPI_KEY`
- `MAPTEC_JSAPI_KEY` 从环境变量获取
- 若未设置，提示用户执行：
  `export MAPTEC_JSAPI_KEY=<你的 MAPTEC JSAPI Key>`

## 功能列表

| 能力 | 说明 | 用户示例 |
|---|---|---|
| 地图加载 | 创建地图实例，初始化加载地图 | “生成一个新加坡的地图” |
| 地图交互 | 支持地图拖拽、缩放、旋转、倾斜、手势控制、交互开关配置 | “禁止用户旋转或拖拽地图” |
| 地图控件 | 支持缩放导航、比例尺、全屏、指南针、鹰眼控件的位置配置、添加、移除与清理 | “在地图右下角添加比例尺控件” |
| 样式切换 | 支持白天、黑夜模式切换 | “将地图切换为黑夜模式”“增加一个按钮切换白天和黑夜地图” |
| 事件监听 | 支持地图事件和用户交互监听，配置地图点击、缩放变化、中心点变化、覆盖物点击等事件监听代码 | “点击地图获取当前位置的经纬度”“监听地图缩放级别变化” |
| Marker | 面向业务可视化场景，支持 Marker 覆盖物 | “在点击位置增加Marker点” |
| 矢量覆盖物 | 面向业务可视化场景，支持点、线、圆、多边形矢量覆盖物的样式配置、数据绑定、事件绑定 | “在地图上绘制一个半径2000米的圆形” |
| 信息窗口 | 面向业务可视化场景，支持信息窗口覆盖物 | “点击地图增加一个信息窗口展示当前位置经纬度” |
| 轨迹动画 | 面向动态轨迹可视化场景，支持关键帧轨迹、行驶轨迹增长、图标沿线移动、车头自动朝向、视角跟随 | “让小车图标沿路线移动”“实现轨迹回放并支持暂停、继续、停止” |
| POI检索 | 面向 POI 检索场景，支持关键词检索、周边检索、类型检索、详情检索 | “搜索新加坡所有咖啡馆并标注在地图上”“乌节路附近的餐厅” |
| 路线规划 | 面向路线规划场景，支持驾车路线规划和路线展示 | “绘制一个新加坡国立大学到乌节路的驾车路线” |
| 地理编码 | 面向地址解析场景，支持将地址转换为经纬度坐标 | “将新加坡摩天观景轮标注在地图上” |
| 逆地理编码 | 面向坐标反查地址场景，支持将经纬度转换为地址信息 | “将用户当前位置坐标转换为详细地址” |

## 能力路由

按需只读取相关参考文档：

- **地图加载**：`references/map.md`。
- **地图交互**：`references/operate.md`。
- **地图控件**：`references/controls.md`。
- **样式切换**：`references/map-style.md`；运行时样式切换使用 `map.setStyle(styleID)`。
- **事件监听**：`references/events.md`；涉及 Marker、矢量覆盖物或信息窗口事件时读取对应能力文档。
- **Marker**：`references/marker.md`。
- **矢量覆盖物**：`references/overlay.md`。
- **信息窗口**：`references/popup.md`。
- **轨迹动画**：`references/track.md`；如果轨迹来自真实道路，先读取 `references/routing.md`。
- **POI检索**：`references/place-search.md`；需要填写或匹配 POI `type/types` 时读取 `references/poi-categories.md`；地点范围不明确或附近检索需要中心点时读取 `references/geocoding.md`。
- **路线规划**：`references/routing.md`；起终点是地址或地名时先读取 `references/geocoding.md`。
- **地理编码**：`references/geocoding.md`；需要标注结果时读取 `references/marker.md`。
- **逆地理编码**：`references/re-geocoding.md`；需要用户当前位置时结合浏览器 `navigator.geolocation`。

## 实现流程

1. 先把用户需求归入一个或多个功能列表条目。
2. 明确输入：地点名、地址、坐标、POI 类型、半径、路线起终点、样式模式、控件位置、交互开关、事件类型。
3. 只使用已确认能力：
   - 地图加载：`Maptec.Map`
   - 地图交互：`MapOptions` 交互字段、`map.interactive`、`minZoom/maxZoom`、`minPitch/maxPitch`、`maxBounds`、`jumpTo/easeTo/flyTo/fitBounds`
   - 地图控件：`NavigationControl`、`ScaleControl`、`FullscreenControl`、`CompassControl`、`HawkeyeControl`
   - 样式切换：初始化 `style`；运行时使用 `map.setStyle(styleID)`
   - 事件监听：`map.on`、`map.once`、`map.off`、Marker/矢量覆盖物/信息窗口 `on/off`
   - Marker：`Maptec.Marker`
   - 矢量覆盖物：`Maptec.CircleOverlay`、`Maptec.PolylineOverlay`、`Maptec.PolygonOverlay`、`Maptec.GeoJSONOverlay`
   - 信息窗口：`Maptec.Popup`
   - 轨迹动画：`PointKeyFrameTrack`、`PolylineKeyFrameTrack`、`CameraKeyFrameTrack`、`CameraOrbitKeyFrameTrack`
   - POI检索：`Maptec.PlaceSearch`
   - 路线规划：`Maptec.Driving`；货车路线才使用 `Maptec.TruckDriving`
   - 地理编码：`Maptec.Geocode.getLocation`
   - 逆地理编码：`Maptec.Geocode.getAddress`
4. 生成代码前说明命中的能力、使用的类/方法、异步流程和需要用户确认的不确定点。
5. 生成代码时包含错误处理、空结果处理、分页限制、事件解绑、覆盖物/控件清理和视图适配。

## 强约束

- 地理坐标统一使用 `[lng, lat]`，不要使用 `[lat, lng]`。
- 不要发明 Maptec 不存在或未在当前文档确认的类、方法、参数或事件名。
- **必须严格按照 reference 文档中定义的响应字段名访问 API 数据**，不得套用其他地图 SDK（如 Google Maps、Mapbox）的字段名惯例。各服务响应字段名不同，严禁混用：

| 服务 | 结果列表字段 | 坐标字段 | ❌ 常见错误 |
|---|---|---|---|
| POI 检索 `PlaceSearch` | `result.places` | `place.location`（直接含 `latitude`/`longitude`） | ~~`result.results`~~、~~`place.geometry?.location`~~ |

- 真实 POI 必须使用 `Maptec.PlaceSearch`，不要伪造咖啡馆、餐厅、酒店等真实数据。
- POI `type/types` 必须来自 `references/poi-categories.md` 的 Maptec 类目值；不要使用未确认的通用词如 `school`、`restaurant`、`hotel`、`parking`，除非该值在类目补充中明确存在。不确定时只用关键词检索，不要强塞类型过滤。
- 地址、地名、地标转坐标必须先用 `Maptec.Geocode.getLocation`。
- 坐标反查地址必须用 `Maptec.Geocode.getAddress`。
- 真实驾车路线必须使用 `Maptec.Driving` 或 `Maptec.TruckDriving`，不要用手写折线冒充路线规划。
- 路线规划结果必须使用 `Maptec.Marker` 增加起终点方向图标，起点标识“起”，终点标识“终”，并在清理阶段移除这两个 Marker。
- Marker、Popup、CircleOverlay、PolylineOverlay、PolygonOverlay、GeoJSONOverlay 等通过 `map.addOverlay(overlay)` 添加，通过 `map.removeOverlay(overlay)` 或对应销毁方法清理。
- 控件通过 `map.addControl(control, position?)` 添加，通过 `map.removeControl(control)` 清理。
- 事件订阅必须保存订阅对象或 listener 引用，并在清理阶段取消。
- 地图加载后再添加依赖地图资源的控件、Marker、矢量覆盖物、信息窗口、检索结果、路线结果和动画对象。
- 地图初始化 `center` 必须设置为用户提及的地理区域的合理默认坐标（如"新加坡"→ `[103.8198, 1.3521]`），不得使用 `[0, 0]` 或空值。路线规划、POI 检索等场景，先用区域默认中心初始化地图，数据加载完成后再通过 `fitBounds` 适配实际数据视口。
- 绘制 Marker、Popup、CircleOverlay、PolylineOverlay、PolygonOverlay、GeoJSONOverlay、POI 检索结果或路线结果后，必须根据所有可见地理元素计算 bounds，并调用 `map.fitBounds(bounds, { padding, maxZoom? })` 进行视图适配；单点或小范围场景可使用 `map.easeTo/jumpTo` 设置中心和合适 zoom。
- “所有/尽可能多”的 POI 检索必须说明分页和前端上限，不要补造缺失结果。
- 样式切换使用 `map.setStyle(styleID)`；定位按钮使用浏览器 `navigator.geolocation` 加自定义业务按钮，不要编造内置定位控件类。
- 未在 `maptec-js/src/index.ts` 公开导出或源码中确认的能力，统一标记为需确认。

## 语言自适应

- **必须**根据用户输入的语言自动选择响应语言。如果用户使用英文提问，所有输出（意图识别、代码注释、UI 文本、错误信息、日志输出等）必须使用英文；如果用户使用中文提问，则使用中文。
- 代码中的用户可见文本（如 Popup 内容、Marker 标签、按钮文字）必须与用户输入语言一致。
- 不要在英文场景下使用中文注释或中文 UI 文本，反之亦然。

## 输出要求

面对代码实现任务，输出：

- 命中的功能名称。
- 使用的 Maptec 类、方法和关键参数。
- 必要的地理编码、POI 检索、路线规划或轨迹动画流程。
- 可直接落地的代码或补丁。
- 未确认能力或 SDK 限制。

面对方案设计任务，输出：

- 能力归类。
- 数据与服务调用计划。
- Marker、矢量覆盖物、信息窗口、控件、事件和样式计划。
- 生命周期和清理策略。
