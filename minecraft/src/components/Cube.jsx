import { useBox } from "@react-three/cannon";
import * as textures from "../assets/textures";

export const Cube = ({ position, texture }) => {
  const [ref] = useBox(() => ({
    type: "Static",
    position,
  }));

  const activeTexture = textures[texture + "Texture"];

  return (
    <mesh ref={ref}>
      <boxGeometry attach="geometry" />
      <meshStandardMaterial attach="material" map={activeTexture} />
    </mesh>
  );
};
