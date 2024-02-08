from colorama import Fore


def compute_compound_interest(
    principle: int, no_years: int, rate_of_interest: float
):
    return (
        principle * ((100 + rate_of_interest) ** no_years) / (100**no_years)
    )


def compute_simple_interest(
    principle: float, no_years: int, rate_of_interest: float
):
    return principle + ((principle * no_years * rate_of_interest) / 100)


def main():
    principle = 1_00_000
    rate_of_interest = 9
    prefix, suffix = 8, 2
    for no_year in range(1, 41):
        simple_interest: float = compute_simple_interest(
            principle, no_year, rate_of_interest
        )
        compound_interest: int = compute_compound_interest(
            principle, no_year, rate_of_interest
        )
        print(
            Fore.YELLOW,
            f"{no_year:3d} {compound_interest:>{prefix}.{suffix}f}",
            Fore.RESET,
        )
        print(
            Fore.GREEN,
            f"{no_year:3d} {simple_interest:>{prefix}.{suffix}f}",
            Fore.RESET,
        )
        print(
            Fore.RED,
            f"    {compound_interest - simple_interest:{prefix}.{suffix}f}",
            Fore.RESET,
        )
        principle += 1_00_000
    print()


if __name__ == "__main__":
    main()
