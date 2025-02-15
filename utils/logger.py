verbose_mode = False

def enable_verbose():
    global verbose_mode
    verbose_mode = True

def log(message):
    if verbose_mode:
        print(f"[LOG] {message}")
