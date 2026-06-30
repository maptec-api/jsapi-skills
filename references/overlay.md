# 矢量覆盖物能力参考

当用户要求绘制点、线、圆、多边形、范围、区域、业务面、GeoJSON 数据层，或要求矢量覆盖物样式配置、数据绑定、事件绑定时，使用本参考。

## 能力范围

- 圆点/圆形范围：`Maptec.CircleOverlay`
- 折线/路径：`Maptec.PolylineOverlay`
- 多边形/区域：`Maptec.PolygonOverlay`
- 数据驱动点线面：`Maptec.GeoJSONOverlay`
- 统一添加与移除：`map.addOverlay(overlay)`、`map.removeOverlay(overlay)`
- 样式配置、显隐控制、事件绑定、数据更新、渲染查询

## CircleOverlay

`CircleOverlay` 一个实例可管理一组圆，圆心通过 `centers` 传入。`unit: "pixels"` 适合点位圆点，`unit: "meters"` 适合地理范围。

```js
const circle = new Maptec.CircleOverlay({
  centers: [[103.8198, 1.3521]],
  radius: 2000,
  unit: "meters",
  fillColor: "#2563eb",
  fillOpacity: 0.18,
  strokeColor: "#2563eb",
  strokeWidth: 2,
  strokeOpacity: 0.9
});

map.addOverlay(circle);
```

常用属性：

- `centers`: 圆心数组，格式为 `LngLatLike[]`。
- `radius`
- `unit`: `"meters"` 或 `"pixels"`。
- `fillColor`、`fillOpacity`
- `strokeColor`、`strokeOpacity`、`strokeWidth`、`strokeDasharray`
- `type`: `CircleOverlayType`，用于波纹、雷达扫描等圆效果。
- `visible`

数据更新：

```js
circle.centers = [
  [103.8198, 1.3521],
  [103.834, 1.31]
];
circle.radius = 120;
```

## PolylineOverlay

```js
const polyline = new Maptec.PolylineOverlay({
  positions: [
    [103.8318, 1.3048],
    [103.8198, 1.3521],
    [103.7764, 1.2966]
  ],
  strokeColor: "#108ee9",
  strokeWeight: 6,
  strokeOpacity: 0.9,
  showDirection: true
});

map.addOverlay(polyline);
```

常用属性：

- `positions`: 折线顶点序列。
- `strokeColor`、`strokeWeight`、`strokeOpacity`
- `strokeDasharray`
- `strokeCap`: `"butt"`、`"round"`、`"square"`。
- `strokeJoin`: `"miter"`、`"round"`、`"bevel"`。
- `strokeGradient`: 按路径进度配置线性渐变。
- `showDirection`、`directionColor`
- `properties`

## PolygonOverlay

```js
const polygon = new Maptec.PolygonOverlay({
  positions: [
    [103.78, 1.29],
    [103.84, 1.29],
    [103.84, 1.34],
    [103.78, 1.34]
  ],
  fillColor: "#22c55e",
  fillOpacity: 0.3,
  strokeColor: "#15803d",
  strokeWeight: 3,
  strokeOpacity: 0.85
});

map.addOverlay(polygon);
```

带洞多边形使用 `[outerRing, hole1, hole2]`：

```js
const polygonWithHole = new Maptec.PolygonOverlay({
  positions: [outerRing, hole],
  fillColor: "#22c55e",
  fillOpacity: 0.28,
  strokeColor: "#15803d"
});
```

## GeoJSONOverlay

大量点、线、面或需要数据驱动样式时，优先使用 `Maptec.GeoJSONOverlay`。

```js
const overlay = new Maptec.GeoJSONOverlay({
  data: featureCollection,
  circleStyle: {
    circleRadius: 8,
    circleColor: "#00bcd4",
    circleStrokeWidth: 2,
    circleStrokeColor: "#004d40"
  },
  lineStyle: {
    strokeColor: "#108ee9",
    strokeWeight: 4
  },
  polygonStyle: {
    fillColor: "#22c55e",
    fillOpacity: 0.3,
    strokeColor: "#15803d",
    strokeWeight: 2
  }
});

map.addOverlay(overlay);
```

`GeoJSONOverlayOptions` 常用字段：

- `data`: GeoJSON `Feature`、`FeatureCollection` 或 `Geometry`。
- `circleStyle`: Point/MultiPoint 圆点样式。
- `symbolStyle`: Point/MultiPoint 图标或文字样式。
- `lineStyle`: LineString/MultiLineString 线样式。
- `polygonStyle`: Polygon/MultiPolygon 面样式。
- `pointCluster`: 点聚合配置。
- `hoverStyle`: 悬停样式。

GeoJSON 坐标也必须使用 `[lng, lat]`。要按单个要素覆盖样式时，可在 feature `properties` 中写入对应样式字段，例如 `circleRadius`、`circleColor`、`symbolText`、`textColor`。

## GeoJSON 样式

圆点样式：

- `circleRadius`
- `circleColor`
- `circleOpacity`
- `circleStrokeColor`
- `circleStrokeWidth`

线样式：

- `strokeColor`
- `strokeWeight`
- `strokeOpacity`
- `strokeDasharray`
- `strokeCap`
- `strokeJoin`
- `strokeGradient`

面样式：

- `fillColor`
- `fillOpacity`
- `strokeColor`
- `strokeWeight`
- `strokeOpacity`
- `strokeDasharray`

符号样式：

- `iconSize`
- `iconOpacity`
- `iconAllowOverlap`
- `textSize`
- `textColor`
- `textAnchor`
- `textOffset`
- `textHaloColor`
- `textHaloWidth`

点聚合：

```js
const clustered = new Maptec.GeoJSONOverlay({
  data: pointFeatureCollection,
  pointCluster: {
    enabled: true,
    clusterRadiusPixels: 60,
    clusterMinPoints: 3,
    showClusterPointCount: true,
    clusterFillColor: "#2563eb",
    clusterStrokeColor: "#ffffff",
    clusterStrokeWidth: 2
  }
});
```

渲染查询：

```js
const features = map.queryRenderedFeatures(point, {
  overlays: [overlay],
  validate: true
});
```

## 事件绑定

```js
const onCircleClick = (event) => {
  console.log("点击圆形", event.features);
};

circle.on("click", onCircleClick);

function cleanup() {
  circle.off("click", onCircleClick);
  map.removeOverlay(circle);
}
```

## 数据更新

```js
circle.centers = [[103.8298, 1.3521]];
circle.radius = 1500;
circle.visible = true;

polyline.positions = [
  [103.8318, 1.3048],
  [103.7764, 1.2966]
];

polygon.positions = [
  [103.78, 1.29],
  [103.84, 1.29],
  [103.84, 1.34],
  [103.78, 1.34]
];

overlay.data = nextFeatureCollection;
```

## 视图适配

绘制圆、线、面或 GeoJSON 覆盖物后，应根据覆盖物坐标自动适配地图视图，确保用户能看到完整几何。

```js
const bounds = path.reduce((nextBounds, point) => [
  [
    Math.min(nextBounds[0][0], point[0]),
    Math.min(nextBounds[0][1], point[1])
  ],
  [
    Math.max(nextBounds[1][0], point[0]),
    Math.max(nextBounds[1][1], point[1])
  ]
], [path[0], path[0]]);

map.fitBounds(bounds, { padding: 80, maxZoom: 16 });
```

圆形范围需要把半径换算成经纬度包围盒后适配，避免只把圆心居中而圆边缘不可见：

```js
const metersPerDegreeLat = 111320;
const latDelta = radius / metersPerDegreeLat;
const lngDelta = radius / (metersPerDegreeLat * Math.cos(center[1] * Math.PI / 180));
map.fitBounds([
  [center[0] - lngDelta, center[1] - latDelta],
  [center[0] + lngDelta, center[1] + latDelta]
], { padding: 80, maxZoom: 16 });
```

## 选型规则

- 半径、服务范围、搜索范围：`CircleOverlay`
- 路径、轨迹、连接线：`PolylineOverlay`
- 区域、围栏、行政边界：`PolygonOverlay`
- 大量点线面、聚合、按属性设置样式：`GeoJSONOverlay`

## 注意事项

- 坐标始终使用 `[lng, lat]`。
- 真实驾车路线不要用手写 `PolylineOverlay` 冒充，必须使用路线规划能力。
- 大量数据优先使用 `GeoJSONOverlay`。
- 大量点位需要聚合时，优先使用 `GeoJSONOverlay` 的 `pointCluster`。
- `strokeDasharray: []` 表示实线；省略时使用 SDK 默认样式。
- 覆盖物事件要保存 handler，并在清理阶段解绑。

## Agent 规则

- 圆、线、面和 GeoJSON 覆盖物必须使用已确认类：`CircleOverlay`、`PolylineOverlay`、`PolygonOverlay`、`GeoJSONOverlay`。
- 不要生成 `new Maptec.Circle()`、`new Maptec.Polyline()`、`new Maptec.Polygon()`。
- 所有地理坐标必须使用 `[lng, lat]`，GeoJSON 坐标也遵循经纬度顺序。
- 真实路线需求必须转到路线规划能力，不要用手写 `PolylineOverlay` 冒充。
- 添加覆盖物后必须说明清理方式：`map.removeOverlay(overlay)`，事件 handler 也要解绑。
- 添加覆盖物、检索结果或路线结果后必须进行视图适配：优先使用 `map.fitBounds(bounds, { padding, maxZoom })`；只有单点且没有范围时才使用 `map.easeTo` 或 `map.jumpTo`。
