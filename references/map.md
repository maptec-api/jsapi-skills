# 地图加载能力参考

当用户要求创建地图实例、初始化加载地图、生成某个城市或国家的地图时，使用本参考。本文件只覆盖功能 **地图加载**。

## 能力入口

| 用户需求 | 优先实现 |
|---|---|
| “生成一个新加坡的地图” | 创建 `new Maptec.Map(...)`，设置容器、样式、中心点和缩放级别 |
| “初始化地图” | 设置 `Maptec.apiKey`，创建地图实例，监听 `load` |
| “打开某个地点的地图” | 明确中心点坐标；若只有地名，先使用地理编码能力 |

## 初始化地图

```js
Maptec.apiKey = "YOUR_MAPTEC_KEY";

const map = new Maptec.Map({
  container: "map",
  style: "YOUR_STYLE_URL",
  center: [103.8198, 1.3521],
  zoom: 11.5,
  bearing: 0,
  pitch: 0
});

map.on("load", () => {
  console.log("地图加载完成");
});
```

## MapOptions 常用字段

- `Maptec.apiKey`: 全局 API Key，必须在创建 `new Maptec.Map(...)` 前设置。
- `Maptec.workerCount` / `Maptec.workerUrl`: WebWorker 配置，如需调整也应在创建地图前设置。
- `container`: `HTMLElement | string`，地图容器。
- `style`: 地图样式地址或项目已确认的样式配置。
- `center`: 地图中心点，坐标顺序必须是 `[lng, lat]`。
- `zoom`: 地图缩放级别。
- `bearing`: 地图旋转角度。
- `pitch`: 地图倾斜角度。
- `minZoom` / `maxZoom`: 缩放范围。
- `minPitch` / `maxPitch`: 倾斜范围。
- `maxBounds`: 限制地图平移范围。
- `logoPosition` / `attributionPosition`: 内置标识和版权信息位置。

## 坐标规则

Maptec JSAPI 地理坐标统一使用 `[lng, lat]`，不要使用 `[lat, lng]`。

```js
const singapore = [103.8198, 1.3521];
```

常见坐标类型：

- `LngLatLike`: `Maptec.LngLat`、`[number, number]`、`{ longitude, latitude }`。
- `LngLatObject`: `{ longitude: number, latitude: number }`，常见于服务返回结果。
- `LngLatBoundsLike`: `[southWest, northEast]` 或 `[west, south, east, north]`。
- `PointLike`: 像素坐标，常用于 `panBy`、Marker 偏移、Popup 偏移。

```js
function toLngLat(input) {
  if (Array.isArray(input) && input.length >= 2) {
    return [Number(input[0]), Number(input[1])];
  }
  if (input && typeof input === "object") {
    const lng = input.longitude ?? input.lng ?? input.lon;
    const lat = input.latitude ?? input.lat;
    if (lng != null && lat != null) return [Number(lng), Number(lat)];
  }
  return null;
}
```

## 加载生命周期

常用方法和事件：

- `map.on("load", handler)`：地图样式和资源加载完成。
- `map.once("load", handler)`：只监听一次加载完成。
- `map.on("error", handler)`：监听地图错误。
- `map.loaded()`：检查地图资源是否已加载。
- `map.destroy()` 或 `map.remove()`：运行时支持时销毁地图。

```js
const onLoad = () => {
  // 添加控件、Marker、矢量覆盖物、信息窗口、路线或检索结果。
};

const onError = (error) => {
  console.error("地图加载错误", error);
};

map.on("load", onLoad);
map.on("error", onError);
```

## 常用区域默认中心和缩放

当用户提到以下地区时，使用对应的默认中心点和缩放级别初始化地图。数据加载完成后通过 `fitBounds` 适配实际视口。

| 地区 | `center` | `zoom` |
|---|---|---|
| 新加坡 / Singapore | `[103.8198, 1.3521]` | `11.5` |
| 泰国 / Thailand | `[100.5018, 13.7563]` | `6` |
| 马来西亚 / Malaysia | `[101.6869, 3.1390]` | `6` |
| 日本 / Japan | `[138.2529, 36.2048]` | `5.5` |
| 韩国 / South Korea | `[127.9780, 36.5712]` | `7` |
| 印度尼西亚 / Indonesia | `[106.8650, -6.1754]` | `5.5` |
| 越南 / Vietnam | `[108.2772, 14.0583]` | `5.5` |
| 中国 / China | `[108.9402, 34.3416]` | `4.5` |
| 美国 / United States | `[-98.5795, 39.8283]` | `4` |
| 英国 / United Kingdom | `[-3.4360, 55.3781]` | `5.5` |
| 沙特阿拉伯 / Saudi Arabia | `[46.6753, 24.7136]` | `5.5` |
| 巴西 / Brazil | `[-47.8822, -15.7939]` | `4.5` |
| 墨西哥 / Mexico | `[-99.1332, 19.4326]` | `5.5` |

> **重要**：不要使用 `center: [0, 0]` 或 `center: [0.0, 0.0]`（大西洋"空岛"）。必须根据用户提及的地区设置合理的默认中心。

## 根据地名加载地图

如果用户只给出地名，不能凭空编造精确坐标。可使用产品默认坐标，或先调用地理编码能力。

```js
geocode.getLocation("Singapore", { region: "SG" }, (error, result) => {
  if (error) {
    console.error("地理编码失败", error);
    return;
  }

  const location = result?.results?.[0]?.geometry?.location;
  if (!location) return;

  const center = [location.longitude, location.latitude];
  map.flyTo({ center, zoom: 11.5 });
});
```

## 注意事项

- 坐标顺序始终使用 `[lng, lat]`。
- 设置 `Maptec.apiKey` 后再创建地图实例。
- 不要在应用代码中依赖 SDK 内部工具类型。
- 不要在地图实例创建前调用地图方法。
- 依赖地图资源的控件、Marker、矢量覆盖物、信息窗口、路线结果应在 `load` 后添加。
- 不要硬编码未知或未确认的 `style_id`。

## Agent 规则

- 生成地图加载代码时，必须先确认容器、样式、中心点和缩放级别。
- 如果用户只提供地名，不要编造精确坐标；应使用地理编码能力或明确使用产品默认中心点。
- 地图相关控件、覆盖物、路线、检索结果和动画对象应在 `load` 后添加。
- 必须说明地图实例销毁方式，优先使用当前 SDK 支持的 `map.destroy()` 或 `map.remove()`。
