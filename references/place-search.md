# Maptec PlaceSearch Reference

本文件对应功能 **POI检索**：面向 POI 检索场景，支持关键词检索、周边检索、类型检索、详情检索。

| 用户需求 | 优先实现 |
|---|---|
| “搜索新加坡所有咖啡馆并标注在地图上” | `PlaceSearch.search`，`keyword`/`type: "Cafe"`，分页，Marker 渲染 |
| “乌节路附近的餐厅” | 先地理编码乌节路，再 `searchNearby`，`types: "Restaurant"` |
| “搜索某个地点详情” | 先搜索获得 `placeId`，再详情检索 |
| “搜索框输入建议” | `suggest` / autocomplete 能力 |

## 检索功能与适用场景

| 功能 | 适用场景 |
|---|---|
| 关键词检索 | 用户输入明确地点名、品牌名、商户名或自然语言关键词时使用，例如“搜索 Starbucks”“搜索新加坡国立大学”。 |
| 类型检索 | 用户按 POI 类别查找地点时使用，例如“搜索咖啡馆”“搜索新加坡所有餐厅”。需要传入最接近的 `type`，并按分页获取更多结果。 |
| 周边检索 | 用户要求“附近”“周边”“指定半径内”地点时使用，例如“乌节路附近的餐厅”“当前位置 3 公里内的酒店”。必须提供 `locationLimit.center`，可配置 `radius` 和 `types`。 |
| 详情检索 | 已获得 `placeId` 后，需要查询地点详情时使用，例如展示电话、地址、营业时间、照片、摘要等更完整信息。 |

## When To Use Which Search

| User scenario | Use | Required parameters |
|---|---|---|
| "Search Starbucks", "标记新加坡国立大学" | Text search | `keyword`, `region` |
| "Show restaurants in Thailand", "泰国所有餐厅" | Type search | `keyword`, `region`, `type` |
| "Restaurants near me", "周边 3km 餐厅" | Nearby search | `locationLimit.center`, `locationLimit.radius`, optional `types`, `region` |
| "POIs inside this area" | Bounded/range search | `keyword`, `region`, `locationLimit` bounds |
| "All / as many as possible" | Search plus pagination | `nextPageToken`, `pageToken`, `pageSize`, max pages |
| "Search box autocomplete", "搜索框输入建议" | Suggest | `query`, optional `sessionToken`, `types`, `locationBias` |
| "Show details for this POI", "查看地点详情" | Place details | `placeId`, optional `sessionToken`, `language`, `region` |

## Region Selection

Use `new Maptec.PlaceSearch({ region })`.

Common region codes:
- Singapore: `sg`
- Thailand: `th`
- Japan: `jp`
- South Korea: `kr`
- Malaysia: `my`
- Indonesia: `id`
- Vietnam: `vn`
- China: `cn`
- United States: `us`
- United Kingdom: `gb`

If the user does not specify a location, ask a clarifying question or use the product default only if the product already defines one.

## POI Type Mapping

Use the closest supported `type` value from `references/poi-categories.md`. Do not invent unsupported values.

Important rules:

- `search(keyword, options, callback)` uses singular `type`.
- `searchNearby(options, callback)` uses comma-separated `types`.
- Do not pass broad natural-language labels as type values. For example, do not use `school`, `restaurant`, `hotel`, `parking`, `cafe`, `tourist_attraction` unless that exact value is confirmed in `poi-categories.md`.
- If the user gives an exact place name, brand, campus, landmark or address, prefer keyword search without `type`; type filtering can accidentally remove the correct POI.
- If a type-filtered request returns `ZERO_RESULTS`, retry the same keyword without `type/types`, then report that the category filter was too restrictive.

Common mappings:

- 大学 / university / college: `College_University`
- 中学: `Middle_School`
- 小学: `Primary_School`
- 幼儿园: `Kindergarten`
- 培训机构: `Training_Institution`
- 餐厅 / 餐馆 / restaurant: `Restaurant`
- 咖啡 / cafe: `Cafe`
- 酒店 / hotel: `Hotels`、`Star_Rated_Hotel`、`Budget_Hotel_Chain`、`Luxury_Hotel`
- 停车场 / parking: `Parking`、`Indoor_Parking`、`Outdoor_Parking`、`Roadside_Parking`
- 加油站 / gas station: `Gas_Station`
- 充电站 / EV charging: `Ev_Charging_Station`
- 地铁站 / MRT / subway: `Subway_Light_Rail_Station`
- 火车站: `Train_Station`
- 公交站: `Bus_Stop`
- 机场: `Airport`
- 医院 / hospital: `General_Hospital`、`Specialized_Hospital`、`Emergency_Center`
- 诊所 / clinic: `Clinics`、`Private_Clinic`、`Community_Clinic`、`Dental_Clinic`
- 药房 / pharmacy: `Pharmacy`
- 银行 / bank: `Bank`
- ATM: `Atm`
- 商场 / mall: `Shopping_Mall`、`Shopping_Center`
- 超市 / supermarket: `Supermarket`
- 便利店: `Convenience_Store`
- 景点 / attraction: `Tourism_Culture`、`Historic_Site`、`Observation_Deck`
- 公园: `Urban_Park`、`National_Park`、`Nature_Reserve`
- 博物馆: `Museum`
- 图书馆: `Library`
- 健身房: `Gym`

## Service And Option Types

`PlaceSearchOptions` for constructor defaults:

- `language?: string`. Default `"en"`.
- `region?: string`. ccTLD region code.
- `timeout?: number`. Default `10000`.

`PlaceSearchTextOptions` for `search(keyword, options, callback)`:

- `language?: string`
- `region?: string`
- `type?: string`. Single POI category.
- `locationBias?: PlaceSearchLocationArea`. Bias results; mutually exclusive with `locationLimit`.
- `locationLimit?: PlaceSearchLocationArea`. Restrict results; mutually exclusive with `locationBias`.
- `rank?: "RELEVANCE" | "DISTANCE" | "POPULARITY"`. Default `"POPULARITY"`.
- `pageSize?: number`. Range `[1, 20]`, default `20`.
- `pageToken?: string`. Request next page.

`PlaceSearchTextResult`:

- `status: string`. Typical values include `"OK"`, `"ZERO_RESULTS"`, `"ERROR"`.
- `places?: PlaceSearchPlace[] | null`.
- `nextPageToken?: string | null`. Use this as `pageToken` for the next request.
- `error?: { code: string; message: string } | null`.

`PlaceSearchNearbyOptions` for `searchNearby(options, callback)`:

- `locationLimit: { center: LngLatLike; radius?: number }`. Required circular search area, radius default `500` meters.
- `types?: string`. Comma-separated type list, for example `"hotel,restaurant"`.
- `resultLimit?: number`. Range `[1, 20]`, default `20`.
- `rank?: "RELEVANCE" | "DISTANCE" | "POPULARITY"`. Default `"DISTANCE"`.
- `language?: string`
- `region?: string`

`PlaceSearchNearbyResult`:

- `status: string`.
- `places?: PlaceSearchPlace[] | null`.
- `error?: { code: string; message: string } | null`.

`PlaceSearchLocationArea` can be either:

- `LngLatBoundsLike`: rectangle, for example `[[103.8, 1.3], [103.9, 1.4]]`.
- `{ center: LngLatLike; radius: number }`: circle, radius in meters. Radius defaults to `500` meters where the option allows it.

`PlaceSearchPlace` common fields:

- `id: string`、`name: string`、`displayName: { text: string; languageCode: string }`、`formattedAddress: string`、`location: { latitude: number; longitude: number }`、`types: string[]`、`viewport: { northeast: { latitude: number; longitude: number }; southwest: { latitude: number; longitude: number } }`、`phoneNumber: string`、`openingHours`、`photos`、`summary: { text: string; languageCode: string }`。

> **重要**：`location` 是 `{ latitude, longitude }` 对象，直接取值即可。不要把 `location` 写成 `geometry.location`——后者是 Google Maps API 的结构，Maptec 中不存在。

Callback types:

- `PlaceSearchCallback = (error?, result?) => void`, result type `PlaceSearchTextResult`.
- `PlaceSearchNearbyCallback = (error?, result?) => void`, result type `PlaceSearchNearbyResult`.
- `PlaceSearchDetailsCallback = (error?, result?) => void`, result type `PlaceSearchDetailsResult`.
- `PlaceSearchSuggestCallback = (error?, result?) => void`, result type `PlaceSearchSuggestResult`.

## Text Search

Use `search(keyword, callback)` or `search(keyword, options, callback)` for keyword/type search.

```js
const placeSearch = new Maptec.PlaceSearch({
  language: "zh-CN",
  region: "sg"
});

placeSearch.search("restaurant", {
  type: "Restaurant",
  region: "sg",
  language: "zh-CN",
  pageSize: 20,
  rank: "POPULARITY"
}, (error, result) => {
  if (error) return console.error(error);
  const places = result?.places || [];
  console.log(places);
});
```

Use `locationBias` to bias results near an area, and `locationLimit` to restrict results to an area. They are mutually exclusive.

```js
placeSearch.search("hotel", {
  locationBias: {
    center: [103.8198, 1.3521],
    radius: 5000
  },
  rank: "DISTANCE"
}, callback);

placeSearch.search("restaurant", {
  locationLimit: [[103.8, 1.3], [103.9, 1.4]]
}, callback);
```

## Type Search Template

Use this when the user asks for category results in a region, such as "泰国所有餐厅".

```html
<script>
Maptec.apiKey = "YOUR_MAPTEC_KEY";

const map = new Maptec.Map({
  container: "map",
  style: "https://test-api.maptec.com/maps/v1/styles?style_id=style_00001",
  center: [100.5018, 13.7563],
  zoom: 6
});

map.on("load", () => {
  const search = new Maptec.PlaceSearch({ region: "th" });
  const renderLimit = 80;
  const collectedPlaces = [];
  const renderedKeys = new Set();

  const toLngLat = (location) => {
    if (!location) return null;
    if (Array.isArray(location)) return location;
    const lng = location.longitude ?? location.lng ?? location.lon;
    const lat = location.latitude ?? location.lat;
    return lng == null || lat == null ? null : [lng, lat];
  };

  const getNextPageToken = (result) =>
    result?.nextPageToken || result?.next_page_token || result?.pageToken || result?.nextToken;

  const mergeUniquePlaces = (places) => {
    const seen = new Set(collectedPlaces.map((place) => {
      const position = toLngLat(place.location);
      return `${place.id || place.placeId || place.name}:${position?.[0]},${position?.[1]}`;
    }));

    places.forEach((place) => {
      const position = toLngLat(place.location);
      const key = `${place.id || place.placeId || place.name}:${position?.[0]},${position?.[1]}`;
      if (!seen.has(key)) {
        seen.add(key);
        collectedPlaces.push(place);
      }
    });
  };

  const renderMarkers = () => {
    collectedPlaces.slice(0, renderLimit).forEach((place) => {
      const position = toLngLat(place.location);
      if (!position) return;
      const markerKey = `${place.id || place.placeId || place.name}:${position[0]},${position[1]}`;
      if (renderedKeys.has(markerKey)) return;
      renderedKeys.add(markerKey);

      const title = place.displayName?.text || place.name || "Unknown place";
      const address = place.formattedAddress || place.address || "";
      const type = place.types?.[0] || "";
      const popup = new Maptec.Popup({
        offset: 25,
        html: `<div style="padding: 5px;">
          <strong style="font-size: 14px;">${title}</strong><br>
          <small style="color: #666;">${address}</small>
          ${type ? `<br><small style="color: #999;">${type}</small>` : ""}
        </div>`
      });
      map.addOverlay(new Maptec.Marker({ position, popup }));
    });
  };

  const loadPage = (pageToken) => {
    const options = pageToken
      ? { type: "Restaurant", language: "zh-CN", region: "th", pageSize: 20, pageToken }
      : { type: "Restaurant", language: "zh-CN", region: "th", pageSize: 20 };

    search.search("餐厅", options, (error, result) => {
      if (error) {
        console.error("PlaceSearch failed", error);
        return;
      }

      mergeUniquePlaces(result?.places || []);
      renderMarkers();

      const nextPageToken = getNextPageToken(result);
      if (nextPageToken && collectedPlaces.length < renderLimit) {
        loadPage(nextPageToken);
      }
    });
  };

  loadPage();
});
</script>
```

## Nearby Search Template

Use this when the user explicitly asks for nearby/radius/range. `searchNearby` receives one options object; it does not receive a keyword as the first argument.

```js
const search = new Maptec.PlaceSearch({ region: "sg" });

search.searchNearby({
  locationLimit: {
    center: [103.8198, 1.3521],
    radius: 3000
  },
  types: "restaurant",
  resultLimit: 20,
  language: "zh-CN"
}, (error, result) => {
  if (error) return console.error(error);
  const places = result?.places || [];
  // Render with Maptec.Marker + Maptec.Popup.
});
```

## Suggest Search

Use `suggest(options, callback)` for autocomplete/search-box suggestions. Use the same `sessionToken` for the user typing session and the subsequent detail lookup when applicable.

`PlaceSearchSuggestOptions`:

- `query: string`.
- `language?: string`. Default `"en"`.
- `region?: string`. Default `"SG"` in the SDK docs.
- `types?: string`. Comma-separated types, for example `"restaurant,cafe"`.
- `resultLimit?: number`. Range `[1, 20]`, default `20`.
- `sessionToken?: string`.
- `locationBias?: PlaceSearchLocationArea`.
- `locationLimit?: PlaceSearchLocationArea`.

`PlaceSearchSuggestResult`:

- `status: string`.
- `suggestions?: PlaceSearchSuggestion[] | null`.
- `error?: { code: string; message: string } | null`.

`PlaceSearchSuggestion`:

- `placeId: string`.
- `placeName: string`.
- `text?: { languageCode: string; text: string } | null`.

```js
const sessionToken = crypto.randomUUID();

placeSearch.suggest({
  query: "rest",
  sessionToken,
  types: "restaurant,cafe",
  resultLimit: 10,
  region: "SG",
  locationBias: {
    center: [103.8198, 1.3521],
    radius: 5000
  }
}, (error, result) => {
  if (error) return console.error(error);
  const suggestions = result?.suggestions || [];
  console.log(suggestions.map((item) => item.text?.text));
});
```

## Place Details

Use `getPlaceDetails(options, callback)` when you already have a `placeId` from `search`, `searchNearby`, or `suggest` and need richer place information.

`PlaceSearchDetailsOptions`:

- `placeId: string`. Required.
- `language: string`. Use when you need localized details.
- `region: string`. Use when you need regional bias/context.
- `sessionToken: string`. Use the same token from `suggest` when details are selected from autocomplete.

`PlaceSearchDetailsResult`:

- `status: string`.
- `places?: PlaceSearchPlace | null`. Details returns a single place object, not an array.
- `error?: { code: string; message: string } | null`.

```js
placeSearch.getPlaceDetails({
  placeId: "osm-node-10004862482_v0.1",
  sessionToken,
  language: "zh-CN",
  region: "SG"
}, (error, result) => {
  if (error) return console.error(error);
  const place = result?.places;
  console.log(place?.displayName?.text, place?.formattedAddress, place?.phoneNumber);
});
```

## Known Pitfalls

- **字段名 `places` 而非 `results`**：`PlaceSearchTextResult` 和 `PlaceSearchNearbyResult` 的结果数组字段是 `places`，不是 `results`。不要写成 `result.results`，这是 Google Maps API 的字段名，Maptec 中不存在。
- **字段名 `location` 而非 `geometry.location`**：`PlaceSearchPlace` 的坐标字段是 `location`，直接包含 `latitude` 和 `longitude` 属性。不要写成 `place.geometry?.location`，这是 Google Maps API 的结构，Maptec 中不存在。正确用法：`place.location.latitude`、`place.location.longitude`，或使用 `toLngLat(place.location)` 辅助函数转为 `[lng, lat]`。
- A single text search page returns at most `pageSize` results, with documented range `[1, 20]`. Use `nextPageToken` from the result as `pageToken` for broad requests.
- Nearby search returns at most `resultLimit` results, with documented range `[1, 20]`.
- `nextPageToken` is for pagination, not for choosing the search type.
- `type` is what makes text search category/type constrained; `types` is used by nearby search.
- Do not use `locationBias` for a whole-country category search unless the user asked for biasing near a location.
- Use `locationLimit` for nearby/radius search and bounded search.
- Do not pass a keyword to `searchNearby`; nearby search is `searchNearby(options, callback)`.
- Do not treat details result `places` as an array; `PlaceSearchDetailsResult.places` is a single `PlaceSearchPlace | null`.
- Keep the same `sessionToken` across `suggest` and `getPlaceDetails` for one autocomplete session when using interactive search.
- Do not reuse Singapore defaults for Thailand, China, or other regions. The `region`, map center, and zoom must match the user's requested geography.
- Do not render fake markers for real-world search results. If `PlaceSearch` returns no valid coordinates, show the failure or empty state.
- If the SDK does not return any pagination token, state that only one page can be rendered from the front end.
- Keep generated code and actual map rendering logic identical.

## Agent 规则

- 真实 POI 必须来自 `Maptec.PlaceSearch` 返回结果，不要伪造咖啡馆、餐厅、酒店、地址或坐标。
- 关键词检索和类型检索使用 `search(keyword, options, callback)`；周边检索使用 `searchNearby(options, callback)`。
- “全部”“尽可能多”等需求必须说明分页、前端渲染上限和 `nextPageToken` 限制。
- 结果为空、服务错误、坐标缺失时必须显式处理，不要渲染假 Marker。
