from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

COMMON_CONFIG = {
    "env_file": ".env",
    "extra": "ignore",
}


class OpenRouterSettings(BaseSettings):
    base_url: str = "https://openrouter.ai/api/v1"
    api_key: str
    model: str

    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
        env_prefix="OPENROUTER_",
    )


class GithubSettings(BaseSettings):
    token: str

    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
        env_prefix="GITHUB_",
    )


class Settings(BaseSettings):
    openrouter: OpenRouterSettings = Field(default_factory=OpenRouterSettings)
    github: GithubSettings = Field(default_factory=GithubSettings)
    debug: bool = False

    model_config = SettingsConfigDict(**COMMON_CONFIG)


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
