import * as THREE from 'three';
import { PointerLockControls } from 'three/examples/jsm/controls/PointerLockControls.js';
import { Sky } from 'three/examples/jsm/objects/Sky.js';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import { PianoBGM } from './bgm.js';

// --- ゲーム状態管理 ---
let soundEnabled = true;
const clock = new THREE.Clock();
const bgm = new PianoBGM();

// 物理演算（ジャンプと重力）パラメータ
let velocityY = 0;
const gravity = 22.0;       // 重力の強さ
const jumpStrength = 8.5;   // ジャンプの初速
let isGrounded = true;      // 接地フラグ

// 操作キーの状態
const keys = { w: false, a: false, s: false, d: false, space: false };

// エリア設定
const areaSize = 150; // 150m x 150m の範囲

// ランドマーク（湖）の設定
const lakeX = 40;
const lakeZ = -30;
const lakeRadius = 22;
const lakeInfluenceRadius = 28; // 湖畔へ繋ぐ緩やかなスロープの影響半径

// 基準高度（湖の窪みを作る前の起伏）を計算する関数
function getBaseTerrainHeight(x, z) {
  let y = Math.sin(x * 0.04) * Math.cos(z * 0.04) * 4.0;
  y += Math.sin(x * 0.015) * 8.0; // 大きな起伏
  y += Math.cos(z * 0.01) * 6.0;
  y += Math.sin(x * 0.1) * Math.cos(z * 0.1) * 0.8; // 細かな凸凹
  return y;
}

const lakeBaseHeight = getBaseTerrainHeight(lakeX, lakeZ); // 湖の中心の基準高度 (約 12.3m)
const waterHeight = lakeBaseHeight - 2.5; // 水面の高さを基準高度から2.5m下がった位置に設定 (約 9.8m)

// ランドマーク（モニュメント）の設定
const monumentX = -30;
const monumentZ = 30;
const monumentRadius = 3.6; // 衝突判定用の半径
let monumentCrystal; // アニメーション回転用のグローバル参照
let waterMesh;       // 水面アニメーション用のグローバル参照

// --- 1. 地形の高さ計算 (数理的に丘を生成) ---
function getTerrainHeight(x, z) {
  let y = getBaseTerrainHeight(x, z);
  
  // 湖の窪みとアプローチスロープを作る
  const dx = x - lakeX;
  const dz = z - lakeZ;
  const distToLake = Math.sqrt(dx*dx + dz*dz);
  
  if (distToLake < lakeInfluenceRadius) {
    if (distToLake >= lakeRadius) {
      // 緩やかな湖畔へのスロープ (28m から 22m にかけて水面の高さへ近づける)
      const slopeFactor = (lakeInfluenceRadius - distToLake) / (lakeInfluenceRadius - lakeRadius);
      y = THREE.MathUtils.lerp(y, waterHeight, Math.pow(slopeFactor, 1.2));
    } else {
      // 湖の内部 (22m から 0m)。湖畔 (22m) は完全に waterHeight と一致し、中心部ほど深くなる
      const depthFactor = (lakeRadius - distToLake) / lakeRadius;
      const maxDepth = 5.5; // 最大水深 5.5m
      y = waterHeight - Math.pow(depthFactor, 1.5) * maxDepth;
    }
  }
  
  return y;
}

// --- 2. シーン・カメラ・レンダラーのセットアップ ---
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0xd6eaff, 0.008); // 澄み渡る昼間の青い霧で遠景をなじませる

const camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.1, 1000);
// 初期位置 (中央の丘の上に配置)
camera.position.set(0, getTerrainHeight(0, 0) + 1.8, 0);

const canvas = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.85;

// --- 3. 一人称視点コントロール (PointerLockControls) ---
let controls;

document.addEventListener('DOMContentLoaded', () => {
  controls = new PointerLockControls(camera, document.body);
  
  const playButton = document.getElementById('play-button');
  const blocker = document.getElementById('blocker');

  if (playButton) {
    playButton.addEventListener('click', () => {
      controls.lock();
    });
  }

  controls.addEventListener('lock', () => {
    if (blocker) {
      blocker.style.opacity = '0';
      setTimeout(() => {
        blocker.style.display = 'none';
      }, 800);
    }
    
    if (soundEnabled) {
      bgm.start();
    }
  });

  controls.addEventListener('unlock', () => {
    if (blocker) {
      blocker.style.display = 'flex';
      setTimeout(() => {
        blocker.style.opacity = '1';
      }, 10);
    }
  });
});

// BGMのオン・オフを切り替える関数
function toggleBGM() {
  soundEnabled = !soundEnabled;
  
  const soundStatus = document.getElementById('sound-status');
  const speakerPath = document.getElementById('speaker-path');
  
  if (soundEnabled) {
    soundStatus.textContent = 'BGM: ON';
    speakerPath.setAttribute('d', 'M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z');
    if (controls && controls.isLocked) {
      bgm.start();
    }
  } else {
    soundStatus.textContent = 'BGM: OFF';
    speakerPath.setAttribute('d', 'M4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4zM16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.21.05-.42.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71z');
    bgm.stop();
  }
}

// キーボードイベントの登録
const handleKeyDown = (e) => {
  const k = e.key.toLowerCase();
  if (k === 'w' || e.key === 'ArrowUp') keys.w = true;
  if (k === 'a' || e.key === 'ArrowLeft') keys.a = true;
  if (k === 's' || e.key === 'ArrowDown') keys.s = true;
  if (k === 'd' || e.key === 'ArrowRight') keys.d = true;
  if (e.code === 'Space') {
    keys.space = true;
    e.preventDefault(); // スペースキーによるブラウザスクロール防止
  }
  if (k === 'm') {
    toggleBGM();
  }
};

const handleKeyUp = (e) => {
  const k = e.key.toLowerCase();
  if (k === 'w' || e.key === 'ArrowUp') keys.w = false;
  if (k === 'a' || e.key === 'ArrowLeft') keys.a = false;
  if (k === 's' || e.key === 'ArrowDown') keys.s = false;
  if (k === 'd' || e.key === 'ArrowRight') keys.d = false;
  if (e.code === 'Space') keys.space = false;
};

document.addEventListener('keydown', handleKeyDown);
document.addEventListener('keyup', handleKeyUp);

// --- 4. 地面 (Terrain) の作成 ---
const terrainGeo = new THREE.PlaneGeometry(areaSize + 40, areaSize + 40, 180, 180);
const posAttr = terrainGeo.attributes.position;
const terrainColors = [];
const tempColor = new THREE.Color();

for (let i = 0; i < posAttr.count; i++) {
  const x = posAttr.getX(i);
  const z = posAttr.getY(i); // 平面形状なのでyをzとして扱う
  const y = getTerrainHeight(x, z);
  posAttr.setZ(i, y); // zを高さに
  
  // 湖底とアプローチスロープにおける頂点カラー（砂利）と陰影の計算
  const dx = x - lakeX;
  const dz = z - lakeZ;
  const distToLake = Math.sqrt(dx*dx + dz*dz);
  
  let gravelRatio = 0;
  if (distToLake < lakeRadius) {
    gravelRatio = 1.0;
  } else if (distToLake < lakeInfluenceRadius) {
    // 湖畔から外側に向けて砂利から草へとブレンド (22m から 28m)
    const factor = (lakeInfluenceRadius - distToLake) / (lakeInfluenceRadius - lakeRadius);
    gravelRatio = Math.pow(factor, 1.5);
  }
  
  if (gravelRatio > 0) {
    // 濡れた砂利の色 (濃いめのグレーブラウン)
    const gravelColor = new THREE.Color(0x54493e);
    
    // 砂利の質感を出すための決定論的ノイズ
    const gravelNoise = 0.82 + (Math.sin(x * 2.2) * Math.cos(z * 2.2) * 0.18);
    gravelColor.multiplyScalar(gravelNoise);
    
    // 水深に応じて影を強くする (深いほど暗く)
    const depth = Math.max(0, waterHeight - y);
    const shadowFactor = Math.min(1.0, depth / 5.5);
    const bottomShadow = 0.45 + (1.0 - shadowFactor) * 0.55;
    gravelColor.multiplyScalar(bottomShadow);
    
    const grassColor = new THREE.Color(0x22441b);
    // 草原の緑から砂利の色へなめらかにブレンド
    tempColor.copy(grassColor).lerp(gravelColor, gravelRatio);
  } else {
    // 通常の草原の緑
    tempColor.setHex(0x22441b);
  }
  terrainColors.push(tempColor.r, tempColor.g, tempColor.b);
}
terrainGeo.setAttribute('color', new THREE.Float32BufferAttribute(terrainColors, 3));
terrainGeo.computeVertexNormals();
// 平面を水平に寝かせる
terrainGeo.rotateX(-Math.PI / 2);

// 地面の質感 (頂点カラーによる芝生と砂利のブレンド)
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, // 頂点カラーを有効化
  roughness: 0.95,
  metalness: 0.01,
  flatShading: true // 少しローポリライクなカット面を出すことで温かみのある陰影を作る
});

const terrain = new THREE.Mesh(terrainGeo, terrainMat);
terrain.receiveShadow = true;
scene.add(terrain);

// --- 5. 風に揺れる草 (InstancedMesh + Custom Shader) ---
const grassCount = 38000; // 密度を向上
const grassWidth = 0.15;  // 葉っぱの幅を広げてボリュームを出す
const grassHeight = 0.8;

// ひねりとカーブを持たせたリアルな草のブレード(葉)を生成
const singleBladeGeo = new THREE.PlaneGeometry(grassWidth, grassHeight, 1, 3);
const bladePos = singleBladeGeo.attributes.position;
for (let i = 0; i < bladePos.count; i++) {
  const y = bladePos.getY(i);
  const factor = y / grassHeight; // 0 (根元) から 1 (先端)
  
  // 先端に行くほど細く
  let x = bladePos.getX(i);
  x *= (1.0 - factor * 0.85);
  bladePos.setX(i, x);
  
  // なだらかなカーブ（Z軸方向への反り）とわずかなひねり
  let z = bladePos.getZ(i);
  z += Math.sin(factor * Math.PI / 2) * 0.12; 
  bladePos.setZ(i, z);
}
singleBladeGeo.computeVertexNormals();
singleBladeGeo.translate(0, grassHeight / 2, 0); // 基準点を底面に

// 2つのブレードを直交（クロス）させてボリュームを出す
const blade1 = singleBladeGeo.clone();
const blade2 = singleBladeGeo.clone();
blade2.rotateY(Math.PI / 2); // 90度回転

// 結合して1つの草の束を作る
const grassGeometry = BufferGeometryUtils.mergeGeometries([blade1, blade2]);

// 草のマテリアル設定 (頂点シェーダーで風揺れ、フラグメントシェーダーで根元から先端へのグラデーションを実装)
const grassMaterial = new THREE.MeshStandardMaterial({
  color: 0x4aa632, // 明るい青々とした緑 (ベース)
  roughness: 0.8,
  metalness: 0.05,
  side: THREE.DoubleSide
});

grassMaterial.onBeforeCompile = (shader) => {
  shader.uniforms.uTime = { value: 0 };
  
  shader.vertexShader = `
    uniform float uTime;
    varying float vHeightFactor; // 根元からの高さ割合をフラグメントへ送る
  ` + shader.vertexShader;
  
  shader.vertexShader = shader.vertexShader.replace(
    '#include <begin_vertex>',
    `
    #include <begin_vertex>
    vec3 wPos = (modelMatrix * instanceMatrix * vec4(position, 1.0)).xyz;
    
    // 風の波（時間と位置で算出）
    float wave = sin(wPos.x * 0.15 + uTime * 2.0) * cos(wPos.z * 0.12 + uTime * 1.5);
    float breeze = sin(wPos.x * 1.5 + uTime * 4.5) * cos(wPos.z * 1.8 + uTime * 3.8) * 0.12;
    
    vHeightFactor = position.y / ${grassHeight};
    
    // 根本は固定し、先端ほど大きく揺らす
    transformed.x += (wave + breeze) * 0.25 * vHeightFactor;
    transformed.z += (wave + breeze) * 0.18 * vHeightFactor;
    `
  );
  
  shader.fragmentShader = `
    varying float vHeightFactor;
  ` + shader.fragmentShader;
  
  shader.fragmentShader = shader.fragmentShader.replace(
    '#include <color_fragment>',
    `
    #include <color_fragment>
    // 根元は影のような濃い深緑、先端は明るい黄緑色へグラデーション
    vec3 bottomColor = vec3(0.06, 0.18, 0.04); // 深緑
    vec3 topColor = diffuseColor.rgb; // 明るい草色
    diffuseColor.rgb = mix(bottomColor, topColor, vHeightFactor);
    `
  );
  
  grassMaterial.userData.shader = shader;
};

const grassMesh = new THREE.InstancedMesh(grassGeometry, grassMaterial, grassCount);
grassMesh.castShadow = true;
grassMesh.receiveShadow = true;

const dummy = new THREE.Object3D();
for (let i = 0; i < grassCount; i++) {
  // エリア内にランダム配置
  const x = (Math.random() - 0.5) * areaSize;
  const z = (Math.random() - 0.5) * areaSize;
  const y = getTerrainHeight(x, z);
  
  // 湖の領域（水面下）には草を生やさない (水中への浸入を防ぎリアルにする)
  const dx = x - lakeX;
  const dz = z - lakeZ;
  const distToLake = Math.sqrt(dx*dx + dz*dz);
  if (distToLake < lakeRadius - 1.5 && y < waterHeight) {
    // InstancedMeshのインデックスがデフォルト値（原点）で描画されないよう、位置を地下深く、スケールを0にする
    dummy.position.set(0, -999, 0);
    dummy.scale.set(0, 0, 0);
    dummy.updateMatrix();
    grassMesh.setMatrixAt(i, dummy.matrix);
    continue;
  }
  
  dummy.position.set(x, y - 0.05, z); // 浮き防止のため少し埋める
  dummy.rotation.set(
    (Math.random() - 0.5) * 0.2, // 少しランダムに傾ける
    Math.random() * Math.PI * 2,  // Y軸方向は完全にランダム
    (Math.random() - 0.5) * 0.2
  );
  
  // 草ごとのスケールの揺らぎ
  const scale = 0.55 + Math.random() * 0.75;
  dummy.scale.set(scale, scale * (0.8 + Math.random() * 0.4), scale);
  
  dummy.updateMatrix();
  grassMesh.setMatrixAt(i, dummy.matrix);
  
  // 青々しく瑞々しい緑をベースに、夕日に映えるニュアンスをブレンド
  const col = new THREE.Color();
  const hue = 0.25 + Math.random() * 0.11; // より純粋な緑寄りの色相
  const sat = 0.65 + Math.random() * 0.25; // 彩度を高めて青々しさを表現
  const light = 0.35 + Math.random() * 0.2;  // 明るさのバリエーション
  col.setHSL(hue, sat, light);
  grassMesh.setColorAt(i, col);
}
scene.add(grassMesh);

// --- 5.5. 木 (Trees) の生成と配置 ---
const treePositions = []; // 衝突判定用の座標データ
const treeGroup = new THREE.Group();

// 葉っぱのローポリゴン球体を変形して、もこもこ感を出すヘルパー (頂点の裂けを防止)
function createLumpyLeavesGeometry(radius, detail) {
  const leafGeo = new THREE.IcosahedronGeometry(radius, detail);
  const leafPos = leafGeo.attributes.position;
  
  // 頂点を法線方向にノイズで少しデコボコに変形する
  for (let k = 0; k < leafPos.count; k++) {
    const vx = leafPos.getX(k);
    const vy = leafPos.getY(k);
    const vz = leafPos.getZ(k);
    
    const len = Math.sqrt(vx*vx + vy*vy + vz*vz);
    if (len === 0) continue;
    
    // 決定論的なノイズ（頂点位置に依存）で有機的な凸凹を作り、ポリゴンの隙間を防ぐ
    const noise = 1.0 + (Math.sin(vx * 3.2) * Math.cos(vy * 3.2) * 0.08)
                      + (Math.sin(vz * 2.5) * 0.04);
    
    leafPos.setX(k, vx * noise);
    leafPos.setY(k, vy * noise);
    leafPos.setZ(k, vz * noise);
  }
  leafGeo.computeVertexNormals();
  return leafGeo;
}

function createTree(type) {
  const group = new THREE.Group();
  let radius = 0.4;
  
  if (type === 'broadleaf') {
    // 1. 広葉樹タイプ (もこもこした木)
    const trunkHeight = 3.2 + Math.random() * 1.2;
    const trunkRadius = 0.26 + Math.random() * 0.12;
    radius = trunkRadius;
    
    // 曲がった幹を表現するため、2つのシリンダーを少し傾けて連結
    const baseTrunkHeight = trunkHeight * 0.6;
    const trunkGeo1 = new THREE.CylinderGeometry(trunkRadius * 0.8, trunkRadius, baseTrunkHeight, 6);
    trunkGeo1.translate(0, baseTrunkHeight / 2, 0);
    
    const trunkMat = new THREE.MeshStandardMaterial({
      color: 0x473024,
      roughness: 0.95,
      metalness: 0.02,
      flatShading: true
    });
    
    const trunk1 = new THREE.Mesh(trunkGeo1, trunkMat);
    trunk1.castShadow = true;
    trunk1.receiveShadow = true;
    group.add(trunk1);
    
    // 傾けた上の幹
    const topTrunkHeight = trunkHeight * 0.5;
    const trunkGeo2 = new THREE.CylinderGeometry(trunkRadius * 0.5, trunkRadius * 0.8, topTrunkHeight, 6);
    trunkGeo2.translate(0, topTrunkHeight / 2, 0);
    const trunk2 = new THREE.Mesh(trunkGeo2, trunkMat);
    trunk2.position.set(0, baseTrunkHeight - 0.05, 0);
    trunk2.rotation.z = (Math.random() - 0.5) * 0.25;
    trunk2.rotation.x = (Math.random() - 0.5) * 0.25;
    trunk2.castShadow = true;
    trunk2.receiveShadow = true;
    group.add(trunk2);
    
    // 葉 (Icosahedronをベースに変形したもこもこの葉)
    const leavesMat = new THREE.MeshStandardMaterial({
      color: 0x1d4a14, // 豊かな深い緑
      roughness: 0.9,
      metalness: 0.01,
      flatShading: true
    });
    
    const leafLayouts = [
      { r: 1.8, y: trunkHeight, scale: [1.1, 0.9, 1.1] },
      { r: 1.5, y: trunkHeight + 1.2, scale: [1.0, 0.85, 1.0] },
      { r: 1.1, y: trunkHeight + 2.2, scale: [0.85, 0.75, 0.85] }
    ];
    
    leafLayouts.forEach(layer => {
      const leafGeo = createLumpyLeavesGeometry(layer.r, 2);
      const leafMesh = new THREE.Mesh(leafGeo, leavesMat);
      leafMesh.position.set(
        (Math.random() - 0.5) * 0.3 + (trunk2.position.x + topTrunkHeight * Math.sin(trunk2.rotation.z)),
        layer.y,
        (Math.random() - 0.5) * 0.3
      );
      leafMesh.scale.set(layer.scale[0], layer.scale[1], layer.scale[2]);
      leafMesh.castShadow = true;
      leafMesh.receiveShadow = true;
      group.add(leafMesh);
    });
  } else {
    // 2. 針葉樹タイプ (コニファー、背の高い三角形の木)
    const trunkHeight = 4.2 + Math.random() * 1.8;
    const trunkRadius = 0.2 + Math.random() * 0.08;
    radius = trunkRadius;
    
    const trunkGeo = new THREE.CylinderGeometry(trunkRadius * 0.5, trunkRadius, trunkHeight, 5);
    trunkGeo.translate(0, trunkHeight / 2, 0);
    
    const trunkMat = new THREE.MeshStandardMaterial({
      color: 0x3d281e,
      roughness: 0.95,
      metalness: 0.02,
      flatShading: true
    });
    
    const trunk = new THREE.Mesh(trunkGeo, trunkMat);
    trunk.castShadow = true;
    trunk.receiveShadow = true;
    group.add(trunk);
    
    // 葉 (何段かの円錐を重ねて傘にする)
    const needleMat = new THREE.MeshStandardMaterial({
      color: 0x143b17, // 暗めの針葉樹グリーン
      roughness: 0.85,
      metalness: 0.02,
      flatShading: true
    });
    
    const steps = 4;
    const baseLeafY = trunkHeight * 0.35;
    const leafSpan = trunkHeight * 0.65;
    
    for (let s = 0; s < steps; s++) {
      const stepFactor = s / (steps - 1); 
      const leafRadius = 1.9 * (1.0 - stepFactor * 0.7);
      const leafHeight = 1.3 * (1.0 - stepFactor * 0.3);
      
      const coneGeo = new THREE.ConeGeometry(leafRadius, leafHeight, 5);
      coneGeo.translate(0, leafHeight / 2, 0);
      
      const coneMesh = new THREE.Mesh(coneGeo, needleMat);
      coneMesh.position.set(0, baseLeafY + stepFactor * leafSpan, 0);
      coneMesh.rotation.y = Math.random() * Math.PI;
      coneMesh.castShadow = true;
      coneMesh.receiveShadow = true;
      group.add(coneMesh);
    }
  }
  
  const scale = 0.8 + Math.random() * 0.4;
  group.scale.set(scale, scale, scale);
  
  return {
    group: group,
    radius: radius * scale * 1.8
  };
}

const treeCount = 45;
for (let i = 0; i < treeCount; i++) {
  let x, z;
  do {
    x = (Math.random() - 0.5) * (areaSize - 20);
    z = (Math.random() - 0.5) * (areaSize - 20);
    
    // 初期位置(0,0)および湖(lakeX, lakeZ)からの距離をチェック
    const distToCenter = Math.sqrt(x*x + z*z);
    const dxLake = x - lakeX;
    const dzLake = z - lakeZ;
    const distToLake = Math.sqrt(dxLake*dxLake + dzLake*dzLake);
    
    if (distToCenter >= 12 && distToLake >= lakeRadius + 2.5) {
      break;
    }
  } while (true);

  const y = getTerrainHeight(x, z);
  const type = Math.random() < 0.5 ? 'broadleaf' : 'conifer';
  const treeData = createTree(type);
  treeData.group.position.set(x, y - 0.1, z);
  treeGroup.add(treeData.group);
  
  treePositions.push({
    x: x,
    z: z,
    radius: treeData.radius + 0.5
  });
}
scene.add(treeGroup);

// --- 5.6. 湖 (Lake/Water) の作成 ---
const waterGeo = new THREE.RingGeometry(0, lakeRadius, 32);
const waterMat = new THREE.MeshStandardMaterial({
  color: 0x00c4ec, // 透明度の高い美しいシアン系ブルー
  emissive: 0x051d30, // ほのかな自発光で深みを出す
  roughness: 0.08,
  metalness: 0.35, // 反射を少し強めてキラキラさせる
  transparent: true,
  opacity: 0.48, // 透明度を少し上げ、底の砂利がより鮮明に見えるようにする
  flatShading: true,
  side: THREE.DoubleSide
});
const water = new THREE.Mesh(waterGeo, waterMat);
water.rotation.x = -Math.PI / 2;
water.position.set(lakeX, waterHeight, lakeZ);
water.receiveShadow = true;
scene.add(water);
waterMesh = water; // グローバル参照を設定

// --- 5.7. 岩 (Rocks) の生成と配置 ---
const rockGroup = new THREE.Group();
const rockPositions = []; // 衝突判定用

function createRock() {
  const radius = 0.8 + Math.random() * 1.6;
  const rockGeo = new THREE.DodecahedronGeometry(radius, 1);
  
  // 頂点ごとの位置に依存する数式（ノイズ）で変形し、ポリゴンの裂け（スカスカ感）を防ぐ
  const pos = rockGeo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const vx = pos.getX(i);
    const vy = pos.getY(i);
    const vz = pos.getZ(i);
    
    // 元の座標を元にした決定論的な関数で変形量を決定
    // これにより、同じ位置にある共有頂点が全く同じ変形を受け、裂け目を防止する
    const angle = Math.atan2(vz, vx);
    const heightFactor = vy / radius;
    
    // 一貫したデコボコ変形
    const deform = 1.0 + Math.sin(angle * 3.0) * Math.cos(heightFactor * 4.0) * 0.12
                       + Math.cos(angle * 5.0) * 0.05;
    
    // 岩の形状を少し平たく潰しつつ、デコボコを乗せる
    pos.setX(i, vx * deform * 1.15);
    pos.setY(i, vy * deform * 0.65); // 少し低く押しつぶす
    pos.setZ(i, vz * deform * 1.15);
  }
  rockGeo.computeVertexNormals();
  
  const rockMat = new THREE.MeshStandardMaterial({
    color: 0x718096, // 風化したローポリ岩のグレー
    roughness: 0.95,
    metalness: 0.03,
    flatShading: true
  });
  
  const mesh = new THREE.Mesh(rockGeo, rockMat);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.rotation.set(
    Math.random() * Math.PI,
    Math.random() * Math.PI,
    Math.random() * Math.PI
  );
  
  return {
    mesh: mesh,
    radius: radius * 0.95
  };
}

// 湖の周囲に12個、草原の他の場所に12個配置
const rockCount = 24;
for (let i = 0; i < rockCount; i++) {
  let x, z;
  if (i < 12) {
    // 湖の周囲（湖畔）に並べる
    const angle = (i / 12) * Math.PI * 2 + Math.random() * 0.4;
    const r = lakeRadius + 0.5 + Math.random() * 2.5;
    x = lakeX + Math.cos(angle) * r;
    z = lakeZ + Math.sin(angle) * r;
  } else {
    // 草原の他の場所にランダム配置
    do {
      x = (Math.random() - 0.5) * (areaSize - 20);
      z = (Math.random() - 0.5) * (areaSize - 20);
      const distToCenter = Math.sqrt(x*x + z*z);
      const dxLake = x - lakeX;
      const dzLake = z - lakeZ;
      const distToLake = Math.sqrt(dxLake*dxLake + dzLake*dzLake);
      
      if (distToCenter >= 10 && distToLake >= lakeRadius + 2) {
        break;
      }
    } while (true);
  }
  
  const y = getTerrainHeight(x, z);
  const rockData = createRock();
  rockData.mesh.position.set(x, y - 0.25, z); // 地面に少し埋め込む
  rockGroup.add(rockData.mesh);
  
  rockPositions.push({
    x: x,
    z: z,
    radius: rockData.radius + 0.4 // プレイヤー衝突半径を上乗せ
  });
}
scene.add(rockGroup);

// --- 5.8. 神秘的なモニュメント (Monument) の作成と配置 ---
const monumentGroup = new THREE.Group();
const monumentY = getTerrainHeight(monumentX, monumentZ);

// A. 土台
const baseGeo = new THREE.CylinderGeometry(3.5, 3.8, 0.8, 8);
const stoneMat = new THREE.MeshStandardMaterial({
  color: 0x718096, // 古びた石
  roughness: 0.95,
  metalness: 0.05,
  flatShading: true
});
const baseMesh = new THREE.Mesh(baseGeo, stoneMat);
baseMesh.position.set(0, 0.4, 0);
baseMesh.castShadow = true;
baseMesh.receiveShadow = true;
monumentGroup.add(baseMesh);

// B. 壊れた石柱を周囲に4本
const pillarLayouts = [
  { x: 2.2, z: 2.2, h: 2.5, rot: 0.1 },
  { x: -2.2, z: 2.2, h: 1.2, rot: -0.2 },
  { x: 2.2, z: -2.2, h: 0.8, rot: 0.3 },
  { x: -2.2, z: -2.2, h: 2.0, rot: 0.05 }
];

pillarLayouts.forEach(p => {
  const pGeo = new THREE.CylinderGeometry(0.35, 0.4, p.h, 6);
  pGeo.translate(0, p.h / 2, 0);
  const pMesh = new THREE.Mesh(pGeo, stoneMat);
  pMesh.position.set(p.x, 0.7, p.z);
  pMesh.rotation.z = p.rot;
  pMesh.rotation.x = p.rot * 0.5;
  pMesh.castShadow = true;
  pMesh.receiveShadow = true;
  monumentGroup.add(pMesh);
});

// C. 中心に浮かぶ光る結晶 (Crystal)
const crystalGeo = new THREE.OctahedronGeometry(0.7, 0);
const crystalMat = new THREE.MeshBasicMaterial({
  color: 0x63b3ed, // 美しいライトブルーに光る
});
const crystalMesh = new THREE.Mesh(crystalGeo, crystalMat);
crystalMesh.position.set(0, 2.5, 0);
monumentGroup.add(crystalMesh);
monumentCrystal = crystalMesh; // グローバル参照を設定してアニメーションループから回す

// D. 結晶の放つ淡いポイントライト
const monumentLight = new THREE.PointLight(0x63b3ed, 3.5, 12);
monumentLight.position.set(0, 2.5, 0);
monumentLight.castShadow = true;
monumentGroup.add(monumentLight);

monumentGroup.position.set(monumentX, monumentY, monumentZ);
scene.add(monumentGroup);

// --- 6. 空 (Sky) と太陽の設定 ---
const sky = new Sky();
sky.scale.setScalar(450000);
scene.add(sky);

const sun = new THREE.Vector3();
const skyUniforms = sky.material.uniforms;
skyUniforms['turbidity'].value = 2.0;       // 空の透明度（低くして澄んだ青空にする）
skyUniforms['rayleigh'].value = 1.8;        // 大気散乱（標準的な青空）
skyUniforms['mieCoefficient'].value = 0.005; // 塵の散乱
skyUniforms['mieDirectionalG'].value = 0.8;  // 太陽の周りの光のにじみ

// 太陽の角度 (昼間の高く昇った太陽)
const elevation = 48.0;  // 太陽の高度（高く昇らせる）
const azimuth = 195;    // 方位角

const phi = THREE.MathUtils.degToRad(90 - elevation);
const theta = THREE.MathUtils.degToRad(azimuth);
sun.setFromSphericalCoords(1, phi, theta);
skyUniforms['sunPosition'].value.copy(sun);

// --- 7. ライティング ---
// 太陽のメイン光 (明るく白い昼間の自然光)
const sunLight = new THREE.DirectionalLight(0xfffaed, 1.6);
sunLight.position.copy(sun).multiplyScalar(150);
sunLight.castShadow = true;
// シャドウマップの最適化
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 400;
const d = 60;
sunLight.shadow.camera.left = -d;
sunLight.shadow.camera.right = d;
sunLight.shadow.camera.top = d;
sunLight.shadow.camera.bottom = -d;
sunLight.shadow.bias = -0.0005; // シャドウアクネの防止
scene.add(sunLight);

// 環境光 (青空の反射光をシミュレートする薄い青色の光)
const ambientLight = new THREE.AmbientLight(0xdbe9ff, 0.7);
scene.add(ambientLight);

// --- 8. UI とオーディオ連携 ---
document.addEventListener('DOMContentLoaded', () => {
  const soundToggleBtn = document.getElementById('sound-toggle-btn');
  if (soundToggleBtn) {
    soundToggleBtn.addEventListener('click', (e) => {
      e.stopPropagation(); // ポインターロックが誤作動しないようにクリックの伝播を防止
      toggleBGM();
    });
  }
});

// --- 9. アニメーション・ループ ---
const moveSpeed = 8.0; // 歩く速度 (m/s)
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();

function animate() {
  requestAnimationFrame(animate);

  const delta = clock.getDelta();
  const time = clock.getElapsedTime();

  // 草のシェーダーに経過時間を送って揺らす
  if (grassMaterial.userData.shader) {
    grassMaterial.userData.shader.uniforms.uTime.value = time;
  }

  // モニュメントの結晶をアニメーション (回転と上下浮遊)
  if (monumentCrystal) {
    monumentCrystal.rotation.y += 1.0 * delta;
    monumentCrystal.rotation.x += 0.5 * delta;
    monumentCrystal.position.y = 2.5 + Math.sin(time * 1.5) * 0.18;
  }

  // プレイヤーの移動処理
  if (controls && controls.isLocked) {
    // 前後・左右の入力方向の算出
    direction.z = Number(keys.w) - Number(keys.s);
    direction.x = Number(keys.d) - Number(keys.a);
    direction.normalize(); // 斜め移動でスピードが上がらないように

    // カメラの向いている向きに基づく移動ベクトルの計算
    const camDir = new THREE.Vector3();
    camera.getWorldDirection(camDir);
    camDir.y = 0; // 上下移動は無視
    camDir.normalize();

    const camRight = new THREE.Vector3();
    camRight.crossVectors(camDir, camera.up).normalize();

    velocity.set(0, 0, 0);
    if (keys.w || keys.s) velocity.addScaledVector(camDir, direction.z * moveSpeed * delta);
    if (keys.a || keys.d) velocity.addScaledVector(camRight, direction.x * moveSpeed * delta);

    // カメラ位置の更新 (水平移動のみ適用)
    camera.position.add(velocity);

    // エリア境界の制限 (150m四方の外に出られないようにする壁)
    const maxBound = areaSize / 2 - 2;
    camera.position.x = Math.max(-maxBound, Math.min(maxBound, camera.position.x));
    camera.position.z = Math.max(-maxBound, Math.min(maxBound, camera.position.z));

    // 木との衝突判定 (押し戻し)
    const px = camera.position.x;
    const pz = camera.position.z;
    for (let i = 0; i < treePositions.length; i++) {
      const tree = treePositions[i];
      const dx = px - tree.x;
      const dz = pz - tree.z;
      const dist = Math.sqrt(dx * dx + dz * dz);
      if (dist < tree.radius) {
        const overlap = tree.radius - dist;
        camera.position.x += (dx / dist) * overlap;
        camera.position.z += (dz / dist) * overlap;
      }
    }

    // 岩との衝突判定 (押し戻し)
    for (let i = 0; i < rockPositions.length; i++) {
      const rock = rockPositions[i];
      const dx = px - rock.x;
      const dz = pz - rock.z;
      const dist = Math.sqrt(dx * dx + dz * dz);
      if (dist < rock.radius) {
        const overlap = rock.radius - dist;
        camera.position.x += (dx / dist) * overlap;
        camera.position.z += (dz / dist) * overlap;
      }
    }

    // モニュメントとの衝突判定 (押し戻し)
    const dxMon = px - monumentX;
    const dzMon = pz - monumentZ;
    const distMon = Math.sqrt(dxMon * dxMon + dzMon * dzMon);
    if (distMon < monumentRadius) {
      const overlap = monumentRadius - distMon;
      camera.position.x += (dxMon / distMon) * overlap;
      camera.position.z += (dzMon / distMon) * overlap;
    }

    // 湖に入った時の判定
    const dxLake = px - lakeX;
    const dzLake = pz - lakeZ;
    const distToLake = Math.sqrt(dxLake*dxLake + dzLake*dzLake);
    const swimHeight = waterHeight + 1.6; // 少し体が沈んで浮いている状態の目線
    const inLake = distToLake < lakeRadius - 1.5;

    // 移動先の地形の高さを取得
    const terrainHeight = getTerrainHeight(camera.position.x, camera.position.z);
    const targetHeight = terrainHeight + 1.8; // 目線の基本高さ
    
    // プレイヤーの目標とする高さ (湖にいれば水面、陸地なら地面)
    const activeTargetHeight = inLake ? swimHeight : targetHeight;

    // 接地（または水面浮遊）判定とジャンプ物理
    if (camera.position.y <= activeTargetHeight + 0.02) {
      isGrounded = true;
      velocityY = 0;
      
      // なめらかに目標高度に追従する
      camera.position.y += (activeTargetHeight - camera.position.y) * 0.12;
    } else {
      isGrounded = false;
    }

    // ジャンプ開始
    if (keys.space && isGrounded) {
      velocityY = jumpStrength;
      isGrounded = false;
    }

    // 空中（または水面上空）での重力適用
    if (!isGrounded) {
      velocityY -= gravity * delta;
      camera.position.y += velocityY * delta;

      // 着地（または水面への着水）判定
      if (camera.position.y < activeTargetHeight) {
        camera.position.y = activeTargetHeight;
        velocityY = 0;
        isGrounded = true;
      }
    }
  }

  // 湖の水面をゆらゆらと波立たせる (さざ波表現)
  if (waterMesh) {
    waterMesh.rotation.z = time * 0.02;
    waterMesh.position.y = waterHeight + Math.sin(time * 1.5) * 0.025;
  }

  renderer.render(scene, camera);
}

// 起動
animate();

// リサイズ対応
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
