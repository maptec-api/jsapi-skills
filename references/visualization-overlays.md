# 高级可视化覆盖物参考

当用户要求批量图标以外的高级二维/三维数据可视化时，使用本参考。本文件覆盖 `PrismOverlay`、`HeatmapOverlay`、`Heatmap3DOverlay`、`HexagonOverlay` 和 `MaskOverlay`。

## 选型

| 需求 | 类 |
|---|---|
| 带固定高度的区域、建筑体块、三维行政区 | `Maptec.PrismOverlay` |
| 点密度的二维热度分布 | `Maptec.HeatmapOverlay` |
| 有高度曲面的三维热度分布 | `Maptec.Heatmap3DOverlay` |
| 按蜂窝归格统计并用柱高/颜色表达数值 | `Maptec.HexagonOverlay` |
| 弱化区域外地图、突出指定区域 | `Maptec.MaskOverlay` |

这些类都通过 `map.addOverlay` 添加、通过 `map.removeOverlay` 清理。依赖异步数据或图片资源时，先完成加载和校验，再创建 Overlay。

## PrismOverlay 三维棱柱

`positions` 支持单个 polygon 外环、带洞 polygon 或多个 polygon；`altitude` 单位为米。

```js
const prism = new Maptec.PrismOverlay({
  id: "business-zone-3d",
  positions: polygonCoordinates,
  altitude: 1200,
  topColor: "#60a5fa",
  topOpacity: 0.9,
  sideColor: "#2563eb",
  sideOpacity: 0.75,
  properties: { zoneId: "A" }
});

map.addOverlay(prism);
```

纹理模式需要先注册图片：

```js
const topImage = await map.loadImage("/images/prism-top.png");
const sideImage = await map.loadImage("/images/prism-side.png");

if (!map.hasImage("prism-top")) map.addImage("prism-top", topImage);
if (!map.hasImage("prism-side")) map.addImage("prism-side", sideImage);

const texturedPrism = new Maptec.PrismOverlay({
  positions: polygonCoordinates,
  altitude: 3000,
  topPattern: "prism-top",
  sidePattern: "prism-side"
});
```

可运行时更新 `positions`、`altitude`、顶/侧面颜色、透明度、纹理和 `visible`，也可用 `setOptions(partial)`。`PrismOverlay` 支持 `on/off/once` 指针事件；使用时保存 listener 并在清理前解绑。

## HeatmapOverlay 二维热力图

```js
const heatmap = new Maptec.HeatmapOverlay({
  id: "poi-heat",
  points: poiData.map((item) => ({
    position: item.position,
    weight: item.score,
    properties: { id: item.id }
  })),
  radius: 30,
  minWeight: 0,
  maxWeight: 100,
  intensity: 1,
  opacity: 0.85,
  gradient: {
    0: "rgba(42,133,184,0)",
    0.5: "#7DF675",
    1: "#D04343"
  },
  minZoom: 7,
  maxZoom: 18,
  visible: true
});

map.addOverlay(heatmap);
```

`weight` 默认为 1。未指定 `maxWeight` 时，SDK 使用数据中的最大 weight；业务需要跨批次可比时应显式固定 `minWeight/maxWeight`。`HeatmapOverlay` 支持 `on/off/once` 指针事件；三维热力图未确认同等拾取语义，不要自行声明。

## Heatmap3DOverlay 三维热力图

```js
const heatmap3D = new Maptec.Heatmap3DOverlay({
  id: "poi-heat-3d",
  points: poiData.map((item) => ({
    position: item.position,
    weight: item.score
  })),
  unit: "meter",
  radius: 500,
  height: 2000,
  minWeight: 0,
  maxWeight: 100,
  intensity: 0.7,
  opacity: 0.7,
  depthTest: true,
  minZoom: 2,
  maxZoom: 22,
  gradient: {
    0.1: "#2A85B8",
    0.5: "#7DF675",
    1: "#D04343"
  },
  heightAnimate: {
    duration: 1600,
    delay: 0
  }
});

map.addOverlay(heatmap3D);
```

- `unit: "meter"`：半径和高度按地理米解释。
- `unit: "px"`：半径和高度按屏幕像素解释。
- `depthTest: true`：曲面参与三维遮挡。
- `heightAnimate`：挂载后从 0 高度增长；不传时直接显示完整高度。

可更新 `points`、`radius`、`unit`、`height`、权重范围、渐变、透明度、层级范围和显隐，也可用 `setOptions`。

## HexagonOverlay 三维蜂窝聚合

`HexagonOverlay` 负责按半径归格，但业务统计值由调用方根据每个 cell 的 `points` 计算。

```js
const sumValues = (points) =>
  points.reduce((sum, point) => sum + Number(point.value ?? 0), 0);

const hexagons = new Maptec.HexagonOverlay({
  id: "demand-hexagons",
  points: sourceData.map((item) => ({
    position: item.position,
    value: item.value,
    properties: { id: item.id }
  })),
  radius: 120,
  gap: 0,
  height: (cell) => Math.max(20, sumValues(cell.points) * 10),
  topColor: (cell) => sumValues(cell.points) > 100 ? "#ef4444" : "#3b82f6",
  sideColor: (cell) => sumValues(cell.points) > 100 ? "#b91c1c" : "#1d4ed8",
  topOpacity: 1,
  sideOpacity: 0.9,
  heightGrowth: {
    duration: 500,
    easing: "easeOut",
    random: true,
    delay: 300,
    startDelay: 200
  }
});

map.addOverlay(hexagons);
```

- `radius`、`gap` 和 `height` 的距离单位是米。
- `height`、`topColor`、`sideColor` 可为常量或按 cell 计算的函数。
- `heightGrowth` 可配置 `duration`、`easing`、随机错峰 `delay`、`startDelay` 和 `onComplete`。
- 可调用 `playHeightGrowth(options)` 重播，调用 `stopHeightGrowth()` 停止。

不要声称 SDK 会自动求和、平均或分级；这些统计必须在回调里明确实现。`HexagonOverlay` 支持 `on/off/once` 指针事件；Mask 和三维热力图的指针事件未确认时应标记为需确认。

## MaskOverlay 区域遮罩

```js
const mask = new Maptec.MaskOverlay({
  id: "singapore-focus",
  positions: polygonOrMultiPolygonCoordinates,
  maskColor: "#0b1d3a",
  maskOpacity: 0.55,
  strokeColor: "#00eeff",
  strokeWeight: 2,
  strokeOpacity: 0.95,
  strokeDasharray: [],
  showStroke: true,
  maxRingPoints: 500,
  simplifyTolerance: 0.00005,
  visible: true
});

map.addOverlay(mask);
```

`positions` 可为简单 polygon、带洞 polygon 或多个区域。遮罩覆盖高亮区域之外的地图，高亮区域本身保持可见。

可更新 `positions`、遮罩颜色/透明度、边界样式、`showStroke` 和 `visible`，也可用 `setOptions(partial)`。

## 数据更新、视图与清理

```js
heatmap.points = nextHeatPoints;
heatmap3D.setOptions({ height: 3000, opacity: 0.8 });
hexagons.points = nextHexagonPoints;
prism.altitude = 1800;
mask.visible = false;

function cleanup() {
  hexagons.stopHeightGrowth();
  map.removeOverlay([prism, heatmap, heatmap3D, hexagons, mask]);

  if (map.hasImage("prism-top")) map.removeImage("prism-top");
  if (map.hasImage("prism-side")) map.removeImage("prism-side");
}
```

创建后应基于全部源坐标调用 `fitBounds`。热力图、蜂窝图的数据为空时不要创建空图层，应展示空状态。

## Agent 规则

- 只使用已公开的 `PrismOverlay`、`HeatmapOverlay`、`Heatmap3DOverlay`、`HexagonOverlay`、`MaskOverlay`，不要发明相似类名。
- 二维热力和三维热力必须根据用户是否需要高度表达进行选型。
- 蜂窝统计必须显式实现聚合函数，不能声称 SDK 自动完成业务指标计算。
- Prism 纹理必须先 `loadImage` 和 `addImage`，清理时只移除当前业务拥有的图片资源。
- 异步加载必须检查 HTTP 响应、空数据和几何类型；失败时不要继续创建 Overlay。
- 保存 Overlay 引用，停止动画、解绑事件并调用 `map.removeOverlay` 清理。
