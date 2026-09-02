# queryRenderedFeatures 渲染要素查询参考

当用户要求点击拾取地图要素、框选要素、查询当前视口内可见要素，或限定图层/覆盖物查询时，使用本参考。

## 查询边界

`map.queryRenderedFeatures` 查询当前已渲染且可见的要素，坐标参数是相对地图画布左上角的像素坐标，不是经纬度。

已确认签名：

```ts
map.queryRenderedFeatures(pointOrBox?, options?)
```

- 单点：`[x, y]` 或地图事件的 `event.point`
- 框选：`[[left, top], [right, bottom]]`
- 省略 geometry：查询当前视口
- options：`overlays`、`layers`、`filter`、`availableImages`、`validate`

如果同时传入 `overlays` 和 `layers`，SDK 忽略 `layers`。

## 点击查询

```js
const onMapClick = (event) => {
  const features = map.queryRenderedFeatures(event.point);
  if (features.length === 0) {
    console.log("当前位置没有可见要素");
    return;
  }
  console.log(features);
};

map.on("click", onMapClick);
```

## 限定覆盖物

```js
const features = map.queryRenderedFeatures(event.point, {
  overlays: [geojsonOverlay, circleOverlay, polylineOverlay, polygonOverlay],
  validate: true
});
```

`overlays` 当前只确认支持 `GeoJSONOverlay`、`CircleOverlay`、`PolylineOverlay`、`PolygonOverlay`。不要把 `IconOverlay`、`PrismOverlay`、热力图、蜂窝或遮罩直接传入 `overlays`，除非后续 SDK 类型已明确扩展。

## 框选查询

```js
const start = [120, 100];
const end = [420, 360];
const confirmedLayerIds = ["CONFIRMED_STYLE_LAYER_ID"];
const features = map.queryRenderedFeatures([start, end], {
  layers: confirmedLayerIds
});
```

拖拽框选时应把起止点归一化为左上角和右下角：

```js
const box = [
  [Math.min(start[0], end[0]), Math.min(start[1], end[1])],
  [Math.max(start[0], end[0]), Math.max(start[1], end[1])]
];
```

## 全视口查询

```js
const confirmedLayerIds = ["CONFIRMED_STYLE_LAYER_ID"];
const visibleFeatures = map.queryRenderedFeatures({
  layers: confirmedLayerIds
});
```

省略 geometry 时，第一个参数可以直接传 options。全视口结果可能很多，应设置图层或过滤条件，并对 UI 展示数量设上限。

## 过滤与结果处理

```js
const confirmedLayerIds = ["CONFIRMED_STYLE_LAYER_ID"];
const features = map.queryRenderedFeatures(event.point, {
  layers: confirmedLayerIds,
  filter: ["==", ["get", "CONFIRMED_PROPERTY_NAME"], "CONFIRMED_VALUE"],
  validate: true
});

const uniqueFeatures = Array.from(
  new Map(features.map((feature) => [
    `${feature.layer?.id ?? ""}:${feature.id ?? JSON.stringify(feature.geometry)}`,
    feature
  ])).values()
);
```

跨 tile 的同一逻辑要素可能重复出现；有稳定 `feature.id` 时优先用它去重。不要假设所有结果都有相同 properties。图层 ID 和过滤字段必须来自当前已加载样式或项目配置，不能照抄示例占位符。

## 清理

```js
function cleanup() {
  map.off("click", onMapClick);
}
```

框选 UI 还应清理鼠标事件、选择框 DOM 和临时 Popup/Overlay。

## Agent 规则

- 像素查询参数不能使用 `[lng, lat]`。
- 点击查询优先使用地图事件的 `event.point`，不要自行把经纬度当像素。
- 同时传入 `overlays` 和 `layers` 时明确说明 `layers` 会被忽略。
- 全视口查询必须考虑结果上限、去重和空结果。
- `layers` 和 `filter` 中的图层 ID、属性名和值必须来自当前样式或业务数据定义。
- `validate: false` 只用于过滤表达式已预先校验的性能场景。
