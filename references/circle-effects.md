# CircleOverlay 特效、阴影、发光与聚合参考

当用户要求波纹点、雷达扫描、圆形阴影/发光或海量圆点聚合时，在 `references/overlay.md` 基础上读取本参考。

## 类型与适用限制

`Maptec.CircleOverlayType` 已确认值：

- `Circle`：普通圆，值为 `"circle"`
- `Wave`：波纹圆，值为 `"wave"`
- `RadarScan`：雷达扫描圆，值为 `"radarScan"`

`Wave`、`RadarScan` 和聚合只在 `unit: "pixels"` 时生效。实际地理半径范围继续使用 `unit: "meters"`，不要为了动画效果改变业务距离含义。

## 波纹

```js
const wave = new Maptec.CircleOverlay({
  centers: [[103.8519, 1.2903]],
  radius: 24,
  unit: "pixels",
  type: Maptec.CircleOverlayType.Wave,
  fillColor: "#148df9",
  speed: 1,
  waveCount: 3,
  gradient: 0.8
});

map.addOverlay(wave);
```

## 雷达扫描

```js
const radar = new Maptec.CircleOverlay({
  centers: [[103.8198, 1.3521]],
  radius: 80,
  unit: "pixels",
  type: Maptec.CircleOverlayType.RadarScan,
  fillColor: "#22c55e",
  fillOpacity: 0.45,
  speed: 1.2
});

map.addOverlay(radar);
```

## 内阴影与外发光

```js
const highlighted = new Maptec.CircleOverlay({
  centers: [[103.84, 1.31]],
  radius: 36,
  unit: "pixels",
  fillColor: "#0f172a",
  innerShadow: true,
  innerShadowColor: "#000000",
  innerShadowOpacity: 0.55,
  innerShadowWidth: 10,
  outerGlow: true,
  glowColor: "#22d3ee",
  glowRadius: 28,
  depthTest: false
});

map.addOverlay(highlighted);
```

`depthTest: true` 会让圆被三维建筑等几何正确遮挡；只有业务明确需要三维遮挡关系时启用。

## 聚合

```js
const clusteredCircles = new Maptec.CircleOverlay({
  centers: poiCoordinates,
  radius: 7,
  unit: "pixels",
  fillColor: "#6366f1",
  enableCluster: true,
  clusterRangeRadius: 50,
  clusterMaxZoom: 14,
  clusterFillColor: "#4f46e5",
  clusterRadiusPixels: 22,
  clusterStrokeWidth: 2,
  clusterStrokeColor: "#ffffff",
  showClusterPointCount: true,
  clusterPointCountTextSize: 12,
  clusterPointCountTextColor: "#ffffff"
});

map.addOverlay(clusteredCircles);
```

`clusterRangeRadius` 决定哪些点合并成簇，`clusterRadiusPixels` 决定簇圆在屏幕上的显示大小，两者不要混用。

## 更新与清理

```js
wave.centers = nextCenters;
wave.radius = 30;
highlighted.setOptions({ glowRadius: 40, outerGlow: true });

function cleanup() {
  map.removeOverlay([wave, radar, highlighted, clusteredCircles]);
}
```

## Agent 规则

- 波纹、雷达和聚合必须设置 `unit: "pixels"`。
- 地理范围圆必须使用 `unit: "meters"`，不能用像素圆冒充实际距离。
- 不要编造 `Maptec.RadarOverlay` 或 `Maptec.WaveOverlay`；使用 `CircleOverlayType`。
- 大量点聚合前说明数据规模和前端上限；真实 POI 数据仍必须来自 `PlaceSearch`。
- 使用事件时保存 listener，并在清理阶段解绑和移除 Overlay。
