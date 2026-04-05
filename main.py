import logging.config
import time
from pathlib import Path

import cv2
import mss
import pyautogui
from mss.base import MSSBase

from automation_utils import AutomationUtils
from image_not_found import ImageNotFound

ENTER = 'enter'
ASSETS = 'assets'

ARQUIVOS_SALVOS = cv2.imread(str(Path(__file__).parent / ASSETS / 'Arquivos Salvos.png'), 0)
LOCAL_DO_SALVAMENTO = cv2.imread(str(Path(__file__).parent / ASSETS / 'Local do Salvamento.png'), 0)
MENU = cv2.imread(str(Path(__file__).parent / ASSETS / 'Menu.png'), 0)
NADA_CONSTA = cv2.imread(str(Path(__file__).parent / ASSETS / 'Nada Consta.png'), 0)
PASTA_JURIDICA = cv2.imread(str(Path(__file__).parent / ASSETS / 'PJ.png'), 0)
SALVAR_EM_DISCO = cv2.imread(str(Path(__file__).parent / ASSETS / 'Salvar em Disco.png'), 0)
SUMARIO = cv2.imread(str(Path(__file__).parent / ASSETS / 'Sumário.png'), 0)
VOLTAR = cv2.imread(str(Path(__file__).parent / ASSETS / 'Voltar.png'), 0)

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


def locate_on_screen(image: cv2.typing.MatLike, screen: MSSBase) -> tuple[float, float, float, float]:
    for attempt in range(1, TENTATIVAS_DE_LOCALIZAR + 1):
        found_coord = AutomationUtils.find_template(image, screen)
        if found_coord is not None:
            return found_coord
        if attempt < TENTATIVAS_DE_LOCALIZAR:
            LOG.debug(f'Imagem NÃO Encontrada: aguardando {INTERVALO_ENTRE_TENTATIVAS} segundos.')
            time.sleep(INTERVALO_ENTRE_TENTATIVAS)
    raise ImageNotFound('A Imagem Solicitada NÃO foi Encontrada!')


def send_hotkey() -> None:
    try:
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
    finally:
        pyautogui.keyUp('ctrl')


def main(contador_de_pj: int, busca_sequencial: bool, busca_nao_sequencial: list[int]) -> None:
    nao_encontradas = []
    with mss.mss() as default_screen:
        try:
            while True:
                if busca_sequencial and contador_de_pj > ULTIMO_VALOR_DE_PJ:
                    LOG.debug(f'Pastas Jurídias NÃO Encontradas: {nao_encontradas}')
                    LOG.info('Encerrando as Exportações com SUCESSO!')
                    break
                LOG.info(f'Iniciando o Processo de Exportação para a Pasta Jurídica: {contador_de_pj}')
                x, y, w, h = locate_on_screen(PASTA_JURIDICA, default_screen)
                mouse_coord = AutomationUtils.move_mouse_to((x + w, y, 100.0, h))
                pyautogui.click(mouse_coord)
                send_hotkey()
                pyautogui.typewrite(str(contador_de_pj))
                pyautogui.press(ENTER)
                try:
                    locate_on_screen(NADA_CONSTA, default_screen)
                    LOG.info(f'A Pasta Jurídica {contador_de_pj} NÃO foi Encontrada!')
                    nao_encontradas.append(contador_de_pj)
                    pyautogui.press(ENTER)
                    if busca_sequencial:
                        contador_de_pj += 1
                    else:
                        contador_de_pj = busca_nao_sequencial.pop()
                    continue
                except ImageNotFound:
                    pyautogui.press(ENTER)
                found_coord = locate_on_screen(MENU, default_screen)
                mouse_coord = AutomationUtils.move_mouse_to(found_coord)
                pyautogui.click(mouse_coord)
                found_coord = locate_on_screen(SUMARIO, default_screen)
                AutomationUtils.move_mouse_to(found_coord)
                found_coord = locate_on_screen(SALVAR_EM_DISCO, default_screen)
                mouse_coord = AutomationUtils.move_mouse_to(found_coord)
                pyautogui.click(mouse_coord)
                found_coord = locate_on_screen(LOCAL_DO_SALVAMENTO, default_screen)
                mouse_coord = AutomationUtils.move_mouse_to(found_coord)
                pyautogui.click(mouse_coord)
                pyautogui.press(ENTER)
                locate_on_screen(ARQUIVOS_SALVOS, default_screen)
                pyautogui.press(ENTER)
                LOG.info(f'A Pasta Jurídica {contador_de_pj} foi Exportada com SUCESSO!')
                found_coord = locate_on_screen(VOLTAR, default_screen)
                mouse_coord = AutomationUtils.move_mouse_to(found_coord)
                pyautogui.click(mouse_coord)
                if busca_sequencial:
                    contador_de_pj += 1
                else:
                    contador_de_pj = busca_nao_sequencial.pop()
        except IndexError:
            LOG.debug(f'Pastas Jurídias NÃO Encontradas: {nao_encontradas}')
            LOG.info('Todas as Pastas Jurídicas Informadas foram PROCESSADAS!')
        except (ImageNotFound, cv2.error) as error:
            LOG.info('Houve um Problema durante o Fluxo de Exportação!')
            LOG.debug(error)
        except KeyboardInterrupt:
            LOG.debug(f'Pastas Jurídias NÃO Encontradas: {nao_encontradas}')
            LOG.info('Encerrando as Exportações com SUCESSO!')


if __name__ == '__main__':
    setup_logging()
    time.sleep(INTERVALO_ENTRE_TENTATIVAS)
    main(1, True, [1, 2, 3, 4, 5])
