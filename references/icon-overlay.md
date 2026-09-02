# IconOverlay 批量图标与文字参考

当用户要求展示大量图标、图标文字注记、图标碰撞避让或点聚合时，使用本参考。

## 能力入口

| 用户需求 | 优先实现 |
|---|---|
| “批量显示站点图标和名称” | `Maptec.IconOverlay` |
| “密集图标不要互相遮挡” | `IconOverlay` 的符号碰撞机制 |
| “低缩放级别聚合图标并显示数量” | `cluster.enabled: true` |
| “点击聚合点后放大到展开层级” | `getClusterExpansionZoom(feature)` + `map.easeTo` |

少量需要自定义 DOM、拖拽或独立 Popup 的点位优先使用 `Marker`；大量纯图标/文字点位优先使用 `IconOverlay`；包含点线面混合数据时优先使用 `GeoJSONOverlay`。

## 基础用法

`iconImage` 是必填项，可使用图片 URL、已经注册的图片 ID、`ImageData` 或浏览器图片对象。每个数据项必须包含 `position`。

```js
const stations = new Maptec.IconOverlay({
  id: "stations",
  iconImage: "https://example.com/station.svg",
  data: [
    {
      position: [103.8519, 1.2903],
      text: "站点 A",
      iconSize: 0.8,
      properties: { stationId: "A" }
    },
    {
      position: [103.8601, 1.3002],
      text: "站点 B",
      iconSize: 0.8,
      heading: 30,
      properties: { stationId: "B" }
    }
  ],
  rotationAlignment: "viewport",
  pitchAlignment: "viewport",
  visible: true
});

map.addOverlay(stations);
```

## 数据项与样式

`IconOverlayItem` 常用字段：

- `position: LngLatLike`
- `iconImage?`、`iconSize?`、`iconOpacity?`
- `heading?`、`anchor?`、`offset?`
- `text?`、`textSize?`、`textColor?`、`textOpacity?`
- `textHaloColor?`、`textHaloWidth?`、`textHaloBlur?`
- `textOffset?`、`textAnchor?`、`textJustify?`
- `properties?`：随渲染要素返回的业务属性

单项的 `iconImage` 和文字样式可以覆盖 Overlay 级默认值。所有地理坐标仍使用 `[lng, lat]`。

## 点聚合

```js
const clustered = new Maptec.IconOverlay({
  id: "clustered-stations",
  iconImage: "https://example.com/station.svg",
  data: stationData,
  cluster: {
    enabled: true,
    radiusPixels: 50,
    maxZoom: 14,
    minPoints: 2,
    fillColor: "#2563eb",
    strokeColor: "#ffffff",
    strokeWidth: 2,
    showCount: true,
    countSize: 12,
    countColor: "#ffffff"
  }
});

map.addOverlay(clustered);
```

`cluster.iconImage` 存在时优先用图片表示聚合簇；否则使用圆和数量文字。

## 聚合点点击展开

```js
const onClusterClick = async (event) => {
  const feature = event.features?.[0];
  if (!feature?.properties?.point_count) return;

  const zoom = await clustered.getClusterExpansionZoom(feature);
  const [lng, lat] = feature.geometry.coordinates;
  map.easeTo({ center: [lng, lat], zoom });
};

clustered.on("click", onClusterClick);
```

## 更新与清理

```js
clustered.data = nextStationData;
clustered.visible = false;
clustered.setClusterOptions({ radiusPixels: 60, maxZoom: 15 });
clustered.setOptions({ visible: true });

function cleanup() {
  clustered.off("click", onClusterClick);
  map.removeOverlay(clustered);
}
```

更新 `data` 时应整体替换数组。数据为空、图片加载失败或聚合展开失败时应提供错误处理和空状态。

## Agent 规则

- 批量图标和文字优先使用 `Maptec.IconOverlay`，不要无上限创建 DOM Marker。
- `iconImage` 和非空 `data` 是创建 `IconOverlay` 的必要输入。
- 只有点击结果含 `properties.point_count` 时才调用 `getClusterExpansionZoom`。
- 保存事件 listener，并在移除 Overlay 前调用 `off`。
- 添加后根据全部点位计算 bounds 并调用 `fitBounds`；不要默认只显示第一条数据。
