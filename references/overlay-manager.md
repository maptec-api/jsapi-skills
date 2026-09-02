# OverlayManager 统一管理参考

当用户要求批量添加/移除覆盖物、统一显隐、按 ID 查询或清空地图业务覆盖物时，使用本参考。

## 能力范围

`map.overlayManager` 管理 `CircleOverlay`、`PolylineOverlay`、`PolygonOverlay`、`PrismOverlay`、`HeatmapOverlay`、`Heatmap3DOverlay`、`HexagonOverlay`、`MaskOverlay`、`IconOverlay`。

`Marker`、`Popup` 可通过 `map.addOverlay/removeOverlay` 使用，但不属于公开 `MapOverlay` 类型联合，不要宣称它们支持全部 `OverlayManager` 查询和统一显隐语义。

## 添加单个或多个覆盖物

```js
const circle = new Maptec.CircleOverlay({
  id: "service-area",
  centers: [[103.8198, 1.3521]],
  radius: 2000,
  unit: "meters"
});

const route = new Maptec.PolylineOverlay({
  id: "route-line",
  positions: routePath,
  strokeColor: "#148df9",
  strokeWeight: 5
});

map.addOverlay([circle, route]);
```

`map.addOverlay` 是推荐业务入口，并支持数组。直接调用 `map.overlayManager.addOverlay` 也支持单个或数组。ID 必须唯一，重复 ID 会报错。

## 统一显隐

```js
map.overlayManager.visible = false;
map.overlayManager.visible = true;
```

统一显隐不会改变各 Overlay 自身的 `visible` 值。管理器重新显示后，单个 Overlay 原本的显隐状态仍应生效。

## 查询

```js
const routeOverlay = map.overlayManager.getOverlayById("route-line");
const allOverlays = map.overlayManager.getOverlays();
const sameList = map.overlayManager.overlays;
```

地图实例也提供 `map.getOverlayById(id)` 和 `map.getOverlays()` 便捷方法。

## 移除与清空

```js
map.removeOverlay([circle, route]);

map.overlayManager.removeOverlayById("route-line");
map.overlayManager.removeAll();
```

`map.removeOverlay` 支持数组；`OverlayManager.removeOverlay` 使用单个 Overlay 实例。清空前如果 Overlay 注册了业务 listener，应先逐个解绑。

```js
function cleanup() {
  for (const overlay of map.overlayManager.getOverlays()) {
    const listener = overlayListeners.get(overlay.id);
    if (listener) overlay.off?.("click", listener);
  }
  map.overlayManager.removeAll();
}
```

## Agent 规则

- 需要统一显隐、按 ID 查询或清空时使用 `map.overlayManager`，不要额外维护一套不一致的全局数组。
- 创建 Overlay 时设置稳定且唯一的 `id`，不要依赖自动 ID 做跨流程查询。
- 批量添加/移除优先使用 `map.addOverlay(array)`、`map.removeOverlay(array)`。
- `removeAll` 会移除托管 Overlay；业务事件 listener、外部 DOM 和计时器仍应由业务代码清理。
- 不要把 Marker/Popup 宣称为 `MapOverlay` 联合中的类型。
