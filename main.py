import logging.config
import time
from pathlib import Path
from typing import Any

import cv2
import mss
import pyautogui
from mss.base import MSSBase

from automation_utils import AutomationUtils
from image_not_found import ImageNotFound

ARQUIVOS_SALVOS = cv2.imread(str(Path(__file__).parent / 'assets' / 'Arquivos salvos.jpeg'), 0)
LOCAL_DO_SALVAMENTO = cv2.imread(str(Path(__file__).parent / 'assets' / 'Local do Salvamento.jpeg'), 0)
MENU = cv2.imread(str(Path(__file__).parent / 'assets' / 'Menu.jpeg'))
NADA_CONSTA = cv2.imread(str(Path(__file__).parent / 'assets' / 'Nada consta.jpeg'), 0)
PASTA_JURIDICA = cv2.imread(str(Path(__file__).parent / 'assets' / 'PJ.jpeg'), 0)
SALVAR_EM_DISCO = cv2.imread(str(Path(__file__).parent / 'assets' / 'Salvar em Disco.jpeg'), 0)
SUMARIO = cv2.imread(str(Path(__file__).parent / 'assets' / 'Sumário.jpeg'), 0)
VOLTAR = cv2.imread(str(Path(__file__).parent / 'assets' / 'Voltar.jpeg'))

ULTIMO_VALOR_DE_PJ = 4500
TENTATIVAS_DE_LOCALIZAR = 3
INTERVALO_ENTRE_TENTATIVAS = 5

LOG = logging.getLogger('migracao')
pyautogui.PAUSE = 0.5


def setup_logging() -> None:
    logging_config = Path(__file__).parent / 'config' / 'logging.ini'
    if logging_config.exists():
        logging_dir = Path(__file__).parent / 'logs'
        logging_dir.mkdir(exist_ok=True)
        logging.config.fileConfig(
            logging_config,
            disable_existing_loggers=False,
            encoding='utf-8'
        )
    else:
        logging.basicConfig(level=logging.INFO)


def locate_on_screen(image: cv2.typing.MatLike, screen: MSSBase) -> tuple[int, int, Any, Any]:
    for attempt in range(1, TENTATIVAS_DE_LOCALIZAR + 1):
        found_coord = AutomationUtils.find_template(image, screen)
        if found_coord is not None:
            return found_coord
        if attempt < TENTATIVAS_DE_LOCALIZAR:
            logging.debug(f'Imagem NÃO Encontrada: aguardando {INTERVALO_ENTRE_TENTATIVAS} segundos.')
            time.sleep(INTERVALO_ENTRE_TENTATIVAS)
    raise ImageNotFound('A Imagem Solicitada NÃO foi Encontrada!')


def main(contador_de_pj: int, busca_sequencial: bool) -> None:
    default_screen = mss.mss()
    nao_encontradas = []
    try:
        while True:
            if busca_sequencial and contador_de_pj > ULTIMO_VALOR_DE_PJ:
                logging.debug(f'Pastas Jurídias NÃO Encontradas: {nao_encontradas}')
                logging.info('Encerrando as Exportações com SUCESSO!')
                break
            logging.info(f'Iniciando o Processo de Exportação para a Pasta Jurídica: {contador_de_pj}')
            x, y, w, h = locate_on_screen(PASTA_JURIDICA, default_screen)
            AutomationUtils.move_mouse_to((x + w, y, 100, h))
            pyautogui.click()
            pyautogui.typewrite(str(contador_de_pj))
            pyautogui.press('enter')
            try:
                locate_on_screen(NADA_CONSTA, default_screen)
                logging.info(f'A Pasta Jurídica {contador_de_pj} NÃO foi Encontrada!')
                if busca_sequencial:
                    nao_encontradas.append(contador_de_pj)
                    contador_de_pj += 1
                    continue
                contador_de_pj = nao_encontradas.pop()
                pyautogui.press('enter')
            except ImageNotFound:
                pass
            pyautogui.press('enter')
            locate_on_screen(MENU, default_screen)
            pyautogui.click()
            found_coord = locate_on_screen(SUMARIO, default_screen)
            AutomationUtils.move_mouse_to(found_coord)
            found_coord = locate_on_screen(SALVAR_EM_DISCO, default_screen)
            AutomationUtils.move_mouse_to(found_coord)
            pyautogui.click()
            found_coord = locate_on_screen(LOCAL_DO_SALVAMENTO, default_screen)
            AutomationUtils.move_mouse_to(found_coord)
            pyautogui.click()
            pyautogui.press('enter')
            logging.info(f'A Pasta Jurídica {contador_de_pj} foi Exportada com SUCESSO!')
            found_coord = locate_on_screen(VOLTAR, default_screen)
            AutomationUtils.move_mouse_to(found_coord)
            pyautogui.click()
            if busca_sequencial:
                contador_de_pj += 1
                continue
            contador_de_pj = nao_encontradas.pop()
    except IndexError:
        logging.debug(f'Pastas Jurídias NÃO Encontradas: {nao_encontradas}')
        logging.info('Todas as Pastas Jurídicas Informadas foram PROCESSADAS!')
    except (ImageNotFound, cv2.error):
        logging.info('Houve um Problema durante o Fluxo de Exportação!')
    except KeyboardInterrupt:
        logging.debug(f'Pastas Jurídias NÃO Encontradas: {nao_encontradas}')
        logging.info('Encerrando as Exportações com SUCESSO!')


if __name__ == '__main__':
    setup_logging()
    main(1, True)
