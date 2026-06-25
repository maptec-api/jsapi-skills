# 地图交互能力参考

当用户要求控制地图拖拽、缩放、旋转、倾斜、手势控制、交互开关或视角约束时，使用本参考。本文件只覆盖功能 **地图交互**。

## 能力入口

| 用户需求 | 优先实现 |
|---|---|
| “禁止用户旋转或拖拽地图” | 设置 `dragRotate: false`、`dragPan: false` |
| “禁止滚轮缩放” | 设置 `scrollZoom: false` |
| “限制地图缩放范围” | 设置 `minZoom`、`maxZoom` |
| “限制地图倾斜” | 设置 `minPitch`、`maxPitch` |
| “限制地图拖动范围” | 设置 `maxBounds` |
| “运行时开关交互” | 更新 `map.interactive` |

## 初始化时配置交互

```js
const map = new Maptec.Map({
  container: "map",
  style: "YOUR_STYLE_URL",
  center: [103.8198, 1.3521],
  zoom: 12,
  dragPan: false,
  dragRotate: false,
  scrollZoom: true,
  doubleClickZoom: true,
  keyboard: true,
  boxZoom: true
});
```

已确认的常用交互字段：

- `boxZoom`
- `doubleClickZoom`
- `dragPan`
- `dragRotate`
- `keyboard`
- `scrollZoom`
- `cooperativeGestures`

`cooperativeGestures` 通常用于协作手势：桌面端缩放需要 Cmd/Ctrl，移动端需要双指操作。具体表现以 SDK 运行时为准。

## 运行时开关交互

使用 `map.interactive` 更新运行时交互配置。

```js
map.interactive = {
  ...map.interactive,
  dragPan: false,
  dragRotate: false,
  scrollZoom: true,
  doubleClickZoom: true,
  keyboard: true,
  boxZoom: true
};
```

## 视角约束

```js
map.minZoom = 8;
map.maxZoom = 18;
map.minPitch = 0;
map.maxPitch = 60;

map.maxBounds = [
  [103.6, 1.18],
  [104.05, 1.48]
];
```

清除平移范围：

```js
map.maxBounds = null;
```

## 视角控制

地图交互需求经常伴随主动移动视角，可使用相机方法：

- `jumpTo(options)`：立即切换视角。
- `easeTo(options)`：平滑过渡。
- `flyTo(options)`：飞行动画。
- `panTo(lngLatLike)`、`panBy(pointLike)`。
- `zoomIn()`、`zoomOut()`、`zoomTo(zoom)`。
- `rotateTo(bearing)`。
- `fitBounds(boundsLike, options?)`。

常见相机参数：

- `center?: LngLatLike`
- `zoom?: number`
- `bearing?: number`
- `pitch?: number`
- `padding?: number | { top; right; bottom; left }`
- `duration?: number`
- `maxZoom?: number`，常用于 `fitBounds`

```js
map.flyTo({
  center: [103.7764, 1.2966],
  zoom: 15,
  bearing: 0,
  pitch: 0,
  duration: 1000
});
```

## 交互事件

如果需求是监听用户交互，而不是开关交互能力，应读取 `events.md`。

常见事件：

- `dragstart`、`drag`、`dragend`
- `zoomstart`、`zoom`、`zoomend`
- `rotatestart`、`rotate`、`rotateend`
- `pitchstart`、`pitch`、`pitchend`
- `movestart`、`move`、`moveend`

## 注意事项

- 不要使用未在当前 Maptec 文档确认的交互字段。
- 禁止旋转通常需要关闭 `dragRotate`；如果触控旋转有单独字段，必须以 SDK 文档为准，不能编造。
- `maxBounds` 使用 `[southWest, northEast]`，每个点仍是 `[lng, lat]`。
- `PointLike` 是像素坐标，不是地理坐标；只用于偏移、`panBy` 等屏幕空间操作。
- 运行时更新交互时保留不需要改变的旧配置。

## Agent 规则

- 交互开关只能使用已确认字段，例如 `dragPan`、`dragRotate`、`scrollZoom`、`doubleClickZoom`、`keyboard`、`boxZoom`。
- 用户要求禁止旋转或拖拽时，优先更新对应交互字段，不要用覆盖透明层阻止操作。
- 运行时修改交互配置时，应保留 `map.interactive` 中未修改的原有字段。
- 涉及触控手势或协作手势时，如 SDK 能力不明确，必须标记为 `需确认 Maptec 是否支持`。
