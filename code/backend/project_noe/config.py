import os
import sys
import enum
import textwrap
from cryptography.fernet import Fernet
import environ
from environ._environ_config import _env_to_bool


def split_by_comma(value):
    return tuple(e.strip() for e in value.split(","))


@environ.config(prefix="")
class NoeConfig:
    debug = environ.bool_var(
        default=False, name="DJANGO_DEBUG", help="SECURITY WARNING: Don't run with debug turned on in production!"
    )
    secret_key = environ.var(help="SECURITY WARNING: keep the secret key used in production secret!")

    frontend_url = environ.var(help="Where the React frontend SPA is hosted")
    backend_url = environ.var(help="Where the Django backend is hosted")
    allowed_hosts = environ.var(default="*", converter=split_by_comma)
    allowed_cors_hosts = environ.var(default=None, converter=lambda val: split_by_comma(val) if val else None)
    behind_tls_proxy = environ.bool_var(
        default=False,
        help='Whether or not to set the "X-Forwarder-Proto" header to "https". Should be set to True behind a proxy.',
    )

    language_code = environ.var(default="hu-hu")
    time_zone = environ.var(default="Europe/Budapest")
    log_level = environ.var(default="INFO", help="Python logger log level")

    sentry_dsn_url = environ.var(
        default=None, name="SENTRY_DSN_URL", help="If you want to track exceptions with https://sentry.io",
    )

    @environ.config
    class Database:
        _DB_SQLITE_ENGINE = "django.db.backends.sqlite3"
        _PARAM_HELP = "Not required for SQLite"

        def _convert_database_engine(value):
            if value == "postgresql":
                return "django.db.backends.postgresql"
            elif value in ("mysql", "mariadb"):
                return "django.db.backends.mysql"
            elif value in ("sqlite", "sqlite3"):
                return NoeConfig.Database._DB_SQLITE_ENGINE

            raise ValueError(
                f'Invalid database engine: {value!r}\npossible values: "postgresql", "mysql", "mariadb", "sqlite"'
            )

        def _validate_param(obj, attribute, value):
            if not value and obj.engine != NoeConfig.Database._DB_SQLITE_ENGINE:
                raise ValueError(
                    f"The DJANGO_DATABASE_{attribute.name.upper()} environment variable is required\n{attribute!r}"
                )

        engine = environ.var(converter=_convert_database_engine)
        name = environ.var()
        user = environ.var(default=None, validator=_validate_param, help=_PARAM_HELP)
        password = environ.var(default=None, validator=_validate_param, help=_PARAM_HELP)
        host = environ.var(default=None, validator=_validate_param, help=_PARAM_HELP)
        port = environ.var(default=None, validator=_validate_param, help=_PARAM_HELP)

    database = environ.group(Database)

    @environ.config
    class Email:
        class Backend(enum.Enum):
            CONSOLE = "console"
            SMTP = "smtp"

        _PARAM_HELP = "Required for SMTP only"

        def _convert_backend(value):
            backend = NoeConfig.Email.Backend(value)
            return f"django.core.mail.backends.{backend.value}.EmailBackend"

        def _validate_param(obj, attribute, value):
            if not value and obj.backend == "smtp":
                raise ValueError(
                    f"The DJANGO_DATABASE_{attribute.name.upper()} environment variable is required\n{attribute!r}"
                )

        def _convert_verification_key(value):
            if value is None:
                raise ValueError("You need to generate an EMAIL_VERIFICATION_KEY.")

            value_bytes = value.encode()

            try:
                Fernet(value_bytes)
            except Exception as exc:
                raise ValueError(f"EMAIL_VERIFICATION_KEY: {value}")
            else:
                return value_bytes

        backend = environ.var(converter=_convert_backend, help='"console" or "smtp"')
        host = environ.var(default=None, help=_PARAM_HELP)
        port = environ.var(default=None, help=_PARAM_HELP)
        user = environ.var(default=None, help=_PARAM_HELP)
        password = environ.var(default=None, help=_PARAM_HELP)
        use_tls = environ.bool_var(default=True)
        default_from = environ.bool_var(help="Sender email address for automatic emails")
        verification_key = environ.var(
            default=None,
            converter=_convert_verification_key,
            help="SECRET_KEY for encrpyting the email verification token",
        )

    email = environ.group(Email)

    @environ.config
    class Static:
        url = environ.var(
            default="/static/",
            help=(
                "URL path generated for static files. "
                "If you change this, backend won't serve static files with WhiteNoise anymore."
            ),
        )
        root = environ.var(
            default="/project_noe/static_root",
            help=(
                "Where manage.py collectstatic put all static files. "
                "The default value is where the static files are in the Docker container"
            ),
        )

    static = environ.group(Static)

    default_time_slot_capacity = environ.var(default=30, converter=int)

    @environ.config
    class Szamlazzhu:
        agent_key = environ.var()
        invoice_prefix = environ.var()

    szamlazzhu = environ.group(Szamlazzhu)

    @environ.config
    class SimplePay:
        class Environment(enum.Enum):
            SANDBOX = "sandbox"
            LIVE = "live"

        merchant = environ.var()
        secret_key = environ.var()
        ipn_url = environ.var()
        use_live = environ.var(default=False)
        environment = environ.var(name="SIMPLEPAY_ENVIRONMENT", converter=Environment)

        def __attrs_post_init__(self):
            self.use_live = self.environment is NoeConfig.SimplePay.Environment.LIVE

    simplepay = environ.group(SimplePay)

    def __attrs_post_init__(self):
        if not self.allowed_cors_hosts and "*" not in self.allowed_hosts:
            self.allowed_cors_hosts = self.allowed_hosts


def print_config_schema():
    print("Possible configuration environment variables:")
    config_schema = NoeConfig.generate_help(display_defaults=True)
    for line in config_schema.splitlines():
        # Workaround for wrongly generated variable names
        print("-", line.lstrip("_"))


_django_debug = os.environ.get("DJANGO_DEBUG", False)

# bootstrapping is hard. environ-config can't handle this use-case
if _env_to_bool(_django_debug):
    # The dotenv package is installed only in a dev environment
    from dotenv import load_dotenv

    print("Loading environment variables from .env file")
    print()
    load_dotenv()


try:
    config = NoeConfig.from_environ()
except Exception as exc:
    print_config_schema()
    print()

    print("Error during loading environment variable:")
    exc_message = f"{exc.__class__.__name__}: {exc}"
    print(textwrap.indent(exc_message, "    "))

    sys.exit(1)
