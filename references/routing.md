# Maptec Route Planning Reference

Use this reference when planning or rendering driving routes, truck routes, waypoint routes, alternative routes, route styling, route summaries, or turn-by-turn steps.

## 中文能力入口

本文件对应功能 **路线规划**：面向路线规划场景，支持驾车路线规划和路线展示。

| 用户需求 | 优先实现 |
|---|---|
| “绘制一个新加坡国立大学到乌节路的驾车路线” | 先分别地理编码起终点，再 `Maptec.Driving.search` |
| “展示驾车路线” | `new Maptec.Driving({ map, enableDrawRoute: true })` |
| “避开高速/收费路” | 使用 `avoid` 参数 |
| “货车路线” | 使用 `Maptec.TruckDriving` 和车辆规格参数 |

## Capability Selection

- Use `Maptec.Driving` for normal driving routes.
- Use `Maptec.TruckDriving` when the scenario mentions truck, freight, vehicle height/weight/length, cargo constraints, or truck-specific restrictions.
- If the user provides addresses or place names instead of coordinates/place ids, geocode them first with `Maptec.Geocode.getLocation(...)`, then pass `[lng, lat]` coordinates into route search.
- Do not use a hand-drawn `Polyline` as a substitute for route planning when the requirement is a real route. Use `Driving`/`TruckDriving`; optionally render or restyle the returned path afterward.
- Route planning results must mark direction with start/end icons. Use `Maptec.Marker` at origin/destination or the returned route path endpoints, for example green "起" and red "终"; include these markers in cleanup.

## DrivingOptions

Create the service with a map instance:

- `map: Map`
- `enableDrawRoute?: boolean`. Default `true`; when true, SDK draws the selected route.
- `strokeColor?: string`. Default `"#3FB1CE"`.
- `strokeWeight?: number`. Default `6`.
- `timeout?: number`. Default `10000`.

```js
const driving = new Maptec.Driving({
  map,
  enableDrawRoute: true,
  strokeColor: "#2563eb",
  strokeWeight: 6,
  timeout: 10000
});
```

## Driving.search

Supported call patterns:

```js
driving.search(origin, destination, callback);
driving.search(origin, destination, options, callback);
```

`origin` and `destination` can be `LngLatLike` coordinates or supported place id strings. Prefer `[lng, lat]` coordinates after geocoding user-provided addresses.

```js
const origin = [103.8318, 1.3048];
const destination = [103.7764, 1.2966];

driving.search(origin, destination, {
  strategy: "fastest",
  alternatives: true,
  language: "en-GB",
  units: "metric"
}, (error, result) => {
  if (error) {
    console.error("Driving search failed", error);
    return;
  }

  const route = result?.routes?.[0];
  if (!route) {
    console.warn("No route found", result?.status);
    return;
  }

  console.log(route.summary.distanceMeters, route.summary.durationSeconds);
});
```

## 起终点方向标识

路线绘制完成后，应使用 `Maptec.Marker` 标识起点和终点，帮助用户确认路线方向。推荐起点使用绿色“起”，终点使用红色“终”。如果起终点来自地址或地名，先解析为坐标；如果路线结果返回 `route.path`，也可以用路径首尾点标识。

```js
function createRouteEndpointElement(label, color) {
  const element = document.createElement("div");
  element.textContent = label;
  Object.assign(element.style, {
    width: "30px",
    height: "30px",
    borderRadius: "999px",
    border: "2px solid #ffffff",
    background: color,
    color: "#ffffff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "800"
  });
  return element;
}

const startMarker = new Maptec.Marker({
  position: origin,
  element: createRouteEndpointElement("起", "#16a34a"),
  anchor: "bottom"
});

const endMarker = new Maptec.Marker({
  position: destination,
  element: createRouteEndpointElement("终", "#dc2626"),
  anchor: "bottom"
});

map.addOverlay(startMarker);
map.addOverlay(endMarker);
```

## DirectionsCommonSearchOptions

`DrivingSearchOptions = DirectionsCommonSearchOptions`.

Fields:

- `waypoints?: LngLatLike[]`. Intermediate points.
- `departureTime?: string`. ISO 8601, for example `"2025-10-31T10:00:00Z"`.
- `strategy?: "fastest" | "shortest" | "eco" | "balanced"`. Default `"fastest"`.
- `alternatives?: boolean`. Default `false`.
- `language?: string`. Default `"en-GB"`.
- `units?: "metric" | "imperial"`. Default `"metric"`.
- `avoid?: DrivingAvoid`.
- `bearing?: number`. Origin heading `0..359`, helps road snapping.
- `radius?: number`. Origin/destination matching radius in meters.

```js
driving.search(origin, destination, {
  waypoints: [[103.82, 1.31]],
  strategy: "shortest",
  alternatives: true,
  avoid: { criteria: ["tolls", "ferries"] },
  bearing: 90,
  radius: 50
}, callback);
```

## DrivingAvoid

`DrivingAvoid`:

- `criteria?: ("tolls" | "highways" | "ferries")[]`
- `areas?: string[]`. AI-defined areas such as `["high_crime_zones"]`.
- `polygons?: any[]`. GeoJSON Polygon Geometry objects.

```js
const avoid = {
  criteria: ["tolls", "ferries"],
  polygons: [
    {
      type: "Polygon",
      coordinates: [[
        [100.505, 13.760],
        [100.515, 13.760],
        [100.515, 13.768],
        [100.505, 13.768],
        [100.505, 13.760]
      ]]
    }
  ]
};
```

## TruckDriving

`Maptec.TruckDriving` uses the same search pattern as `Driving`, with truck-specific `vehicleSpec`.

`TruckDrivingSearchOptions = DirectionsCommonSearchOptions & { vehicleSpec?: DrivingVehicleSpec }`.

Use `TruckDrivingSearchOptions` when the route must consider truck dimensions, gross weight, cargo, or truck-restricted roads. If `vehicleSpec` is omitted, the server plans with generic truck defaults.

`DrivingVehicleSpec`:

- `heightMeters?: number`
- `lengthMeters?: number`
- `weightTons?: number`
- `payloadType?: string[]`

```js
const truck = new Maptec.TruckDriving({
  map,
  enableDrawRoute: true
});

truck.search(origin, destination, {
  vehicleSpec: {
    heightMeters: 4.2,
    weightTons: 40,
    lengthMeters: 16
  },
  avoid: { criteria: ["ferries"] },
  alternatives: true
}, callback);
```

Truck search supports the same call patterns:

```js
truck.search(origin, destination, callback);
truck.search(origin, destination, truckOptions, callback);
```

Truck-specific option example:

```js
truck.search(origin, destination, {
  vehicleSpec: {
    heightMeters: 3.8,
    weightTons: 20,
    lengthMeters: 12
  },
  avoid: { criteria: ["ferries"] },
  alternatives: true,
  strategy: "shortest"
}, (error, result) => {
  if (error) return console.error(error);
  console.log(result?.routes);
});
```

## Result Types

`DrivingCallback = (error, result?) => void`.

`DrivingError`:

- `code: string`
- `message: string`

`DrivingResult`:

- `status: "OK" | "NO_ROUTE_FOUND" | "ERROR"`
- `routes?: DrivingRoute[]`
- `error?: DrivingError`

`DrivingRoute`:

- `summary: DrivingSummary`
- `legs: DrivingLeg[]`
- `path?: LngLat[]`. Route coordinates for custom drawing if needed.
- `warnings?: string[]`

`DrivingSummary`:

- `distanceMeters: number`
- `durationSeconds: number`
- `trafficDurationSeconds?: number`

`DrivingLeg`:

- `startAddress: string`
- `endAddress: string`
- `summary: DrivingSummary`
- `steps: DrivingStep[]`

`DrivingStep`:

- `instruction: string`
- `startLocation: LngLatLike`
- `endLocation: LngLatLike`
- `distanceMeters: number`
- `durationSeconds: number`
- `polyline: string`
- `turnType: string`

## Route From Natural Language Addresses

Use geocoding first, then route planning:

```js
const geocode = new Maptec.Geocode({ region: "SG", language: "en" });
const driving = new Maptec.Driving({ map, enableDrawRoute: true });

function getFirstLocation(query) {
  return new Promise((resolve, reject) => {
    geocode.getLocation(query, { region: "SG" }, (error, result) => {
      if (error) {
        reject(error);
        return;
      }
      const location = result?.results?.[0]?.geometry?.location;
      if (!location) {
        reject(new Error(`No geocode result for ${query}`));
        return;
      }
      resolve([location.longitude, location.latitude]);
    });
  });
}

Promise.all([
  getFirstLocation("Orchard Road, Singapore"),
  getFirstLocation("National University of Singapore")
]).then(([origin, destination]) => {
  driving.search(origin, destination, { strategy: "fastest" }, (error, result) => {
    if (error) return console.error(error);
    const route = result?.routes?.[0];
    if (route?.path?.length) {
      const bounds = route.path.reduce((nextBounds, point) => [
        [
          Math.min(nextBounds[0][0], point[0]),
          Math.min(nextBounds[0][1], point[1])
        ],
        [
          Math.max(nextBounds[1][0], point[0]),
          Math.max(nextBounds[1][1], point[1])
        ]
      ], [route.path[0], route.path[0]]);
      map.fitBounds(bounds, { padding: 80 });
    }
  });
});
```

## Service Methods

Route services expose:

- `search(...)`
- `clear()`: clear drawn route.
- `setActiveRoute(index)`: switch active route by route index when alternatives exist.
- `setStyle(style)`: update route drawing style when supported.

## Pitfalls

- Do not decompose a route request into only markers. A route request must call `Driving.search` or `TruckDriving.search`.
- Do not pass address strings to route search unless the SDK explicitly supports them. Use `Geocode.getLocation` first.
- If `enableDrawRoute` is `true`, avoid also drawing a duplicate custom `Polyline` unless product intentionally needs a second visual.
- When `alternatives: true`, render route selection UI or call `setActiveRoute(...)`; otherwise the user cannot compare alternatives.
- Truck constraints belong in `vehicleSpec`, not in normal `DrivingSearchOptions`.
- Do not use `TruckDriving` for normal passenger-car routing unless the user specifically needs truck restrictions.

## Agent 规则

- 真实路线规划必须使用 `Maptec.Driving.search` 或 `Maptec.TruckDriving.search`，不能用手写折线冒充。
- 起终点是地址、地名或 POI 名称时，必须先使用 `Maptec.Geocode.getLocation` 转换为 `[lng, lat]`。
- 货车路线只有在用户明确提到货车、载重、限高、限宽、货运等约束时才使用 `TruckDriving`。
- 路线结果必须处理 `NO_ROUTE_FOUND`、错误和空 `routes`，不能渲染假路线。
- 路线规划必须使用 `Maptec.Marker` 增加起终点图标，起点标识“起”，终点标识“终”，并在清理阶段移除这两个 Marker。
