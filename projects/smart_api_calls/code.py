import random

from tenacity import retry, stop_after_attempt, wait_exponential_jitter


def network_failure():
    rnc = random.uniform(1, 4)
    if rnc < 2:
        raise ValueError


@retry(
    stop=stop_after_attempt(
        max_attempt_number=5,
    ),
    wait=wait_exponential_jitter(
        initial=1,
        max=10,
        exp_base=3,
        jitter=2,
    ),
)
def fetch():
    print('trying...')
    network_failure()
    return {'status': 'ok'}


print(fetch())
