import os
import sys
from src.core.screen_finder import find_image_center
from src.core.mouse_controller import move_mouse_to

def main(image_path: str) -> int:
    if not os.path.isfile(image_path):
        print(f"Imagem não encontrada: {image_path}")
        return 1
    print(f"Procurando imagem na tela: {image_path}")
    center = find_image_center(image_path, tolerance=0.7)
    if center is None:
        print("Imagem não encontrada na tela. Tente:")
        print("- Aumentar tolerance (ex.: 0.2)")
        print("- Recapturar a imagem com AutoPy")
        return 2
    print(f"Imagem encontrada no ponto: {center}")
    move_mouse_to(center)
    print("Mouse movido até o centro da imagem")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m scripts.find_and_move caminho/para/imagem.png")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
