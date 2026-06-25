# Maptec Events Reference

Use this reference when handling map events, mouse/wheel events, subscriptions, custom events, overlay events, or cleanup.

## 中文能力入口

本文件对应功能 **事件监听**：支持地图点击、缩放变化、中心点变化、Marker 点击、矢量覆盖物点击、信息窗口打开/关闭等事件监听代码。

| 用户需求 | 事件 |
|---|---|
| “点击地图获取当前位置的经纬度” | `map.on("click", handler)`，读取 `event.lngLat` |
| “监听地图缩放级别变化” | `map.on("zoomend", handler)`，读取 `map.zoom` |
| “监听中心点变化” | `map.on("moveend", handler)`，读取 `map.center` |
| “监听Marker点击” | `marker.on("click", handler)` |
| “监听矢量覆盖物点击” | `circleOverlay.on("click", handler)`、`polylineOverlay.on("click", handler)`、`polygonOverlay.on("click", handler)`、`geojsonOverlay.on("click", handler)` |
| “监听信息窗口打开/关闭” | `popup.on("open", handler)`、`popup.on("close", handler)` |

## Evented Pattern

Maptec map, overlays, and some controls support:

- `on(type, listener)`: subscribe.
- `once(type, listener?)`: subscribe once, or return a promise when no listener is provided.
- `off(type, listener)`: remove listener.

Some `on` calls return a `Subscription` with `unsubscribe()`.

```js
const subscription = map.on("click", (event) => {
  console.log("clicked", event.lngLat);
});

subscription.unsubscribe();
```

If the runtime does not return a subscription, keep the listener reference and call `off`.

```js
const onMoveEnd = () => {
  console.log(map.center, map.zoom);
};

map.on("moveend", onMoveEnd);
map.off("moveend", onMoveEnd);
```

## Map Event Types

Common `MapEventType` entries:

- Lifecycle: `load`, `destroy`, `resize`
- Mouse: `click`, `dblclick`, `contextmenu`, `mousedown`, `mouseup`, `mousemove`, `mouseover`, `mouseout`, `mouseenter`, `mouseleave`
- Wheel: `wheel`
- Touch: `touchstart`, `touchmove`, `touchend`, `touchcancel`
- Move: `movestart`, `move`, `moveend`
- Drag: `dragstart`, `drag`, `dragend`
- Zoom: `zoomstart`, `zoom`, `zoomend`
- Rotate: `rotatestart`, `rotate`, `rotateend`
- Pitch: `pitchstart`, `pitch`, `pitchend`
- Box zoom: `boxzoomstart`, `boxzoomend`, `boxzoomcancel`

```js
map.on("load", () => {
  console.log("map loaded");
});

map.on("moveend", () => {
  console.log("view", map.center, map.zoom);
});
```

## MapMouseEvent

Mouse events such as `click` provide a `MapMouseEvent`.

Important fields:

- `type`
- `target`: map instance
- `originalEvent`: original DOM mouse event
- `point`: screen pixel point
- `lngLat`: geographic coordinate
- `defaultPrevented`

Method:

- `preventDefault()`

```js
map.on("click", (event) => {
  console.log("screen point", event.point);
  console.log("lngLat", event.lngLat);
});
```

Click map and get `[lng, lat]`:

```js
const onMapClick = (event) => {
  const lngLat = Maptec.LngLat.convert(event.lngLat).toArray();
  console.log("点击坐标", lngLat);
};

map.on("click", onMapClick);

// cleanup
map.off("click", onMapClick);
```

Use `event.lngLat` for map coordinates and `event.point` for UI pixel calculations.

## MapWheelEvent

`wheel` events provide `MapWheelEvent`.

Fields:

- `type`: `"wheel"`
- `target`: map instance
- `originalEvent`: original `WheelEvent`
- `defaultPrevented`

Method:

- `preventDefault()`: prevents the map's default zoom behavior for that wheel event.

```js
map.on("wheel", (event) => {
  if (shouldBlockWheelZoom(event.originalEvent)) {
    event.preventDefault();
  }
});
```

## MaptecEvent

`Maptec.Event` can be created and fired.

```js
const event = new Maptec.Event("custom:ready", {
  message: "地图初始化完成"
});

map.fire(event);
```

Use custom events sparingly. Prefer normal application state events unless the event should be part of the Maptec map event pipeline.

## Overlay Events

Overlays such as `Marker`, `Popup`, `CircleOverlay`, `PolylineOverlay`, `PolygonOverlay`, and `GeoJSONOverlay` expose event methods where supported.

```js
const marker = new Maptec.Marker({
  position: [103.8198, 1.3521]
});

marker.on("click", () => {
  marker.togglePopup();
});

map.addOverlay(marker);
```

```js
const polyline = new Maptec.PolylineOverlay({
  positions: [
    [103.8318, 1.3048],
    [103.8198, 1.3521]
  ],
  strokeColor: "#7c3aed",
  strokeWeight: 5
});

const onLineClick = (event) => {
  console.log("点击折线", event.features);
};

polyline.on("click", onLineClick);
map.addOverlay(polyline);
```

## Cleanup Pattern

```js
const cleanups = [];

function listen(target, type, listener) {
  const subscription = target.on(type, listener);
  cleanups.push(() => {
    if (subscription?.unsubscribe) {
      subscription.unsubscribe();
      return;
    }
    target.off?.(type, listener);
  });
}

listen(map, "moveend", () => {
  console.log(map.center);
});

function cleanup() {
  cleanups.splice(0).forEach((fn) => fn());
}
```

## Pitfalls

- Do not attach listeners repeatedly inside render loops without cleanup.
- Use `once` for one-time initialization reactions.
- Use `preventDefault()` only when intentionally overriding SDK behavior.
- Use `lngLat` for geographic work and `point` for pixel/UI work.
- 覆盖物事件示例必须使用真实公开类名，不要写 `Circle`、`Polyline`、`Polygon`。

## Agent 规则

- 监听事件时必须保存 listener 引用或订阅对象，清理阶段使用 `off` 或 `unsubscribe()`。
- 地图点击获取经纬度时使用 `event.lngLat`，需要数组时再转换为 `[lng, lat]`。
- 缩放、中心点、旋转、倾斜等状态应从地图实例读取，不要自行缓存后当作真实状态。
- 覆盖物事件使用 `Marker`、`Popup`、`CircleOverlay`、`PolylineOverlay`、`PolygonOverlay`、`GeoJSONOverlay` 的事件能力。
- 不要编造未确认事件名；未确认事件必须标记为 `需确认 Maptec 是否支持`。
