# Marker 能力参考

当用户要求添加 Marker、点击地图增加点标记、拖拽点标记、设置 Marker 样式或绑定 Marker 事件时，使用本参考。

## 能力范围

- 创建 `Maptec.Marker`。
- 设置 Marker 位置、颜色、缩放、透明度、旋转、拖拽、偏移和锚点。
- 使用自定义 HTMLElement 作为 Marker 外观。
- 绑定 Marker 点击、拖拽等事件。
- 与 `Maptec.Popup` 组合，但信息窗口细节优先读取 `popup.md`。

## 基础 Marker

```js
const marker = new Maptec.Marker({
  position: [103.8198, 1.3521]
});

map.addOverlay(marker);
```

## 点击地图增加 Marker

```js
const markers = [];

const onMapClick = (event) => {
  const position = Maptec.LngLat.convert(event.lngLat).toArray();
  const marker = new Maptec.Marker({
    position,
    color: "#2563eb",
    scale: 1
  });

  map.addOverlay(marker);
  markers.push(marker);
};

map.on("click", onMapClick);

function cleanup() {
  map.off("click", onMapClick);
  markers.forEach((marker) => {
    map.removeOverlay(marker);
    marker.destroy?.();
  });
}
```

## 样式和属性

已确认的常用配置：

- `position`: `LngLatLike`
- `anchor`: `"center"`、`"top"`、`"bottom"`、`"left"`、`"right"`、`"top-left"`、`"top-right"`、`"bottom-left"`、`"bottom-right"`
- `color`: 默认 Marker 颜色
- `scale`: 缩放比例
- `draggable`: 是否可拖拽
- `element`: 自定义 HTMLElement
- `offset`: 像素偏移，接受 `PointLike`
- `opacity`: 透明度
- `rotation`: 旋转角度
- `popup`: 绑定的 `Maptec.Popup`

Marker 支持的辅助方法：

- `addClassName(className)`
- `removeClassName(className)`
- `togglePopup()`
- `destroy()`
- `isDestroyed()`

```js
marker.position = [103.7764, 1.2966];
marker.draggable = true;
marker.opacity = 0.85;
marker.rotation = 45;
marker.offset = [0, -10];
```

## 事件绑定

```js
const onMarkerClick = () => {
  marker.togglePopup?.();
};

const onDragEnd = () => {
  console.log("Marker 新位置", marker.position);
};

marker.on("click", onMarkerClick);
marker.on("dragend", onDragEnd);

function cleanupMarkerEvents() {
  marker.off("click", onMarkerClick);
  marker.off("dragend", onDragEnd);
}
```

## 数据绑定

业务数据建议单独保存，不要只依赖 DOM 属性。

```js
const markerRecords = places.map((place) => {
  const marker = new Maptec.Marker({
    position: [place.longitude, place.latitude],
    color: "#16a34a"
  });

  map.addOverlay(marker);

  return {
    id: place.id,
    data: place,
    marker
  };
});
```

## 注意事项

- Marker 坐标始终使用 `[lng, lat]`。
- 不要用 DOM 绝对定位伪造地图 Marker。
- 大量点位优先考虑 `GeoJSONOverlay`，不要无上限创建 Marker。
- Marker 绑定 Popup 时优先设置 Popup `offset`，避免遮挡 Marker。
- 组件卸载时移除 Marker，并取消事件监听。

## Agent 规则

- Marker 必须通过 `new Maptec.Marker(...)` 创建，并通过 `map.addOverlay(marker)` 添加到地图。
- 点击地图添加 Marker 时，必须从 `event.lngLat` 获取坐标，不要使用屏幕像素点作为地理坐标。
- 大量点位或需要聚合时，优先使用 `GeoJSONOverlay`，不要生成无限 Marker。
- 绑定 Marker 事件时必须提供解绑逻辑，清理时移除 Marker 并取消事件监听。
