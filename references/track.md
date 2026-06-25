# 轨迹动画参考

当用户要求车辆、人员、设备、船舶等图标沿路线移动，或者要求轨迹回放、暂停、继续、停止、视角跟随、相机过渡、相机绕点旋转时，使用本参考。

## 能力范围

`maptec-js` 已公开导出以下动画能力：

- `Maptec.AnimationManager`
- `Maptec.AnimationKeyFrameTrack`
- `Maptec.PointKeyFrameTrack`
- `Maptec.PolylineKeyFrameTrack`
- `Maptec.CameraKeyFrameTrack`
- `Maptec.CameraOrbitKeyFrameTrack`

常见组合：

- 使用 `PolylineOverlay` 展示完整轨迹线。
- 使用 `PointKeyFrameTrack` 驱动 `Marker` 或 `CircleOverlay` 沿路径移动。
- 使用 `PolylineKeyFrameTrack` 驱动 `PolylineOverlay` 逐步增长，展示行驶轨迹。
- 使用 `CameraKeyFrameTrack` 实现镜头过渡。
- 使用 `CameraOrbitKeyFrameTrack` 实现相机绕点旋转。
- 真实道路路径来自路线规划时，先使用 `Driving` / `TruckDriving` 获取路线，再把路线坐标用于动画。

## 基础轨迹动画

```js
const path = [
  [103.8318, 1.3048],
  [103.8198, 1.3521],
  [103.7764, 1.2966]
];

const fullLine = new Maptec.PolylineOverlay({
  positions: path,
  strokeColor: "#c4b5fd",
  strokeWeight: 6,
  strokeOpacity: 0.45
});

const animatedLine = new Maptec.PolylineOverlay({
  positions: path,
  strokeColor: "#7c3aed",
  strokeWeight: 6,
  strokeOpacity: 0.95,
  showDirection: true
});

const vehicle = new Maptec.Marker({
  position: path[0],
  color: "#ef4444",
  scale: 1.1
});

map.on("load", () => {
  map.addOverlay([fullLine, animatedLine, vehicle]);

  const lineTrack = new Maptec.PolylineKeyFrameTrack(animatedLine, {
    duration: 8,
    interpolation: "linear"
  });

  const vehicleTrack = new Maptec.PointKeyFrameTrack(vehicle, {
    path,
    duration: 8,
    interpolation: "linear",
    autoRotate: true,
    rotateOffset: 0
  });

  map.animation.add(lineTrack);
  map.animation.add(vehicleTrack);

  lineTrack.play();
  vehicleTrack.play();
});
```

## 播放控制

`PointKeyFrameTrack`、`PolylineKeyFrameTrack` 等轨道继承自 `AnimationKeyFrameTrack`，常用控制方法包括：

- `play()`
- `pause()`
- `stop()`
- `reset()`

```js
const track = new Maptec.PointKeyFrameTrack(vehicle, {
  path,
  duration: 10,
  autoRotate: true,
  rotateOffset: 0
});

map.animation.add(track);

playButton.onclick = () => track.play();
pauseButton.onclick = () => track.pause();
stopButton.onclick = () => {
  track.stop();
  track.reset();
};
```

## 车头朝向

`PointKeyFrameTrack` 支持 `autoRotate`。当移动目标是 `Marker` 时，轨道会根据路径方向设置 `marker.rotation`。如果自定义图标素材的“正前方”不是默认方向，用 `rotateOffset` 修正。

```js
const carTrack = new Maptec.PointKeyFrameTrack(carMarker, {
  path,
  duration: 12,
  interpolation: "linear",
  autoRotate: true,
  rotateOffset: 90
});
```

## 视图跟随轨迹

可以监听轨道更新，把地图中心移动到当前 Marker 位置。高频调用时建议使用较短 `duration` 或在业务侧做节流。

```js
const track = new Maptec.PointKeyFrameTrack(droneMarker, {
  path,
  duration: 12,
  autoRotate: true,
  rotateOffset: 0
});

track.on("update", () => {
  map.easeTo({
    center: droneMarker.position,
    zoom: 14,
    duration: 180
  });
});

map.animation.add(track);
track.play();
```

## 镜头过渡

```js
const cameraTrack = new Maptec.CameraKeyFrameTrack([
  { center: [103.8198, 1.3521], zoom: 11, pitch: 0, bearing: 0 },
  { center: [103.8519, 1.2903], zoom: 15, pitch: 55, bearing: 120 }
], {
  duration: 8,
  interpolation: "easeInOut"
});

map.animation.add(cameraTrack);
cameraTrack.play();
```

## 相机绕点旋转

```js
const orbitTrack = new Maptec.CameraOrbitKeyFrameTrack({
  duration: 10,
  center: [103.8519, 1.2903],
  radius: 1000,
  startBearing: 0,
  bearingRange: 360,
  iteration: "INFINITE",
  interpolation: "linear"
});

map.animation.add(orbitTrack);
orbitTrack.play();
```

## 与路线规划结合

如果用户说“沿真实驾车路线移动”“从 A 到 B 轨迹回放”，不能手写虚假路径。应先使用 `Geocode` 转换地址，再用 `Driving.search` 或 `TruckDriving.search` 获取路线。

```js
const driving = new Maptec.Driving({
  map,
  enableDrawRoute: true,
  strokeColor: "#2563eb",
  strokeWeight: 6
});

driving.search(origin, destination, (error, result) => {
  if (error) {
    console.error("路线规划失败", error);
    return;
  }

  const route = result?.routes?.[0];
  const path = route?.path || [];
  if (path.length < 2) {
    console.warn("路线结果没有可用于动画的轨迹坐标");
    return;
  }

  const vehicle = new Maptec.Marker({ position: path[0] });
  const track = new Maptec.PointKeyFrameTrack(vehicle, {
    path,
    duration: 15,
    autoRotate: true
  });

  map.addOverlay(vehicle);
  map.animation.add(track);
  track.play();
});
```

## 常见意图映射

| 用户说法 | 实现方式 |
|---|---|
| “让小车图标沿路线移动” | `Marker` + `PointKeyFrameTrack` |
| “行驶轨迹要显示出来” | `PolylineOverlay` 展示底线，`PolylineKeyFrameTrack` 驱动动画线增长 |
| “车头一直朝轨迹方向” | `PointKeyFrameTrack({ autoRotate: true, rotateOffset })` |
| “实现轨迹回放并支持暂停、继续、停止” | 使用轨道的 `play/pause/stop/reset` |
| “视角跟随车辆/无人机” | 监听轨道 `update`，调用 `map.easeTo({ center })` |
| “镜头从 A 点飞到 B 点” | `CameraKeyFrameTrack` |
| “绕建筑或中心点旋转” | `CameraOrbitKeyFrameTrack` |

## 注意事项

- 不要发明 `Maptec.TrackAnimation`、`Maptec.MoveAnimation` 等未公开类。
- 不要用手写播放循环替代 JSAPI 已提供的关键帧轨道能力。
- 真实道路轨迹必须走路线规划结果。
- `autoRotate` 只会在移动目标是 `Marker` 时更新 `rotation`；若图标方向不对，用 `rotateOffset` 调整。
- 组件卸载时停止轨道并移除 Marker、PolylineOverlay 等覆盖物。

## Agent 规则

- 轨迹动画优先使用 `PointKeyFrameTrack`、`PolylineKeyFrameTrack` 和 `map.animation.add(track)`。
- 轨迹线使用 `PolylineOverlay`，不要生成 `Maptec.Polyline`。
- 移动图标使用 `Marker`；需要自动朝向时设置 `autoRotate: true` 和合适的 `rotateOffset`。
- 用户要求真实道路轨迹时，必须先使用路线规划获取路线坐标。
- 播放器必须提供停止或销毁逻辑，清理时停止轨道并移除轨迹线和移动 Marker。
