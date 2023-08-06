from dataclasses import dataclass


@dataclass
class ShinobiClient:
    """
    Model of Shinobi installation.
    """
    host: str
    port: str
    super_user_token: str
    super_user_email: str = None
    super_user_password: str = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def user(self) -> "ShinobiUserOrm":
        from shinobi_client.orms.user import ShinobiUserOrm
        return ShinobiUserOrm(self)

    @property
    def api_key(self) -> "ShinobiApiKey":
        from shinobi_client.api_key import ShinobiApiKey
        return ShinobiApiKey(self)
