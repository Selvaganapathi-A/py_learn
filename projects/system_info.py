def print_system_details():
    import os
    import platform
    import shutil

    COLS, _ = shutil.get_terminal_size()

    padding_length: int = int(COLS * 0.3)

    instruction_set, OS_Name = platform.architecture()
    print(f'{"User": <{padding_length}} : {platform.node()}')
    print(
        (
            f'{"System": <{padding_length}} : {platform.system()} {platform.release()}({platform.version()})'
        )
    )
    print(f'{"Instruction Set": <{padding_length}} : {platform.machine()}')
    print(f'{"Processor": <{padding_length}} : {platform.processor()}')
    print(f'{"Architecture": <{padding_length}} : {instruction_set} {OS_Name}')
    print(
        f'{"CPU Count": <{padding_length}} : {os.cpu_count()} Core Processor'
    )


if __name__ == '__main__':
    print_system_details()
