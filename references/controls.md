# Maptec Controls Reference

Use this reference when adding built-in map controls such as navigation, scale, fullscreen, compass, or hawkeye.

## 中文能力入口

本文件对应功能 **地图控件**：支持缩放导航、比例尺、全屏、指南针、鹰眼控件的位置配置、添加、移除与清理。

当前公开控件类：

- `Maptec.NavigationControl`
- `Maptec.ScaleControl`
- `Maptec.FullscreenControl`
- `Maptec.CompassControl`
- `Maptec.HawkeyeControl`

| 用户需求 | 优先实现 |
|---|---|
| “添加缩放控件” | `new Maptec.NavigationControl()` + `map.addControl(nav, position)` |
| “在地图右下角添加比例尺控件” | `new Maptec.ScaleControl()` + `map.addControl(scale, "bottom-right")` |
| “添加全屏按钮” | `new Maptec.FullscreenControl()` |
| “添加指南针控件” | `new Maptec.CompassControl()` 或使用 `NavigationControl` 内置指南针 |
| “添加鹰眼地图” | `new Maptec.HawkeyeControl(options)` |
| “隐藏/显示某个控件” | 保存 control 实例，使用 `map.addControl` / `map.removeControl` 切换 |

## Common Pattern

Controls are created with `new Maptec.XControl(...)` and added with `map.addControl(control, position?)`.

```js
map.on("load", () => {
  const scale = new Maptec.ScaleControl();
  map.addControl(scale, "bottom-left");
});
```

Supported positions:

- `"top-left"`
- `"top-right"`
- `"bottom-left"`
- `"bottom-right"`

Use `map.removeControl(control)` for cleanup when needed.

```js
const controls = [];

function addControl(control, position) {
  map.addControl(control, position);
  controls.push(control);
}

function cleanup() {
  controls.forEach((control) => map.removeControl(control));
}
```

## NavigationControl

Contains zoom buttons and compass.

```js
const nav = new Maptec.NavigationControl();
map.addControl(nav, "top-left");
```

Use this when users need standard zoom and orientation controls.

## ScaleControl

Displays a distance scale.

```js
const scale = new Maptec.ScaleControl({
  maxWidth: 100,
  unit: "metric"
});

map.addControl(scale, "bottom-left");
```

Supported units:

- `"metric"`
- `"imperial"`
- `"nautical"`

## FullscreenControl

Adds a fullscreen toggle button.

```js
const fullscreen = new Maptec.FullscreenControl();
map.addControl(fullscreen, "top-right");
```

It follows the evented pattern where supported:

- `on(type, listener)`
- `once(type, listener?)`
- `off(type, listener)`

## CompassControl

Shows a compass with rotation controls.

- Left/right arrows rotate the map.
- Center compass resets north when not facing north.
- When already north, center toggles 2D/3D pitch.

```js
const compass = new Maptec.CompassControl();
map.addControl(compass, "top-right");
```

## HawkeyeControl

Shows an overview map and viewport box.

```js
const hawkeye = new Maptec.HawkeyeControl({
  zoomDiff: 4,
  overviewBoxColor: "blue",
  width: "150px",
  height: "100px"
});

map.addControl(hawkeye, "bottom-right");
```

Options:

- `zoomDiff`: zoom difference between main map and overview map; default `4`.
- `overviewBoxColor`: CSS color for viewport box.
- `width`: overview width; default `"150px"`.
- `height`: overview height; default `"100px"`.

## Business Locate Button

`maptec-js/src/index.ts` 未公开导出 `GeolocateControl`。如果产品需要定位按钮，用浏览器定位能力实现业务按钮，再移动地图并添加或更新 Marker。

```js
const locateButton = document.createElement("button");
locateButton.type = "button";
locateButton.textContent = "定位";
locateButton.className = "map-locate-button";

let userMarker = null;

locateButton.addEventListener("click", () => {
  if (!navigator.geolocation) {
    console.warn("当前浏览器不支持定位");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lngLat = [
        position.coords.longitude,
        position.coords.latitude
      ];

      if (!userMarker) {
        userMarker = new Maptec.Marker({
          position: lngLat,
          color: "#2563eb"
        });
        map.addOverlay(userMarker);
      } else {
        userMarker.position = lngLat;
      }

      map.flyTo({ center: lngLat, zoom: 16 });
    },
    (error) => {
      console.error("定位失败", error);
    },
    { enableHighAccuracy: true, timeout: 10000 }
  );
});
```

## Pitfalls

- Do not write `new Maptec.PerformanceMonitorControl()`, `new Maptec.GeolocateControl()`, `new Maptec.LogoControl()`, or `new Maptec.AttributionControl()` in user-facing examples unless those classes are explicitly exported by the current SDK.
- Do not add both `NavigationControl` and separate `CompassControl` unless the UI intentionally needs both.
- Keep control instances so they can be removed during component cleanup.

## Agent 规则

- 添加控件必须使用 `map.addControl(control, position?)`，清理时使用 `map.removeControl(control)`。
- 内置控件只能使用当前公开导出的 `NavigationControl`、`ScaleControl`、`FullscreenControl`、`CompassControl`、`HawkeyeControl`。
- 定位按钮使用浏览器 `navigator.geolocation` 加自定义业务按钮方案，不要编造 `Maptec.GeolocateControl`。
- 控件位置只能使用 SDK 支持的位置值：`top-left`、`top-right`、`bottom-left`、`bottom-right`。
