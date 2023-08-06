def __init__(hub):
    pass


def build(hub, bname):
    """
    Given the build arguments, Make a package!
    """
    pkg_builder = hub.OPT["pop_build"]["pkg_builder"]
    getattr(hub, f"pop_build.pkg.{pkg_builder}.build")(bname)
