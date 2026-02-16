try:
    from IPython.core.getipython import get_ipython

    ip = get_ipython()
    if ip is not None:
        try:
            ip.run_line_magic("alias", "cls clear")
        except Exception:
            # Alias already exists or alias magic unavailable
            pass

        ip.run_line_magic("load_ext", "autoreload")
        ip.run_line_magic("autoreload", "2")
except Exception as e:
    print(f"Could not enable autoreload: {e}")