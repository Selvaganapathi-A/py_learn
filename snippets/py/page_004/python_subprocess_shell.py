import re
import sys
from subprocess import call, check_output, run

call(
    ('cls',),
    shell=True,
)
run(
    ('cls',),
    shell=True,
)
data = check_output(('ipconfig', '/all'))
# with open("ghost.txt", "wb") as writer:
#     writer.write(data)
#     writer.flush()
#     writer.close()
data = data.decode()
print(data)
print('-' * 80)
# sys.exit(208)
var = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', data, re.MULTILINE)
var = re.search(
    r'IPv4.*?\ (?P<ip>(2[0-5][0-5]|1?[0-9]?[0-9]\.){3}(2[0-5][0-5]|1?[0-9]?[0-9]))',
    data,
    re.MULTILINE,
)
if var:
    device_ip = var.group('ip')
    # print(f"{device_ip!r}")
    # print("".join(("py", " -m", " http.server", " -b", f" {device_ip}", " 8000")))
    try:
        run(
            (
                'python',
                '-m',
                'http.server',
                '-b',
                device_ip,
                '8999',
            ),
            shell=True,
        )
    except KeyboardInterrupt:
        pass
