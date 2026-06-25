# 地理编码能力参考

当用户要求把地址、地名、地标、道路或 POI 名称转换为经纬度坐标时，使用本参考。本文件只覆盖功能 **地理编码**。

逆地理编码，即坐标反查地址，请读取 `re-geocoding.md`。

## 能力入口

| 用户需求 | 优先实现 |
|---|---|
| “将新加坡摩天观景轮标注在地图上” | `Geocode.getLocation` 获取坐标，再添加 `Marker` |
| “将地址转换为经纬度坐标” | `Geocode.getLocation(address, options, callback)` |
| “把地名作为路线起终点” | 先 `Geocode.getLocation`，再把 `[lng, lat]` 传给路线规划 |

## Geocode 服务

```js
const geocode = new Maptec.Geocode({
  language: "en",
  region: "SG",
  timeout: 10000
});
```

`GeocodeOptions`:

- `language?: string`：IETF language tag，默认 `"en"`。
- `region?: string`：ccTLD region code，例如 `"SG"` 或 `"BR"`。
- `timeout?: number`：请求超时时间，默认 `10000` 毫秒。

## getLocation

当用户输入地址、地名、地标或道路名，代码需要坐标时使用 `getLocation`。

调用模式：

```js
geocode.getLocation(address, callback);
geocode.getLocation(address, options, callback);
```

示例：

```js
geocode.getLocation("Singapore Flyer", {
  language: "en",
  region: "SG"
}, (error, result) => {
  if (error) {
    console.error("地理编码失败", error);
    return;
  }

  const first = result?.results?.[0];
  const location = first?.geometry?.location;
  if (!location) {
    console.warn("没有地理编码结果", result?.status);
    return;
  }

  const position = [location.longitude, location.latitude];
  map.flyTo({ center: position, zoom: 15 });

  const marker = new Maptec.Marker({ position });
  map.addOverlay(marker);
});
```

`GeocodeLocationOptions`:

- `language?: string`
- `region?: string`
- `components?: string`：过滤格式为 `component:value|component:value`。
- `locationBias?: { southwest: LngLatLike; northeast: LngLatLike }`：偏向某个矩形范围，但不保证结果一定在范围内。

```js
geocode.getLocation("coffee", {
  locationBias: {
    southwest: [103.6, 1.20],
    northeast: [104.1, 1.48]
  }
}, callback);
```

## 结果类型

`GeocodeCallback = (error, result?) => void`。

`GeocodeError`:

- `code: string`
- `message: string`

`GeocodeStatus`:

- `"OK"`
- `"ZERO_RESULTS"`
- `"ERROR"`

`GeocodeResult`:

- `status: GeocodeStatus`
- `results: GeoResult[]`
- `error?: GeocodeError`

`GeoResult`:

- `formattedAddress: string`
- `placeId: string`
- `types: string[]`
- `languageCode: string`
- `geometry: GeocodeGeometry`
- `addressComponents: GeocodeAddressComponent[]`
- `matchDetails: GeocodeMatchDetails`
- `supplementaryInfo: GeocodeSupplementaryInfo`

`GeocodeGeometry`:

- `location: LngLatObject`
- `locationType: GeocodeLocationType`
- `viewport: GeocodeViewport`
- `distance: number`

`GeocodeLocationType`:

- `"ROOFTOP"`
- `"INTERPOLATED"`
- `"CENTER"`

`GeocodeViewport`:

- `southwest: LngLatObject`
- `northeast: LngLatObject`

## 坐标转换

地理编码结果中的 `location` 是对象形式，需要转换为 `[lng, lat]`。

```js
function toLngLatFromGeocode(location) {
  if (!location) return null;
  return [location.longitude, location.latitude];
}
```

转换后可传给 `Marker`、`Popup`、`Driving.search`、`fitBounds`、`flyTo` 或 `GeoJSON`。

## 路线规划集成

```js
async function geocodeOne(query, region = "SG") {
  return new Promise((resolve, reject) => {
    geocode.getLocation(query, { region }, (error, result) => {
      if (error) {
        reject(error);
        return;
      }

      const location = result?.results?.[0]?.geometry?.location;
      if (!location) {
        reject(new Error(`No geocode result: ${query}`));
        return;
      }

      resolve([location.longitude, location.latitude]);
    });
  });
}
```

## 注意事项

- 不要使用 `[location.latitude, location.longitude]`；必须转换成 `[longitude, latitude]`。
- `locationBias` 只是偏向，不是硬边界过滤。
- 必须处理 `ZERO_RESULTS` 和空 `results`。
- 地址或地名作为路线起终点时，先地理编码，再调用路线规划。
- 对关键业务可使用 `matchDetails` 判断低置信度结果，不要直接绘制高风险结果。

## Agent 规则

- 地址、地名、地标或道路名称转坐标必须使用 `Maptec.Geocode.getLocation`。
- 地理编码结果必须从 `geometry.location` 转换为 `[longitude, latitude]`，不能写成 `[latitude, longitude]`。
- 必须处理错误、`ZERO_RESULTS` 和空 `results`。
- 地理编码结果用于 Marker 或路线规划前，应确认存在有效坐标。
