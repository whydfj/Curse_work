from authx import AuthXConfig, AuthX

config = AuthXConfig()

config.JWT_ACCESS_COOKIE_NAME = "aboba"
config.JWT_SECRET_KEY = "test-secret-key"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False  # 👈 отключаем CSRF проверку

security = AuthX(config=config)
