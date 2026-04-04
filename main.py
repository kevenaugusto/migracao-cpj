import logging.config
import time
from pathlib import Path
from typing import Any

import cv2
import mss
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

NAO_ENCONTRADAS = []
BUSCA_SEQUENCIAL = True
CONTADOR_DE_PJ = 1
ULTIMO_VALOR_DE_PJ = 4500
TENTATIVAS_DE_LOCALIZAR = 3
INTERVALO_ENTRE_TENTATIVAS = 5

LOG = logging.getLogger('migracao')


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


def locate_on_screen(image: cv2.typing.MatLike, screen: MSSBase) -> tuple[int, int, Any, Any] | None:
    for attempt in range(1, TENTATIVAS_DE_LOCALIZAR + 1):
        found_coord = AutomationUtils.find_template(image, screen)
        if found_coord is not None:
            return found_coord
        if attempt < TENTATIVAS_DE_LOCALIZAR:
            logging.debug(f'Imagem NÃO Encontrada: aguardando {INTERVALO_ENTRE_TENTATIVAS} segundos.')
            time.sleep(INTERVALO_ENTRE_TENTATIVAS)
    raise ImageNotFound('A Imagem Solicitada NÃO foi Encontrada!')


def main() -> None:
    default_screen = mss.mss()
    try:
        while True:
            # TODO: Verificar se BUSCA_SEQUENCIAL e CONTADOR_DE_PJ Maior do Que ULTIMO_VALOR_DE_PJ
                # TODO: Logging de Encerramento da Execução
                # TODO: Encerrar o Looping de Execução
            # TODO: Logging de Inicialização do Processo
            # TODO: Localizar o Campo PJ e Clicar à DIRETA da Imagens (Quantidade de Pixels a Definir)
            # TODO: Digitar o Número ATUAL do Contador de PJs e Digitar ENTER
            # TODO: Verificar se NADA CONSTA
                # TODO: Logging com a Informação de que NADA CONSTA
                # TODO: Verificar se BUSCA_SEQUENCIAL
                    # TODO: Adição de Valor da PJ em NAO_ENCONTRADAS
                    # TODO: Incrementar o CONTADOR_DE_PJ e Reiniciar o Fluxo
                # TODO: Atribuir ao CONTADOR_DE_PJ o Próximo Valor de NAO_ENCONTRADAS e Reiniciar o Fluxo
            # TODO: Digitar ENTER para Abrir a PJ (Validar a Funcionalidade)
            # TODO: Localizar e Clicar no Menu na Extremidade Direita do CPJ
            # TODO: Localizar e Mover o Mouse até a Opção de Sumário
            # TODO: Localizar e Clicar na Opção de SALVAR EM DISCO
            # TODO: Localizar e Clicar no LOCAL DE SALVAMENTO
            # TODO: Digitar ENTER para Efetuar o Salvamento (Validar a Funcionalidade)
            # TODO: Logging de Salvamento com Sucesso
            # TODO: Localizar e Clicar no Botão de VOLTAR
            # TODO: Verificar se BUSCA_SEQUENCIAL
                # TODO: Incrementar o CONTADOR_DE_PJ e Reiniciar o Fluxo
            # TODO: Atribuir ao CONTADOR_DE_PJ o Próximo Valor de NAO_ENCONTRADAS
            break
    except IndexError:
        # TODO: Logging de Encerramento de Fluxo
        pass
    except ImageNotFound:
        # TODO: Loggin de Encerramento de Fluxo
        pass


if __name__ == '__main__':
    setup_logging()
    main()
