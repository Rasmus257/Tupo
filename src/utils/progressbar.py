def ProgressBar(iteration, total, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 100, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)

    if iteration == total:
        print()
