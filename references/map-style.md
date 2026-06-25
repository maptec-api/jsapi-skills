# 样式切换参考

当用户要求白天/黑夜地图、暗色地图、亮色地图、增加按钮切换模式时，使用本参考。

## 能力范围

- 初始化时通过 `style` 加载地图样式。
- 运行时通过 `map.setStyle(styleID)` 切换地图样式。
- 增加自定义按钮、开关或业务 UI 触发样式切换。
- 切换前保存地图中心点、缩放、旋转、倾斜等视图状态，切换后恢复。

## 样式配置

不要伪造真实 `style_id`。如果项目已有样式常量，优先复用项目常量；如果没有，生成代码时使用清晰的占位常量。

```js
const MAP_STYLES = {
  day: "YOUR_DAY_STYLE_ID",
  night: "YOUR_NIGHT_STYLE_ID"
};
```

初始化黑夜地图：

```js
Maptec.apiKey = "YOUR_MAPTEC_KEY";

const map = new Maptec.Map({
  container: "map",
  style: MAP_STYLES.night,
  center: [103.8198, 1.3521],
  zoom: 12,
  bearing: 0,
  pitch: 0
});
```

## 运行时切换

`maptec-js` 的 `Map` 类公开了 `setStyle(styleID)`。切换前保存视角，切换后使用 `jumpTo` 恢复。

```js
function switchMapStyle(map, styleID) {
  const viewState = {
    center: map.center,
    zoom: map.zoom,
    bearing: map.bearing,
    pitch: map.pitch
  };

  map.setStyle(styleID);
  map.once("style.load", () => {
    map.jumpTo(viewState);
  });
}
```

如果项目里样式加载完成事件名称不同，可在项目适配层里包装，但不要把不存在的 SDK 方法写进对外文档。

## 按钮切换模板

```js
let currentStyle = "day";

const button = document.createElement("button");
button.type = "button";
button.textContent = "切换昼夜";
button.className = "map-style-toggle";

button.addEventListener("click", () => {
  currentStyle = currentStyle === "day" ? "night" : "day";
  switchMapStyle(map, MAP_STYLES[currentStyle]);
});

document.body.appendChild(button);
```

## 与覆盖物配合

切换底图样式可能导致样式资源重载。生成代码时要注意：

- 业务覆盖物如在样式切换后丢失，应在样式加载完成后重新添加。
- 自定义图片图标可能需要重新 `map.addImage`。
- 切换前保存业务覆盖物数组，必要时统一恢复。

```js
const overlays = [];

function addBusinessOverlay(overlay) {
  map.addOverlay(overlay);
  overlays.push(overlay);
}

function restoreOverlays() {
  overlays.forEach((overlay) => {
    if (!map.getOverlayById?.(overlay.id)) {
      map.addOverlay(overlay);
    }
  });
}
```

## 常见意图映射

| 用户说法 | 实现方式 |
|---|---|
| “将地图切换为黑夜模式” | 使用黑夜样式初始化或调用 `map.setStyle(nightStyleID)` |
| “增加一个按钮切换白天和黑夜地图” | 创建业务按钮，维护 `day/night` 状态，调用 `switchMapStyle` |
| “默认白天，晚上自动黑夜” | 根据时间或业务状态选择 `MAP_STYLES.day/night` |

## 注意事项

- 不要把覆盖物颜色变化当作底图样式切换。
- 不要硬编码未知 `style_id`。
- 不要为了切换样式丢失用户当前视角。
- 切换底图样式后关注自定义图标、业务图层和覆盖物是否需要恢复。

## Agent 规则

- 初始化样式通过 `style` 参数设置；运行时样式切换使用 `map.setStyle(styleID)`。
- 切换样式前应保存中心点、缩放、旋转和倾斜等视角状态，切换后恢复。
- 白天/黑夜样式 ID 或样式地址必须来自已确认配置，不要编造真实 `style_id`。
- 若项目有统一样式常量或封装，优先使用项目已有命名。
