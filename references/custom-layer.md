# 自定义 WebGL 与 Three.js 图层参考

当用户要求在 Maptec 地图中绘制自定义 WebGL 内容、加载 GLTF/GLB 三维模型或接入 Three.js 渲染时，使用本参考。这是高级能力，应优先使用内置 Overlay；只有内置能力无法表达需求时才使用自定义图层。

## 已确认接口

- `Maptec.CustomLayerInterface`（TypeScript 类型，仅工程化接入时使用，不是运行时构造器）
- `map.addCustomLayer(layer, beforeId?)`
- `map.removeCustomLayer(layerOrId)`
- `Maptec.MercatorCoordinate.fromLngLat(lngLat, altitude?)`
- `mercatorCoordinate.meterInMercatorCoordinateUnits()`
- `map.triggerRepaint()`

`CustomLayerInterface` 必须包含唯一 `id`、`type: "custom"` 和 `render`。可选 `renderingMode`、`onAdd`、`onRemove`、`prerender`。

## 最小生命周期

```js
const customLayer = {
  id: "custom-webgl-layer",
  type: "custom",
  renderingMode: "3d",

  onAdd(mapInstance, gl) {
    this.map = mapInstance;
    // 在这里创建 shader、program、buffer、texture 和事件 listener。
  },

  render(gl, args) {
    const matrix = args.defaultProjectionData.mainMatrix;
    // 使用共享 GL context 绘制。
  },

  onRemove(mapInstance, gl) {
    // 删除当前图层创建的 GL 资源并解绑事件。
  }
};

map.on("load", () => {
  map.addCustomLayer(customLayer);
});

function cleanup() {
  map.removeCustomLayer(customLayer);
}
```

`renderingMode: "3d"` 使用共享深度缓冲；`"2d"` 不使用共享三维深度。需要离屏 framebuffer 时在 `prerender` 中处理。

## Three.js 坐标转换

```js
const modelOrigin = [103.8522, 1.29];
const modelAltitude = 0;
const mercator = Maptec.MercatorCoordinate.fromLngLat(
  modelOrigin,
  modelAltitude
);

const transform = {
  translateX: mercator.x,
  translateY: mercator.y,
  translateZ: mercator.z,
  scale: mercator.meterInMercatorCoordinateUnits(),
  rotateX: Math.PI / 2,
  rotateY: 0,
  rotateZ: 0
};
```

`MercatorCoordinate` 用于把 `[lng, lat]` 和海拔转换为地图世界坐标。模型缩放必须乘 `meterInMercatorCoordinateUnits()`，不能直接把米当作 Three.js 世界单位。

## Three.js 图层骨架

```js
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const threeLayer = {
  id: "three-model",
  type: "custom",
  renderingMode: "3d",

  onAdd(mapInstance, gl) {
    this.map = mapInstance;
    this.camera = new THREE.Camera();
    this.scene = new THREE.Scene();

    this.renderer = new THREE.WebGLRenderer({
      canvas: mapInstance.getCanvas(),
      context: gl,
      antialias: true
    });
    this.renderer.autoClear = false;

    const loader = new GLTFLoader();
    loader.load(
      "/models/model.gltf",
      (gltf) => {
        this.model = gltf.scene;
        this.scene.add(gltf.scene);
        this.map.triggerRepaint();
      },
      undefined,
      (error) => console.error("三维模型加载失败", error)
    );
  },

  render(gl, args) {
    if (!this.renderer || !this.camera) return;

    const rotationX = new THREE.Matrix4().makeRotationX(transform.rotateX);
    const rotationY = new THREE.Matrix4().makeRotationY(transform.rotateY);
    const rotationZ = new THREE.Matrix4().makeRotationZ(transform.rotateZ);

    const projection = new THREE.Matrix4().fromArray(
      args.defaultProjectionData.mainMatrix
    );
    const model = new THREE.Matrix4()
      .makeTranslation(
        transform.translateX,
        transform.translateY,
        transform.translateZ
      )
      .scale(new THREE.Vector3(
        transform.scale,
        -transform.scale,
        transform.scale
      ))
      .multiply(rotationX)
      .multiply(rotationY)
      .multiply(rotationZ);

    this.camera.projectionMatrix = projection.multiply(model);
    this.renderer.resetState();
    this.renderer.render(this.scene, this.camera);
  },

  onRemove(mapInstance, gl) {
    this.scene?.traverse((object) => {
      object.geometry?.dispose?.();
      if (Array.isArray(object.material)) {
        object.material.forEach((material) => material.dispose?.());
      } else {
        object.material?.dispose?.();
      }
    });
    this.renderer?.dispose();
    this.scene = null;
    this.camera = null;
    this.renderer = null;
  }
};

const map = new Maptec.Map({
  container: "map",
  style: "light",
  center: modelOrigin,
  zoom: 17,
  pitch: 60,
  canvasContextAttributes: { antialias: true }
});
```

持续动画时在 `render` 末尾调用 `map.triggerRepaint()`；静态模型只在资源加载、动画状态或视图外部状态变化时请求下一帧，避免无意义的永久刷新。

## GL 状态与安全边界

- Maptec 与自定义层共享同一个 GL context；每帧不要假定除混合/深度约定外的其他 GL 状态。
- Three.js 绘制前调用 `renderer.resetState()`，并保持 `autoClear = false`。
- 默认混合约定使用预乘 alpha；自定义混合函数后应恢复所需状态。
- `onRemove` 删除 buffer、texture、program、framebuffer，释放 Three.js geometry/material/texture/renderer，并解绑 DOM/地图事件。
- 模型 URL、CORS、资源大小、压缩格式和许可证必须由业务确认。
- WebGL context lost/restored 场景需要能重建资源；不能把只在 `onAdd` 创建且不可恢复的状态当成可靠生产实现。

## Agent 规则

- 内置 Overlay 能完成的需求不使用自定义 GL 图层。
- 自定义层必须设置唯一 `id`、`type: "custom"`、`render` 和完整 `onRemove` 清理。
- 经纬度转模型坐标必须使用 `Maptec.MercatorCoordinate.fromLngLat`。
- 不要把米直接当作 Mercator/Three.js 单位，必须使用 `meterInMercatorCoordinateUnits()`。
- Three.js 复用地图 canvas 和 GL context，必须 `autoClear = false` 并在渲染前 `resetState()`。
- 需要持续动画时才循环调用 `triggerRepaint`；静态场景避免常驻渲染。
