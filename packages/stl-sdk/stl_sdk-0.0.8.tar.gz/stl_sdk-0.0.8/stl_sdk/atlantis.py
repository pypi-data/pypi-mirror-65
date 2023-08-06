import jwt
import requests


class AtlantisClient:
    """Cliente HTTP para comunicação com Atlantis

    :param str atlantis_url: Endereço da API do serviço Atlantis
    :param str client_id: ID do cliente cadastrado no Atlantis
    :param str client_secret: Secret do cliente cadastrado no Atlantis
    """

    def __init__(self, atlantis_url, client_id, client_secret):
        self.atlantis_url = atlantis_url
        self.client_id = client_id
        self.client_secret = client_secret

    def issue_token(self, code):
        """Realiza a troca do code pelo token

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import AtlantisClient

            client = AtlantisClient('https://accounts.spacetimeanalytics.com', 'client_id_abc123', 'client_secret_123abc')
            token = client.issue_token('code123abc')

        :param code: Código concedido pelo Atlantis via redirect (authorization_code)
        :type code: str
        :return: Dicionário com os tokens: ``access_token``, ``id_token`` e ``refresh_token``
        :rtype: dict
        """
        response = requests.post(
            '{}/api/token'.format(self.atlantis_url),
            data={
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            },
            params={
                'grant_type': 'authorization_code'
            })
        response.raise_for_status()
        return response.json()

    def get_public_key(self):
        """Obtém a chave pública do Atlantis para validação do token de acesso

        :return: Chave pública
        :rtype: str
        """
        response = requests.get('{}/api/public-key'.format(self.atlantis_url))
        response.raise_for_status()
        return response.json()

    def validate_token(self, id_token):
        """Valida token de acesso do usuário

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import AtlantisClient

            client = AtlantisClient('https://accounts.spacetimeanalytics.com', 'client_id_abc123')
            token_payload = client.validate_token('tokenJwT')

        :param id_token: Token JWT do usuário gerado pelo Atlantis
        :type id_token: str
        :raises InvalidTokenError: Se o token estiver expirado ou alterado
        :return: Retorna o payload do token JWT
        :rtype: dict
        """
        public_key = self.get_public_key()

        try:
            return jwt.decode(id_token, public_key, audience=self.client_id)
        except Exception as err:
            raise InvalidTokenError(err)

    def introspect_token(self, access_token):
        """Verifica se o access_token está válido

        :param access_token: Token do usuário gerado pelo Atlantis
        :type access_token: str
        :return: Retorna dados do token: ``active``, ``email``, ``scope``, ``client_id``, ``exp``, etc..
        :rtype: dict
        """
        response = requests.post(
            '{}/api/instrospect'.format(self.atlantis_url),
            data={
                'token': access_token,
                'token_type_hint': 'access_token',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            })
        response.raise_for_status()
        return response.json()


class InvalidTokenError(RuntimeError):
    pass
