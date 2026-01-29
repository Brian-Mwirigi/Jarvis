'use client';

import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Torus, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';

function ReactorRing({ radius, speed, color, rotateX = 0, rotateY = 0 }: any) {
    const ref = useRef<THREE.Group>(null);

    useFrame((state) => {
        if (ref.current) {
            ref.current.rotation.z += speed * 0.01;
            ref.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.5) * 0.2 + rotateX;
            ref.current.rotation.y = Math.cos(state.clock.elapsedTime * 0.5) * 0.2 + rotateY;
        }
    });

    return (
        <group ref={ref}>
            <Torus args={[radius, 0.05, 16, 100]} rotation={[Math.PI / 2, 0, 0]}>
                <meshStandardMaterial color={color} emissive={color} emissiveIntensity={2} toneMapped={false} />
            </Torus>
        </group>
    );
}

function Core() {
    const ref = useRef<THREE.Mesh>(null);

    useFrame((state) => {
        if (ref.current) {
            const t = state.clock.getElapsedTime();
            ref.current.scale.setScalar(1 + Math.sin(t * 2) * 0.1);
        }
    });

    return (
        <Sphere ref={ref} args={[0.8, 64, 64]}>
            <MeshDistortMaterial
                color="#00f3ff"
                emissive="#00f3ff"
                emissiveIntensity={2}
                distort={0.4}
                speed={2}
                toneMapped={false}
            />
        </Sphere>
    );
}

function Particles({ count = 100 }) {
    const points = useRef<THREE.Points>(null);

    useFrame((state) => {
        if (points.current) {
            points.current.rotation.y = state.clock.elapsedTime * 0.05;
        }
    });

    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
        const r = 4 + Math.random() * 4;
        const theta = Math.random() * Math.PI * 2;
        const phi = (Math.random() - 0.5) * Math.PI;

        positions[i * 3] = r * Math.cos(theta) * Math.cos(phi);
        positions[i * 3 + 1] = r * Math.sin(phi);
        positions[i * 3 + 2] = r * Math.sin(theta) * Math.cos(phi);
    }

    return (
        <points ref={points}>
            <bufferGeometry>
                <bufferAttribute
                    attach="attributes-position"
                    count={count}
                    array={positions}
                    itemSize={3}
                />
            </bufferGeometry>
            <pointsMaterial
                size={0.05}
                color="#00f3ff"
                transparent
                opacity={0.6}
                sizeAttenuation
            />
        </points>
    );
}

export default function ArcReactor() {
    return (
        <div className="w-full h-full absolute inset-0 -z-10">
            <Canvas camera={{ position: [0, 0, 8] }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} />
                <pointLight position={[-10, -10, -10]} color="#00f3ff" intensity={2} />

                <Core />
                <ReactorRing radius={1.5} speed={2} color="#00f3ff" />
                <ReactorRing radius={1.8} speed={-1.5} color="#0066ff" rotateX={0.5} />
                <ReactorRing radius={2.1} speed={1} color="#00f3ff" rotateY={0.5} />

                <Particles />

                <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
            </Canvas>
        </div>
    );
}
