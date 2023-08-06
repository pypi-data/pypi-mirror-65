import sys
import os

_COLORRED = "\033[0;31m"
_COLORNONE = "\033[0m"


def run(sys_args=None):
    try:
        import yaml
    except ImportError:
        sys.stderr.write(
            "{COLORRED}ERROR: ruamel.yaml not installed "
            "(pip install ruamel.yaml){COLORNONE}\n".format(
                COLORRED=_COLORRED, COLORNONE=_COLORNONE
            )
        )
        sys.exit(1)

    if sys_args is None:
        sys_args = sys.argv[1:]

    fpath = sys_args[0]

    if fpath == "--test":
        return

    if not os.path.exists(fpath):
        sys.stderr.write(
            "{COLORRED}ERROR: could not find path {fpath}{COLORNONE}\n"
            "".format(COLORRED=_COLORRED, COLORNONE=_COLORNONE, fpath=fpath)
        )
        sys.exit(1)
    with open(fpath) as f:
        config = yaml.safe_load(f)

    try:
        outstring = [
            config["store_path"],
            config["su_db_username"],
            config.get("db_port", 5432),
            config["profile"],
        ]
    except KeyError as error:
        sys.stderr.write(
            "{COLORRED}{error}{COLORNONE}\n".format(
                COLORRED=_COLORRED, COLORNONE=_COLORNONE, error=error
            )
        )
        sys.exit(1)

    sys.stdout.write(",".join([str(o) for o in outstring]))
