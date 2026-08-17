import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

const canvas = document.getElementById("hero-canvas");
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 0, 9);

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);

const particleCount = 420;
const positions = new Float32Array(particleCount * 3);
const basePositions = new Float32Array(particleCount * 3);
const phases = new Float32Array(particleCount);

for (let i = 0; i < particleCount; i++) {
  const radius = 3.4 + Math.random() * 2.6;
  const theta = Math.random() * Math.PI * 2;
  const phi = Math.acos(2 * Math.random() - 1);
  const x = radius * Math.sin(phi) * Math.cos(theta);
  const y = radius * Math.sin(phi) * Math.sin(theta) * 0.6;
  const z = radius * Math.cos(phi) * 0.6;
  positions.set([x, y, z], i * 3);
  basePositions.set([x, y, z], i * 3);
  phases[i] = Math.random() * Math.PI * 2;
}

const geometry = new THREE.BufferGeometry();
geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

const material = new THREE.PointsMaterial({
  size: 0.055,
  color: 0xf97316,
  transparent: true,
  opacity: 0.85,
});
const points = new THREE.Points(geometry, material);
scene.add(points);

const linkGeometry = new THREE.BufferGeometry();
const linkMaterial = new THREE.LineBasicMaterial({ color: 0x2563eb, transparent: true, opacity: 0.18 });
const maxLinks = 260;
const linkPositions = new Float32Array(maxLinks * 2 * 3);
linkGeometry.setAttribute("position", new THREE.BufferAttribute(linkPositions, 3));
const lines = new THREE.LineSegments(linkGeometry, linkMaterial);
scene.add(lines);

function rebuildLinks() {
  let count = 0;
  for (let i = 0; i < particleCount && count < maxLinks; i += 3) {
    const j = (i + 17 + Math.floor(Math.random() * 40)) % particleCount;
    const ax = positions[i * 3], ay = positions[i * 3 + 1], az = positions[i * 3 + 2];
    const bx = positions[j * 3], by = positions[j * 3 + 1], bz = positions[j * 3 + 2];
    const dist = Math.hypot(ax - bx, ay - by, az - bz);
    if (dist < 2.4) {
      linkPositions.set([ax, ay, az, bx, by, bz], count * 6);
      count++;
    }
  }
  linkGeometry.setDrawRange(0, count * 2);
  linkGeometry.attributes.position.needsUpdate = true;
}

const clock = new THREE.Clock();

function animate() {
  const t = clock.getElapsedTime();
  const pulse = 1 + 0.06 * Math.sin(t * 1.6) + 0.03 * Math.sin(t * 3.1);

  for (let i = 0; i < particleCount; i++) {
    const bx = basePositions[i * 3];
    const by = basePositions[i * 3 + 1];
    const bz = basePositions[i * 3 + 2];
    const wobble = 0.12 * Math.sin(t * 0.8 + phases[i]);
    positions[i * 3] = bx * pulse + wobble;
    positions[i * 3 + 1] = by * pulse + wobble * 0.6;
    positions[i * 3 + 2] = bz * pulse;
  }
  geometry.attributes.position.needsUpdate = true;

  points.rotation.y = t * 0.09;
  lines.rotation.y = t * 0.09;
  points.rotation.x = Math.sin(t * 0.15) * 0.08;
  lines.rotation.x = points.rotation.x;

  if (Math.floor(t * 4) % 6 === 0) rebuildLinks();

  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

rebuildLinks();
animate();

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
