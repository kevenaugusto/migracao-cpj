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


# TODO: Executar para as PJs que Estão ATIVAS
# TODO: Armazenar os Valores NÃO ENCONTRADOS
# TODO: Executar para os Valores NÃO ENCONTRADOS nas PJs que Estão INATIVAS
# TODO: Armazenar os Valores NÃO ENCONTRADOS


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
            # TODO: Verificar se BUSCA_SEQUENCIAL e CONTADOR_DE_PJ Maior do Que ULTIMO_VALOR_DE_PJ
            if busca_sequencial and contador_de_pj > ULTIMO_VALOR_DE_PJ:
                logging.debug(f'Pastas Jurídias NÃO Encontradas: {nao_encontradas}')
                # TODO: Logging de Encerramento da Execução
                logging.info('Encerrando as Exportações com SUCESSO!')
                # TODO: Encerrar o Looping de Execução
                break
            # TODO: Logging de Inicialização do Processo
            logging.info(f'Iniciando o Processo de Exportação para a Pasta Jurídica: {contador_de_pj}')
            # TODO: Localizar o Campo PJ e Clicar à DIRETA da Imagens (Quantidade de Pixels a Definir)
            found_coord = locate_on_screen(PASTA_JURIDICA, default_screen)
            AutomationUtils.move_mouse_to(found_coord) # TODO: Somar a Quantidade de Pixels Definida
            pyautogui.click()
            # TODO: Digitar o Número ATUAL do Contador de PJs e Digitar ENTER
            pyautogui.typewrite(str(contador_de_pj))
            pyautogui.press('enter')
            # TODO: Verificar se NADA CONSTA
            try:
                locate_on_screen(NADA_CONSTA, default_screen)
                # TODO: Logging com a Informação de que NADA CONSTA
                logging.info(f'A Pasta Jurídica {contador_de_pj} NÃO foi Encontrada!')
                # TODO: Verificar se BUSCA_SEQUENCIAL
                if busca_sequencial:
                    # TODO: Adição de Valor da PJ em NAO_ENCONTRADAS
                    nao_encontradas.append(contador_de_pj)
                    # TODO: Incrementar o CONTADOR_DE_PJ e Reiniciar o Fluxo
                    contador_de_pj += 1
                    continue
                # TODO: Atribuir ao CONTADOR_DE_PJ o Próximo Valor de NAO_ENCONTRADAS e Reiniciar o Fluxo
                contador_de_pj = nao_encontradas.pop()
                pyautogui.press('enter') # Para Fechar o Pop-up de NADA CONSTA
            except ImageNotFound:
                pass
            # TODO: Digitar ENTER para Abrir a PJ (Validar a Funcionalidade)
            pyautogui.press('enter')
            # TODO: Localizar e Clicar no Menu na Extremidade Direita do CPJ
            locate_on_screen(MENU, default_screen)
            pyautogui.click()
            # TODO: Localizar e Mover o Mouse até a Opção de Sumário
            found_coord = locate_on_screen(SUMARIO, default_screen)
            AutomationUtils.move_mouse_to(found_coord)
            # TODO: Localizar e Clicar na Opção de SALVAR EM DISCO
            found_coord = locate_on_screen(SALVAR_EM_DISCO, default_screen)
            AutomationUtils.move_mouse_to(found_coord)
            pyautogui.click()
            # TODO: Localizar e Clicar no LOCAL DE SALVAMENTO
            found_coord = locate_on_screen(LOCAL_DO_SALVAMENTO, default_screen)
            AutomationUtils.move_mouse_to(found_coord)
            pyautogui.click()
            # TODO: Digitar ENTER para Efetuar o Salvamento (Validar a Funcionalidade)
            pyautogui.press('enter')
            # TODO: Logging de Salvamento com Sucesso
            logging.info(f'A Pasta Jurídica {contador_de_pj} foi Exportada com SUCESSO!')
            # TODO: Localizar e Clicar no Botão de VOLTAR
            found_coord = locate_on_screen(VOLTAR, default_screen)
            AutomationUtils.move_mouse_to(found_coord)
            pyautogui.click()
            # TODO: Verificar se BUSCA_SEQUENCIAL
            if busca_sequencial:
                # TODO: Incrementar o CONTADOR_DE_PJ e Reiniciar o Fluxo
                contador_de_pj += 1
                continue
            # TODO: Atribuir ao CONTADOR_DE_PJ o Próximo Valor de NAO_ENCONTRADAS
            contador_de_pj = nao_encontradas.pop()
    except IndexError:
        logging.debug(f'Pastas Jurídias NÃO Encontradas: {nao_encontradas}')
        # TODO: Logging de Encerramento de Fluxo
        logging.info('Todas as Pastas Jurídicas Informadas foram PROCESSADAS!')
    except ImageNotFound:
        # TODO: Loggin de Encerramento de Fluxo
        logging.info('Houve um Problema durante o Fluxo de Exportação!')


if __name__ == '__main__':
    setup_logging()
    main(1, True)
