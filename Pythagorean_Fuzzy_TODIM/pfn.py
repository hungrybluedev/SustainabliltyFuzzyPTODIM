import math

_eps = 1e-5

# Implementation based off of dx.doi.org/doi:10.1016/j.asoc.2015.12.020


class PythagoreanFN(object):
    def __init__(self, mu, nu):
        if mu**2 + nu**2 > 1.0:
            raise ValueError('mu and nu lie outside allowed range')
        self.mu = mu
        self.nu = nu

        self.pi = math.sqrt(1 - mu**2 - nu**2)
        self.score = mu**2 - nu**2
        self.h_score = mu**2 + nu**2

    def __neg__(self):
        return PythagoreanFN(self.nu, self.mu)

    def compare(self, next):
        if type(next) != PythagoreanFN:
            raise ValueError('Operand must be of type PythagoreanFN')
        s_diff = self.score - next.score

        # Compare with the score first
        if abs(s_diff) > _eps:
            return -1 if s_diff < 0 else +1

        # Now the scores are equal so use h_scores
        h_diff = self.h_score - next.h_score
        if abs(h_diff) > _eps:
            return -1 if h_diff < 0 else +1
        return 0

    def __eq__(self, next):
        if type(next) != PythagoreanFN:
            raise ValueError('Operand must be of type PythagoreanFN')
        return self.compare(next) == 0

    def __gt__(self, next):
        if type(next) != PythagoreanFN:
            raise ValueError('Operand must be of type PythagoreanFN')
        return self.compare(next) > 0

    def __lt__(self, next):
        if type(next) != PythagoreanFN:
            raise ValueError('Operand must be of type PythagoreanFN')
        return self.compare(next) < 0

    def __str__(self):
        return f'{self.mu, self.nu}'

    def distance(self, next):
        if type(next) != PythagoreanFN:
            raise ValueError('Operand must be of type PythagoreanFN')
        mu1s = self.mu**2
        mu2s = next.mu**2
        nu1s = self.nu**2
        nu2s = next.nu**2
        pi1s = self.pi**2
        pi2s = next.pi**2

        return math.sqrt(
            0.5 * (
                (mu1s - mu2s)**2 +
                (nu1s - nu2s)**2 +
                (pi1s - pi2s)**2)
        )


def parse_pfn(string):
    # 1. remove extra whitespace (if any)
    # 2. Discard opening and closing parentheses
    # 3. Split based on comma
    parts = string.strip()[1:-1].split(",")
    if len(parts) != 2:
        raise ValueError('Need 2 real values for creating PFNs')

    a, b = parts[0].strip(), parts[1].strip()
    mu = float(a)
    nu = float(b)

    if mu < 0.0 or mu > 1.0:
        raise ValueError('mu must be in (0, 1)')
    if nu < 0.0 or nu > 1.0:
        raise ValueError('nu must be in (0, 1)')

    return PythagoreanFN(mu, nu)
