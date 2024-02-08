import platform


def get_systemdetails():
    instruction_set, OS_Name = platform.architecture()
    print(f"User         : {platform.node()}")
    print(f"System       : {platform.system()} {platform.release()}")
    print(f"System       : {platform.system()} {platform.version()}")
    print(f"Machine      : {platform.machine()}")
    print(f"Processor    : {platform.processor()}")
    print(f"Architecture : {instruction_set} {OS_Name}")


if __name__ == "__main__":
    get_systemdetails()
