import { FC, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { MeshDistortMaterial, Sphere, Environment } from '@react-three/drei';
import * as THREE from 'three';
import { useSpring, animated } from '@react-spring/three';

/** The morphing organic sphere — single continuous form, not a service icon */
const OrganicForm: FC = () => {
  const meshRef = useRef<THREE.Mesh>(null);

  // Subtle auto-rotate
  useFrame((_, delta) => {
    if (!meshRef.current) return;
    meshRef.current.rotation.y += delta * 0.18;
    meshRef.current.rotation.x += delta * 0.04;
  });

  // Spring-in on mount: scale 0 → 1
  const { scale } = useSpring({
    from: { scale: 0 },
    to: { scale: 1 },
    config: { mass: 2, tension: 120, friction: 26 },
    delay: 200,
  });

  return (
    <animated.mesh ref={meshRef} scale={scale as unknown as THREE.Vector3}>
      <Sphere args={[1.45, 128, 128]}>
        <MeshDistortMaterial
          color="#3A6B40"
          distort={0.52}
          speed={2.0}
          roughness={0.12}
          metalness={0.04}
          envMapIntensity={0.5}
        />
      </Sphere>
    </animated.mesh>
  );
};

export const OrganicHero3D: FC = () => {
  return (
    <Canvas
      dpr={[1, 1.5]}
      camera={{ position: [0, 0, 4.2], fov: 42 }}
      style={{ width: '100%', height: '100%', background: 'transparent' }}
      gl={{ alpha: true, antialias: true }}
    >
      {/* Warm ivory key light */}
      <ambientLight intensity={0.55} color="#F5F0E8" />
      <directionalLight
        position={[3, 5, 2]}
        intensity={1.4}
        color="#FAF7F0"
      />
      {/* Sage fill light */}
      <pointLight
        position={[-3, -2, 2]}
        intensity={0.6}
        color="#7A9E6E"
      />
      {/* Warm rim */}
      <pointLight
        position={[2, -3, -2]}
        intensity={0.3}
        color="#C9A15A"
      />

      <Environment preset="forest" />

      <OrganicForm />
    </Canvas>
  );
};
