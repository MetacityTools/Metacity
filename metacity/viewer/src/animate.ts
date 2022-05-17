import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { WebGLRenderer } from 'three/src/renderers/WebGLRenderer';
import { PerspectiveCamera } from 'three/src/cameras/PerspectiveCamera';
import { Scene } from 'three/src/scenes/Scene';
import { Mesh } from 'three/src/objects/Mesh';
import { MeshBasicMaterial } from 'three/src/materials/MeshBasicMaterial';
import { BoxGeometry } from 'three/src/geometries/BoxGeometry';



export function run() {
    let scene = new Scene();
    let camera = new PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    let renderer = new WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    let geometry = new BoxGeometry(1, 1, 1);
    let material = new MeshBasicMaterial({ color: 0x00ff00 });
    let cube = new Mesh(geometry, material);
    scene.add(cube);
    camera.position.z = 5;
    let controls = new OrbitControls(camera, renderer.domElement);
    controls.update();
    
    let animate = function () {
        requestAnimationFrame(animate);
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
        renderer.render(scene, camera);
    }
    animate();
}