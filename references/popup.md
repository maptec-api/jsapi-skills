# 信息窗口能力参考

当用户要求打开信息窗口、点击地图显示经纬度、Marker 绑定气泡、展示 POI 信息或自定义弹窗内容时，使用本参考。

## 能力范围

- 创建 `Maptec.Popup`。
- 设置位置、HTML、纯文本、偏移、宽度、关闭行为。
- 作为独立信息窗口添加到地图。
- 绑定到 `Maptec.Marker`。
- 监听打开、关闭事件。

## 点击地图增加信息窗口展示经纬度

```js
let popup = null;

const onMapClick = (event) => {
  const position = Maptec.LngLat.convert(event.lngLat).toArray();
  const text = `经度：${position[0].toFixed(6)}，纬度：${position[1].toFixed(6)}`;

  if (!popup) {
    popup = new Maptec.Popup({
      position,
      text,
      closeButton: true,
      closeOnClick: false
    });
    map.addOverlay(popup);
  } else {
    popup.position = position;
    popup.text = text;
  }
};

map.on("click", onMapClick);

function cleanup() {
  map.off("click", onMapClick);
  if (popup) {
    map.removeOverlay(popup);
    popup.destroy?.();
  }
}
```

## 基础信息窗口

```js
const popup = new Maptec.Popup({
  position: [103.8198, 1.3521],
  html: "<strong>Singapore</strong>",
  offset: [0, -15],
  maxWidth: "300px",
  closeButton: true,
  closeOnClick: true
});

map.addOverlay(popup);
```

## Marker 绑定信息窗口

```js
const popup = new Maptec.Popup({
  offset: 25,
  html: "<strong>National University of Singapore</strong>"
});

const marker = new Maptec.Marker({
  position: [103.7764, 1.2966],
  color: "#2563eb",
  popup
});

map.addOverlay(marker);
```

## 常用配置

- `position`: 信息窗口坐标
- `anchor`: 信息窗口锚点，未指定时 SDK 通常会动态调整。
- `html`: HTML 内容
- `text`: 纯文本内容
- `offset`: 像素偏移
- `maxWidth`: 最大宽度
- `className`: 自定义样式类
- `closeButton`: 是否显示关闭按钮
- `closeOnClick`: 点击地图时是否关闭
- `closeOnMove`: 地图移动时是否关闭
- `padding`: 用于让 Popup 避开地图边缘。

常用方法：

- `setDOMContent(element)`
- `getElement()`
- `isOpen()`
- `addClassName(className)`
- `removeClassName(className)`
- `destroy()`
- `isDestroyed()`

## DOM 内容

用户内容来自输入、服务结果或外部数据时，优先使用 `text` 或对 HTML 做清洗。

```js
const content = document.createElement("div");
content.textContent = "自定义 DOM 内容";

const popup = new Maptec.Popup({
  position: [103.8198, 1.3521]
});

popup.setDOMContent(content);
map.addOverlay(popup);
```

## 事件

```js
const onOpen = () => console.log("信息窗口打开");
const onClose = () => console.log("信息窗口关闭");

popup.on("open", onOpen);
popup.on("close", onClose);

function cleanupPopupEvents() {
  popup.off("open", onOpen);
  popup.off("close", onClose);
}
```

## 注意事项

- 独立信息窗口必须有 `position`。
- Marker 绑定信息窗口时，优先设置 `offset`，避免遮挡 Marker。
- 不要把用户输入直接拼接进 `html`。
- 清理时移除 Popup，并取消事件监听。

## Agent 规则

- 信息窗口必须使用 `new Maptec.Popup(...)`，并通过 `map.addOverlay(popup)` 或 Marker 绑定方式使用。
- 展示用户输入、POI 服务结果或外部数据时，优先使用 `text` 或安全 DOM，不要直接拼接到 `html`。
- 独立 Popup 必须提供 `position`；Marker 绑定 Popup 时应设置合理 `offset`。
- Popup 打开、关闭事件必须保存 handler，并在清理阶段解绑。
