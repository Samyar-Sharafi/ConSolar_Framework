def logger(target, show_target, repeat:int = 1) -> None:
    if show_target:
        for i in range(repeat):
            print(target)
    else:
        print("[red]Logging is disabled because 'show_target' is set to False.[/red]")
