import enum
import environ


@environ.config(prefix="SIMPLEPAY")
class SimplePayConfig:
    class Environment(enum.Enum):
        SANDBOX = "sandbox"
        LIVE = "live"

    merchant = environ.var()
    secret_key = environ.var()
    ipn_url = environ.var()
    use_live = environ.var(default=False)
    environment = environ.var(converter=Environment)

    def __attrs_post_init__(self):
        self.use_live = self.environment is SimplePayConfig.Environment.LIVE


simplepay_config = SimplePayConfig.from_environ()
