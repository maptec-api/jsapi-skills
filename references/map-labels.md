# 底图标注语言与显隐参考

当用户要求切换底图道路/POI 名称语言、显示或隐藏底图文字和图标时，使用本参考。

## 能力入口

| 用户需求 | 实现方式 |
|---|---|
| “底图显示中文” | 初始化 `language: "zh"` 或设置 `map.language = "zh"` |
| “底图显示英文” | 初始化 `language: "en"` 或设置 `map.language = "en"` |
| “优先显示当地语言” | `map.language = "local"` |
| “隐藏底图 POI 图标和文字” | 初始化 `showLabels: false` 或调用 `map.setLabelsVisible(false)` |

底图 `map.language` 与 `PlaceSearch`、`Geocode`、`Driving` 请求中的 `language` 是不同作用域。前者改变地图标注，后者改变服务返回文本；需要一致时应分别设置。

## 初始化配置

```js
const map = new Maptec.Map({
  container: "map",
  style: "light",
  center: [103.8198, 1.3521],
  zoom: 11.5,
  language: "zh",
  showLabels: true
});
```

- `language?: string | null`：如 `"zh"`、`"en"`、`"local"`。
- `showLabels?: boolean`：是否显示底图标注文字和图标，默认 `true`。

## 运行时语言切换

```js
function setBasemapLanguage(language) {
  map.language = language;
}

setBasemapLanguage("en");
setBasemapLanguage("local");
```

设置为 `null` 或 `undefined` 会取消语言覆盖。不要把用户界面语言自动当作底图语言，除非产品需求明确要求联动。

## 运行时显隐

```js
map.setLabelsVisible(false);
map.setLabelsVisible(true);
```

`setLabelsVisible` 控制底图标注文字和图标，不会隐藏业务 Marker、Popup 或 Overlay。

## 与样式切换结合

样式切换后应在 `style.load` 时重新应用所需语言和显隐状态：

```js
let labelLanguage = "zh";
let labelsVisible = true;

map.on("style.load", () => {
  map.language = labelLanguage;
  map.setLabelsVisible(labelsVisible);
});
```

清理业务 UI 时移除按钮监听；如果临时修改了共享地图实例，按产品约定恢复原语言和显隐状态。

## Agent 规则

- 明确区分底图标注语言与服务返回语言，不能只设置其中一个却声称两者都已切换。
- `showLabels` 必须是 boolean；运行时使用 `map.setLabelsVisible(boolean)`。
- `map.language` 使用确认过的语言代码或 `"local"`，不要虚构 SDK 专用枚举。
- 隐藏底图标注不会隐藏业务覆盖物；业务 Overlay 显隐应单独处理。
