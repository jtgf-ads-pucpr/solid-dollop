import os
import sys

# Garante que o diretorio raiz do projeto esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_helloworld_retorna_sucesso_e_mensagem_correta():
    """
    1. Caso normal:
    Verifica se a rota GET /helloworld retorna status code 200
    e a mensagem de boas-vindas esperada.
    """
    # Preparar (Arrange)
    endpoint = "/helloworld"
    mensagem_esperada = "Hello, World!"

    # Executar (Act)
    response = client.get(endpoint)

    # Verificar (Assert)
    assert response.status_code == 200
    dados = response.json()
    assert "message" in dados
    assert dados["message"] == mensagem_esperada


def test_endpoint_teste_gera_numero_dentro_dos_limites():
    """
    2. Valores-limite / Intervalo esperado:
    Verifica se a rota GET /teste retorna status code 200, confirmacao booleana
    e um numero inteiro contido dentro do limite definido (1 <= n <= 1000).
    """
    # Preparar (Arrange)
    endpoint = "/teste"
    limite_minimo = 1
    limite_maximo = 1000

    # Executar (Act)
    response = client.get(endpoint)

    # Verificar (Assert)
    assert response.status_code == 200
    dados = response.json()
    assert dados["teste"] is True
    assert isinstance(dados["num_aleatorio"], int)
    assert limite_minimo <= dados["num_aleatorio"] <= limite_maximo


def test_cadastrar_estudante_com_dados_validos():
    """
    3. Caso normal com criacao de entidade:
    Verifica se a rota POST /estudante/cadastro cadastra um estudante com dados validos,
    retornando status code 200, mensagem de sucesso e os dados persistidos.
    """
    # Preparar (Arrange)
    endpoint = "/estudante/cadastro"
    payload = {
        "nome": "Jhonatan Fernandes",
        "curso": "Analise e Desenvolvimento de Sistemas",
        "ativo": True,
    }

    # Executar (Act)
    response = client.post(endpoint, json=payload)

    # Verificar (Assert)
    assert response.status_code == 200
    dados = response.json()
    assert dados["message"] == "Estudante cadastrado com sucesso!"
    assert dados["estudante"]["nome"] == payload["nome"]
    assert dados["estudante"]["curso"] == payload["curso"]
    assert dados["estudante"]["ativo"] is True


def test_cadastrar_estudante_com_dados_invalidos_ou_incompletos():
    """
    4. Dados invalidos e campos ausentes:
    Verifica se a validacao rejeita requisicao com campos obrigatorios ausentes
    (sem 'curso' e sem 'ativo'), retornando status HTTP 422 Unprocessable Entity.
    """
    # Preparar (Arrange)
    endpoint = "/estudante/cadastro"
    payload_invalido = {
        "nome": "Estudante Incompleto"
        # campos 'curso' e 'ativo' ausentes propositalmente
    }

    # Executar (Act)
    response = client.post(endpoint, json=payload_invalido)

    # Verificar (Assert)
    assert response.status_code == 422
    dados = response.json()
    assert "detail" in dados
    campos_com_erro = [erro["loc"][-1] for erro in dados["detail"]]
    assert "curso" in campos_com_erro
    assert "ativo" in campos_com_erro


def test_atualizar_estudante_com_id_invalido_rejeita_com_erro():
    """
    5. Validacao de tipo de parametro de rota (Excecao/Valor fora do tipo):
    Verifica se a rota PUT /estudante/update/{id_estudante} rejeita um ID nao numerico,
    retornando erro de validacao HTTP 422 em vez de aceitar tipo inadequado.
    """
    # Preparar (Arrange)
    endpoint = "/estudante/update/id_invalido_texto"
    payload = {
        "nome": "Estudante Atualizado",
        "curso": "Engenharia de Software",
        "ativo": False,
    }

    # Executar (Act)
    response = client.put(endpoint, json=payload)

    # Verificar (Assert)
    assert response.status_code == 422
    dados = response.json()
    assert "detail" in dados
    assert any("id_estudante" in erro["loc"] for erro in dados["detail"])


def test_deletar_estudante_com_id_valido_retorna_confirmacao():
    """
    6. (Bonus) Operacao de exclusao de elemento:
    Verifica se a rota DELETE /estudante/delete/{id_estudante} processa
    a remocao com sucesso para um ID numerico valido.
    """
    # Preparar (Arrange)
    id_estudante = 42
    endpoint = f"/estudante/delete/{id_estudante}"

    # Executar (Act)
    response = client.delete(endpoint)

    # Verificar (Assert)
    assert response.status_code == 200
    dados = response.json()
    assert dados["message"] == f"Estudante com ID {id_estudante} deletado com sucesso!"
