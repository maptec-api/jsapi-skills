# 逆地理编码能力参考

当用户要求把经纬度坐标转换为详细地址、点击地图显示地址、或将用户当前位置坐标转换为地址信息时，使用本参考。本文件只覆盖功能 **逆地理编码**。

地址、地名、地标转坐标请读取 `geocoding.md`。

## 能力入口

| 用户需求 | 优先实现 |
|---|---|
| “将用户当前位置坐标转换为详细地址” | 先获取 `[lng, lat]`，再 `Geocode.getAddress` |
| “点击地图显示地址” | `map.on("click")` 获取坐标，再 `Geocode.getAddress` |
| “根据坐标反查地址” | `Geocode.getAddress(lngLatLike, options, callback)` |

## Geocode 服务

逆地理编码和地理编码使用同一个服务类 `Maptec.Geocode`，但方法不同：逆地理编码使用 `getAddress`。

```js
const geocode = new Maptec.Geocode({
  language: "zh-CN",
  region: "SG",
  timeout: 10000
});
```

## getAddress

调用模式：

```js
geocode.getAddress(lngLatLike, callback);
geocode.getAddress(lngLatLike, options, callback);
```

示例：

```js
geocode.getAddress([103.84748, 1.30002], {
  language: "zh-CN",
  region: "SG"
}, (error, result) => {
  if (error) {
    console.error("逆地理编码失败", error);
    return;
  }

  const address = result?.results?.[0]?.formattedAddress;
  if (!address) {
    console.warn("没有逆地理编码结果", result?.status);
    return;
  }

  console.log(address);
});
```

## 点击地图显示地址

```js
let popup = null;

const onMapClick = (event) => {
  const position = Maptec.LngLat.convert(event.lngLat).toArray();

  geocode.getAddress(position, {
    language: "zh-CN",
    region: "SG"
  }, (error, result) => {
    if (error) {
      console.error("逆地理编码失败", error);
      return;
    }

    const address = result?.results?.[0]?.formattedAddress || "未找到地址";

    if (!popup) {
      popup = new Maptec.Popup({
        position,
        text: address,
        closeButton: true,
        closeOnClick: false
      });
      map.addOverlay(popup);
    } else {
      popup.position = position;
      popup.text = address;
    }
  });
};

map.on("click", onMapClick);
```

## 当前位置反查地址

```js
function reverseGeocodeCurrentPosition() {
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

      geocode.getAddress(lngLat, { language: "zh-CN", region: "SG" }, (error, result) => {
        if (error) {
          console.error("逆地理编码失败", error);
          return;
        }

        console.log(result?.results?.[0]?.formattedAddress);
      });
    },
    (error) => {
      console.error("定位失败", error);
    },
    { enableHighAccuracy: true, timeout: 10000 }
  );
}
```

## ReverseGeocodeOptions

逆地理编码参数可能包含以下过滤字段，具体可用值以 SDK 文档和运行时为准：

- `language?: string`：覆盖服务默认语言。
- `region?: string`：覆盖服务默认区域。
- `resultType?: string`：一个或多个地址结果类型，用 `|` 分隔。
- `locationType?: string`：一个或多个精度过滤值，用 `|` 分隔。

```js
geocode.getAddress([103.84748, 1.30002], {
  resultType: "street_address|premise",
  locationType: "ROOFTOP|INTERPOLATED"
}, callback);
```

常见 `resultType`：

- `"country"`
- `"region"`
- `"subregion"`
- `"locality"`
- `"sublocality"`
- `"neighborhood"`
- `"thoroughfare"`
- `"premise"`
- `"subpremise"`
- `"postalCode"`
- `"intersection"`

## 结果类型

`ReverseGeocodeCallback = (error, result?) => void`。

逆地理编码结果结构与 `GeocodeResult` 一致，常用字段：

- `status`
- `results`
- `results[0].formattedAddress`
- `results[0].geometry.location`
- `results[0].addressComponents`
- `error`

## 注意事项

- 输入坐标必须是 `[lng, lat]`。
- `resultType` 和 `locationType` 只过滤返回结果，不改变输入坐标，也不设置搜索半径。
- 必须处理无地址结果、定位失败和权限拒绝。
- 用户当前位置来自浏览器定位，不是 Maptec 逆地理编码自动获取的。

## Agent 规则

- 坐标反查地址必须使用 `Maptec.Geocode.getAddress`，不能用地理编码方法替代。
- 输入坐标必须是 `[lng, lat]`；浏览器定位结果需要转换为 `[longitude, latitude]`。
- 用户当前位置必须通过浏览器定位或业务传入坐标获取，逆地理编码不会自动定位。
- 必须处理定位权限拒绝、服务错误和无地址结果。
