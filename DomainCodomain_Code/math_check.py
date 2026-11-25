"""
Independent numerical check of every example used in the video.
Run:  python math_check.py
Every line should print OK.  (No animation library needed, only Python + NumPy.)
"""
from fractions import Fraction
import numpy as np


def check(name, cond):
    print(("OK    " if cond else "FAIL  ") + name)
    assert cond, name


# --- Mapping diagram: A = {1,2,3}, B = {a,b,c,d}, 1->a, 2->b, 3->b
A, B = {1, 2, 3}, {"a", "b", "c", "d"}
f = {1: "a", 2: "b", 3: "b"}
check("mapping: every input has exactly one output (dict = one value per key)", set(f) == A)
rng = set(f.values())
check("mapping: range = {a, b}", rng == {"a", "b"})
check("mapping: range is a subset of the codomain", rng <= B)
check("mapping: c and d are in the codomain but not in the range", {"c", "d"} == B - rng)

# --- Example 1: f(x) = x^2, f: R -> R
xs = np.linspace(-1000, 1000, 400001)
ys = xs ** 2
check("ex1: x^2 >= 0 for every sampled real x (range is inside [0, inf))", ys.min() >= 0)
check("ex1: x^2 reaches 0", ys.min() == 0)
for y in [0, 0.5, 1, 4, 9, 1e6]:
    check(f"ex1: every y = {y} >= 0 is hit (x = sqrt(y) gives x^2 = y)", abs(np.sqrt(y) ** 2 - y) < 1e-6 * max(1, y))
check("ex1: -2 is NOT hit (x^2 = -2 has discriminant 0 - 4*1*2 < 0)", 0 - 4 * 1 * 2 < 0)

# --- Example 2: f(x) = sqrt(x - 2)
check("ex2: x - 2 >= 0 exactly when x >= 2", all((x - 2 >= 0) == (x >= 2) for x in np.linspace(-5, 10, 1501)))
xs = np.linspace(2, 10000, 200001)
vals = np.sqrt(xs - 2)
check("ex2: all outputs >= 0", vals.min() >= 0 and vals.min() == 0)
for y in [0, 0.5, 1, 2, 10, 123.4]:
    x = y ** 2 + 2
    check(f"ex2: y = {y} is hit by x = y^2 + 2 = {x:.4g} and x >= 2", x >= 2 and abs(np.sqrt(x - 2) - y) < 1e-9)
check("ex2: f(6) = sqrt(4) = 2 and 2^2 + 2 = 6", np.sqrt(6 - 2) == 2 and 2 ** 2 + 2 == 6)

# --- Example 3: f(x, y) = sqrt(1 - x^2 - y^2)
check("ex3: (0,0) -> 1", 1 - 0 - 0 == 1)
check("ex3: (0.6, 0.8) -> 0  (exact fractions: 1 - 36/100 - 64/100 = 0)",
      1 - Fraction(36, 100) - Fraction(64, 100) == 0)
check("ex3: (1, 1) gives 1 - 1 - 1 = -1 < 0, so (1,1) is not in the domain", 1 - 1 - 1 < 0)
rng_ = np.random.default_rng(0)
pts = rng_.uniform(-1, 1, size=(2_000_000, 2))
inside = pts[(pts ** 2).sum(axis=1) <= 1]
out = np.sqrt(1 - (inside ** 2).sum(axis=1))
check("ex3: on 1M+ random points of the unit disk the output stays in [0, 1]", out.min() >= 0 and out.max() <= 1)
check("ex3: outputs get close to both ends (min < 0.001, max > 0.999)", out.min() < 1e-3 and out.max() > 0.999)
for t in [0.1, 0.5, 0.77, 1.0]:
    # every value t in [0,1] is hit: take (x, y) = (sqrt(1 - t^2), 0)
    x = np.sqrt(1 - t ** 2)
    check(f"ex3: value {t} is hit by ({x:.4f}, 0)", abs(np.sqrt(1 - x ** 2 - 0) - t) < 1e-9)
print("\nAll checks passed.")
