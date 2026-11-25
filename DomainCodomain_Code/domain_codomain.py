"""
M3 Internal Assessment - Animation Video (Option 1)
Topic : Domain, Codomain and Range (through mapping diagrams)

Render the full video (1080p, 30 fps):
    manim -qh --fps 30 domain_codomain.py DomainCodomainVideo

Quick preview while editing (480p, fast):
    manim -ql domain_codomain.py DomainCodomainVideo

No LaTeX is needed: every label is drawn with Text(), not MathTex().
While rendering, the script writes marks.txt (a list of timestamps), which
is useful for lining up the voice-over.
"""

from manim import *
import numpy as np

from config import STUDENT_NAME, STUDENT_ID, MUSIC_CREDIT   # edit config.py, not this file

DOM = BLUE_C      # domain  = blue   (everywhere in the video)
COD = GREEN_C     # codomain = green
RAN = ORANGE      # range   = orange
BAD = RED_C
BG = "#12141f"
WAIT_SCALE = 1.5   # 1.0 = tight, 1.5 = relaxed (about 4:40 total)

PAD = {  # extra seconds added at the END of each segment so the voice-over fits
    'Scene 1 - Hook: vending machine': 0.3,
    'Scene 2 - Concept introduction': 0.7,
    'Definitions: domain, codomain, range': 1.0,
    'Learning objective': 0.8,
    'Scene 3 - Visual intuition: mapping diagram': 3.8,
    'Range highlighted': 1.8,
    'Scene 4 - Example 1: f(x) = x^2': 0.3,
    'Ex1: domain': 0.7,
    'Ex1: -2 is in the codomain but not the range': 0.7,
    'Scene 4 - Example 2: f(x) = sqrt(x - 2)': 1.8,
    'Ex3: domain is a region of the plane': 1.3,
    'Ex3: test points': 3.2,
    'Scene 6 - Summary': 0.2,
}


def T(s, size=30, color=WHITE, **kw):
    return Text(s, font_size=size, color=color, **kw)


class DomainCodomainVideo(Scene):

    # ------------------------------------------------------------ utilities
    def construct(self):
        self.camera.background_color = BG
        self.marks = []
        self.last_label = None
        self._padded = True
        self.opening_frame()
        self.scene1_hook()
        self.scene2_concept()
        self.scene3_visual()
        self.scene4_examples()
        self.scene5_interpretation()
        self.scene6_summary()
        with open("marks.txt", "w") as f:
            f.write("\n".join(self.marks) + "\n")

    def wait(self, duration=1.0, **kw):
        # all pauses are stretched a little so the voice-over has room to breathe
        super().wait(duration * WAIT_SCALE, **kw)

    def _pad(self):
        if not self._padded:
            extra = PAD.get(self.last_label, 0)
            if extra:
                super().wait(extra)
            self._padded = True

    def mark(self, label):
        self._pad()
        self._padded = False
        self.last_label = label
        self.marks.append(f"{self.time:6.1f}s  {label}")

    def clear(self, t=0.6):
        self._pad()
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=t)

    def heading(self, s):
        h = T(s, 38, weight=BOLD).to_edge(UP, buff=0.35)
        self.play(FadeIn(h, shift=DOWN * 0.2), run_time=0.6)
        return h

    def note(self, old, text, color=WHITE, size=30):
        """Swap the caption at the bottom of the screen."""
        new = T(text, size, color).to_edge(DOWN, buff=0.55)
        if old is None:
            self.play(FadeIn(new, shift=UP * 0.2), run_time=0.6)
        else:
            self.play(FadeOut(old), FadeIn(new, shift=UP * 0.2), run_time=0.6)
        return new

    def make_map(self, A, B, pairs, center=ORIGIN, gap=6.0, ew=3.0,
                 off=0.9, lo=0.4, step=0.85, lab=30):
        """Mapping diagram: two ovals, dots, labels, arrows."""
        h = max(len(A), len(B)) * step + 0.6
        cl, cr = center[0] - gap / 2, center[0] + gap / 2
        left = Ellipse(width=ew, height=h, color=DOM).move_to([cl, center[1], 0])
        right = Ellipse(width=ew, height=h, color=COD).move_to([cr, center[1], 0])

        def column(items, cx, side):
            n = len(items)
            dots, labs = {}, {}
            for i, it in enumerate(items):
                y = center[1] + (n - 1) * step / 2 - i * step
                sgn = 1 if side == "L" else -1
                dots[it] = Dot([cx + sgn * off, y, 0], radius=0.08)
                labs[it] = T(it, lab).move_to([cx - sgn * lo, y, 0])
            return dots, labs

        ad, al = column(A, cl, "L")
        bd, bl = column(B, cr, "R")
        arrows = {}
        for a, b in pairs:
            arrows[(a, b)] = Arrow(ad[a].get_center(), bd[b].get_center(),
                                   buff=0.12, stroke_width=3,
                                   max_tip_length_to_length_ratio=0.12,
                                   color=WHITE)
        return dict(left=left, right=right, ad=ad, al=al, bd=bd, bl=bl,
                    arrows=arrows)

    def tick_labels(self, ax, xs=(), ys=(), size=20):
        out = VGroup()
        for x in xs:
            out.add(T(str(x).replace("-", "\u2212"), size, GREY_B)
                    .next_to(ax.c2p(x, 0), DOWN, buff=0.12))
        for y in ys:
            out.add(T(str(y).replace("-", "\u2212"), size, GREY_B)
                    .next_to(ax.c2p(0, y), LEFT, buff=0.12))
        return out

    # ------------------------------------------------------- opening frame
    def opening_frame(self):
        self.mark("Opening frame")
        title = T("Domain, Codomain and Range", 56, weight=BOLD)
        sub = T("Understanding them through visual mapping", 30, GREY_A)
        course = T("M3: Linear Algebra and Calculus  |  Internal Assessment", 24, GREY_B)
        who = T(f"{STUDENT_NAME}   |   {STUDENT_ID}", 28, YELLOW_B)
        g = VGroup(title, sub, course, who).arrange(DOWN, buff=0.45)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(sub), FadeIn(course), run_time=0.8)
        self.play(FadeIn(who), run_time=0.6)
        self.wait(2.5)
        self.clear()

    # ------------------------------------------------------ scene 1: hook
    def scene1_hook(self):
        self.mark("Scene 1 - Hook: vending machine")
        h = self.heading("A vending machine puzzle")
        M = self.make_map(["A1", "A2", "A3"],
                          ["Chips", "Biscuit", "Juice", "Candy"],
                          [("A1", "Chips"), ("A2", "Juice"), ("A3", "Juice")],
                          center=DOWN * 0.2, gap=6.4)
        t_btn = T("Buttons", 28, DOM).next_to(M["left"], UP, buff=0.2)
        t_shelf = T("Shelf", 28, COD).next_to(M["right"], UP, buff=0.2)
        self.play(Create(M["left"]), Create(M["right"]),
                  FadeIn(t_btn), FadeIn(t_shelf), run_time=1.2)
        self.play(*[FadeIn(m) for m in list(M["ad"].values()) + list(M["al"].values())
                    + list(M["bd"].values()) + list(M["bl"].values())], run_time=1.0)
        cap = self.note(None, "Every button gives exactly one snack.")
        self.wait(2.0)
        self.mark("Hook: arrows drawn one by one")
        for key in [("A1", "Chips"), ("A2", "Juice"), ("A3", "Juice")]:
            self.play(Create(M["arrows"][key]), run_time=0.9)
            self.wait(0.4)
        self.wait(1.0)

        self.mark("Hook: two buttons, one snack")
        cap = self.note(cap, "Two buttons, same snack?   Allowed.", GREEN_B)
        self.play(Indicate(M["arrows"][("A2", "Juice")]),
                  Indicate(M["arrows"][("A3", "Juice")]), run_time=1.2)
        self.wait(1.5)

        self.mark("Hook: unreachable snacks")
        cap = self.note(cap, "A snack no button gives?   Allowed.", GREEN_B)
        r1 = SurroundingRectangle(VGroup(M["bl"]["Biscuit"], M["bd"]["Biscuit"]), color=YELLOW, buff=0.12)
        r2 = SurroundingRectangle(VGroup(M["bl"]["Candy"], M["bd"]["Candy"]), color=YELLOW, buff=0.12)
        self.play(Create(r1), Create(r2), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(r1), FadeOut(r2), run_time=0.4)

        self.mark("Hook: button giving nothing / two things")
        cap = self.note(cap, "A button that gives nothing, or two snacks?   Not allowed.", BAD)
        self.wait(3.0)

        self.mark("Hook: bridge to the definitions")
        cap = self.note(cap, "Buttons = inputs.   Shelf = where outputs may land.", WHITE)
        self.play(M["left"].animate.set_fill(DOM, 0.2), M["right"].animate.set_fill(COD, 0.2),
                  run_time=1.0)
        self.wait(3.0)
        self.clear()

    # ---------------------------------------------- scene 2: concept intro
    def scene2_concept(self):
        self.mark("Scene 2 - Concept introduction")
        h = self.heading("What is a function?")
        d1 = T("A function  f : A \u2192 B  gives each input in A", 32).shift(UP * 2.0)
        d2 = T("exactly one output in B.", 32).next_to(d1, DOWN, buff=0.2)
        self.play(Write(d1), Write(d2), run_time=2.0)
        self.wait(2.0)

        self.mark("Definitions: domain, codomain, range")
        rows = VGroup(
            T("Domain:  the set A of allowed inputs", 32, t2c={"Domain": DOM}),
            T("Codomain:  the set B where outputs are declared to land", 32, t2c={"Codomain": COD}),
            T("Range:  the outputs that actually occur,  f(A) \u2286 B", 32, t2c={"Range": RAN}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, -0.5, 0])
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(2.2)

        self.mark("Learning objective")
        box = RoundedRectangle(corner_radius=0.15, width=12.2, height=1.3, color=GREY_B)
        box.to_edge(DOWN, buff=0.3)
        obj = VGroup(T("By the end of this video, you will be able to identify the", 26),
                     T("domain, codomain and range of a function, and explain how they differ.", 26)
                     ).arrange(DOWN, buff=0.12).move_to(box)
        self.play(Create(box), FadeIn(obj), run_time=1.0)
        self.wait(4.0)
        self.clear()

    # ------------------------------------------- scene 3: visual intuition
    def scene3_visual(self):
        self.mark("Scene 3 - Visual intuition: mapping diagram")
        h = self.heading("Reading a mapping diagram")
        A, B = ["1", "2", "3"], ["a", "b", "c", "d"]
        pairs = [("1", "a"), ("2", "b"), ("3", "b")]
        M = self.make_map(A, B, pairs, center=DOWN * 0.25, gap=6.0)
        tA = T("A", 30, DOM).next_to(M["left"], UP, buff=0.2)
        tB = T("B", 30, COD).next_to(M["right"], UP, buff=0.2)
        self.play(Create(M["left"]), Create(M["right"]), FadeIn(tA), FadeIn(tB), run_time=1.0)
        self.play(*[FadeIn(m) for m in list(M["ad"].values()) + list(M["al"].values())
                    + list(M["bd"].values()) + list(M["bl"].values())], run_time=0.8)
        self.wait(1.0)
        for key in pairs:
            self.play(Create(M["arrows"][key]), run_time=0.8)
            self.wait(0.3)
        eq = T("f(1) = a,   f(2) = b,   f(3) = b", 28, GREY_A).next_to(h, DOWN, buff=0.3)
        self.play(FadeIn(eq), run_time=0.6)
        self.wait(2.0)

        self.mark("Domain highlighted")
        cap = self.note(None, "Domain = the whole left set A = {1, 2, 3}", DOM)
        self.play(M["left"].animate.set_fill(DOM, 0.25), run_time=1.0)
        self.wait(3.0)

        self.mark("Codomain highlighted")
        cap = self.note(cap, "Codomain = the whole right set B = {a, b, c, d}", COD)
        self.play(M["right"].animate.set_fill(COD, 0.25), run_time=1.0)
        self.wait(3.0)

        self.mark("Range highlighted")
        cap = self.note(cap, "Range = the elements of B that receive an arrow = {a, b}", RAN)
        self.play(*[M["bl"][k].animate.set_color(RAN) for k in "ab"],
                  *[M["bd"][k].animate.set_color(RAN) for k in "ab"],
                  *[M["bl"][k].animate.set_color(GREY_C) for k in "cd"],
                  *[M["bd"][k].animate.set_color(GREY_C) for k in "cd"], run_time=1.0)
        self.wait(3.0)
        cap = self.note(cap, "c and d are in the codomain, but not in the range.", YELLOW_B)
        self.wait(3.0)
        self.clear()

        # ---- what is NOT a function
        self.mark("Function test: one arrow per input")
        h = self.heading("What makes a relation a function?")
        bad1 = self.make_map(["1", "2"], ["a", "b"], [("1", "a"), ("1", "b"), ("2", "b")],
                             center=LEFT * 3.5 + UP * 0.35, gap=3.4, ew=2.0, off=0.45, lo=0.3)
        bad2 = self.make_map(["1", "2"], ["a", "b"], [("1", "a")],
                             center=RIGHT * 3.5 + UP * 0.35, gap=3.4, ew=2.0, off=0.45, lo=0.3)
        for M2 in (bad1, bad2):
            self.play(Create(M2["left"]), Create(M2["right"]),
                      *[FadeIn(m) for m in list(M2["ad"].values()) + list(M2["al"].values())
                        + list(M2["bd"].values()) + list(M2["bl"].values())], run_time=0.8)
            self.play(*[Create(a) for a in M2["arrows"].values()], run_time=0.8)
        c1 = T("1 has two arrows", 26, BAD).next_to(bad1["left"], DOWN, buff=0.75).shift(RIGHT * 1.7)
        c2 = T("2 has no arrow", 26, BAD).next_to(bad2["left"], DOWN, buff=0.75).shift(RIGHT * 1.7)
        x1 = T("\u2717  not a function", 30, BAD).next_to(c1, DOWN, buff=0.2)
        x2 = T("\u2717  not a function", 30, BAD).next_to(c2, DOWN, buff=0.2)
        self.play(FadeIn(c1), FadeIn(x1), run_time=0.8)
        self.wait(2.5)
        self.play(FadeIn(c2), FadeIn(x2), run_time=0.8)
        self.wait(2.5)
        cap = self.note(None, "Rule: every input in the domain has exactly ONE arrow.", YELLOW_B)
        self.wait(4.0)
        self.clear()

    # --------------------------------------------- scene 4: worked examples
    def scene4_examples(self):
        self.example1()
        self.example2()
        self.example3()

    def example1(self):
        self.mark("Scene 4 - Example 1: f(x) = x^2")
        h = self.heading("Example 1:   f(x) = x\u00b2")
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 9, 1], x_length=6.2, y_length=5.0,
                  tips=False, axis_config={"color": GREY_B}).shift(RIGHT * 3.9 + DOWN * 0.55)
        labels = self.tick_labels(ax, xs=[-3, 3], ys=[-2, 4, 8])
        xl = T("x", 24).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = T("y", 24).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        graph = ax.plot(lambda x: x ** 2, x_range=[-3, 3], color=WHITE)

        L1 = T("f : \u211d \u2192 \u211d,    f(x) = x\u00b2", 28)
        L2 = T("Domain: any real x works  \u2192  \u211d", 26, t2c={"Domain": DOM})
        L3 = T("Codomain: \u211d  (we declared it)", 26, t2c={"Codomain": COD})
        L4 = T("Range: x\u00b2 is never negative\n\u2192  [0, \u221e)", 26, t2c={"Range": RAN})
        side = VGroup(L1, L2, L3, L4).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        side.to_edge(LEFT, buff=0.5).shift(UP * 0.4)

        self.play(FadeIn(L1), run_time=0.8)
        self.play(Create(ax), FadeIn(labels), FadeIn(xl), FadeIn(yl), run_time=1.2)
        self.play(Create(graph), run_time=1.5)
        self.wait(1.5)

        self.mark("Ex1: domain")
        dom_line = Line(ax.c2p(-4, 0), ax.c2p(4, 0), color=DOM, stroke_width=8)
        self.play(FadeIn(L2), Create(dom_line), run_time=1.2)
        self.wait(3.0)

        self.mark("Ex1: codomain")
        cod_line = Line(ax.c2p(0, -3), ax.c2p(0, 9), color=COD, stroke_width=8, stroke_opacity=0.6)
        self.play(FadeIn(L3), Create(cod_line), run_time=1.2)
        self.wait(3.0)

        self.mark("Ex1: range")
        ran_line = Line(ax.c2p(0, 0), ax.c2p(0, 9), color=RAN, stroke_width=8)
        self.play(FadeIn(L4), Create(ran_line), run_time=1.2)
        self.wait(3.0)

        self.mark("Ex1: -2 is in the codomain but not the range")
        pt = Dot(ax.c2p(0, -2), color=BAD, radius=0.11)
        tx = T("\u22122 is in the codomain, but no real x gives x\u00b2 = \u22122", 24, BAD).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(pt), FadeIn(tx), run_time=1.0)
        self.wait(5.0)
        self.clear()

    def example2(self):
        self.mark("Scene 4 - Example 2: f(x) = sqrt(x - 2)")
        h = self.heading("Example 2:   f(x) = \u221a(x \u2212 2)")
        ax = Axes(x_range=[-1, 8, 1], y_length=4.2, y_range=[-1, 3, 1], x_length=6.0,
                  tips=False, axis_config={"color": GREY_B}).shift(RIGHT * 3.6 + DOWN * 0.5)
        labels = self.tick_labels(ax, xs=[2, 4, 6], ys=[1, 2])
        xl = T("x", 24).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = T("y", 24).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        graph = ax.plot(lambda x: np.sqrt(x - 2), x_range=[2, 8], color=WHITE)

        S1 = T("A square root needs  x \u2212 2 \u2265 0", 26)
        S2 = T("so  x \u2265 2", 26)
        S3 = T("Domain = [2, \u221e)", 28, t2c={"Domain": DOM})
        S4 = T("Outputs are \u2265 0, and for any y \u2265 0\nthe input x = y\u00b2 + 2 gives f(x) = y", 24)
        S5 = T("Range = [0, \u221e)\nCodomain: \u211d", 28, t2c={"Range": RAN, "Codomain": COD})
        side = VGroup(S1, S2, S3, S4, S5).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        side.to_edge(LEFT, buff=0.5).shift(UP * 0.1)

        self.play(Create(ax), FadeIn(labels), FadeIn(xl), FadeIn(yl), run_time=1.2)
        self.play(FadeIn(S1), run_time=0.8)
        self.wait(2.5)
        self.play(FadeIn(S2), run_time=0.6)
        self.wait(1.5)

        self.mark("Ex2: domain")
        dom_line = Line(ax.c2p(2, 0), ax.c2p(8, 0), color=DOM, stroke_width=8)
        self.play(FadeIn(S3), Create(dom_line), run_time=1.2)
        self.play(Create(graph), run_time=1.5)
        self.play(FadeIn(Dot(ax.c2p(2, 0), color=WHITE, radius=0.09)), run_time=0.4)
        self.wait(2.5)

        self.mark("Ex2: range")
        self.play(FadeIn(S4), run_time=0.8)
        self.wait(4.0)
        ran_line = Line(ax.c2p(0, 0), ax.c2p(0, 3), color=RAN, stroke_width=8)
        self.play(FadeIn(S5), Create(ran_line), run_time=1.2)
        self.wait(3.0)
        chk = T("Check: f(6) = \u221a4 = 2, and 2\u00b2 + 2 = 6", 24, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(chk), run_time=0.6)
        self.wait(3.5)
        self.clear()

    def example3(self):
        self.mark("Scene 4 - Example 3: two variables")
        h = self.heading("Example 3:   f(x, y) = \u221a(1 \u2212 x\u00b2 \u2212 y\u00b2)")
        ax = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=4.6, y_length=4.6,
                  tips=False, axis_config={"color": GREY_B}).shift(LEFT * 4.0 + DOWN * 0.45)
        labels = self.tick_labels(ax, xs=[-1, 1], ys=[-1, 1], size=18)
        xl = T("x", 22).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = T("y", 22).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        rad = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        disk = Circle(radius=rad, color=DOM, stroke_width=4).set_fill(DOM, 0.3).move_to(ax.c2p(0, 0))

        S1 = T("Inputs are PAIRS (x, y)", 28)
        S2 = T("Need  1 \u2212 x\u00b2 \u2212 y\u00b2 \u2265 0,  i.e.  x\u00b2 + y\u00b2 \u2264 1", 26)
        S3 = T("Domain = the unit disk", 28, t2c={"Domain": DOM})
        S4 = T("(0, 0) \u2192 1       (0.6, 0.8) \u2192 0", 26)
        S5 = T("(1, 1) \u2192 \u221a(\u22121):  not allowed", 26, BAD)
        S6 = T("Range = [0, 1]      Codomain: \u211d", 28, t2c={"Range": RAN, "Codomain": COD})
        side = VGroup(S1, S2, S3, S4, S5, S6).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        side.move_to([3.2, 0.55, 0])

        nl = NumberLine(x_range=[-1, 2, 1], length=5.2, include_ticks=True, include_numbers=False,
                        color=GREY_B).move_to([3.2, -2.6, 0])
        nl_lab = VGroup(*[T(s, 20, GREY_B).next_to(nl.n2p(v), DOWN, buff=0.12)
                          for v, s in [(-1, "\u22121"), (0, "0"), (1, "1"), (2, "2")]])
        nl_cod = Line(nl.n2p(-1), nl.n2p(2), color=COD, stroke_width=8, stroke_opacity=0.6)
        nl_ran = Line(nl.n2p(0), nl.n2p(1), color=RAN, stroke_width=9)

        self.play(Create(ax), FadeIn(labels), FadeIn(xl), FadeIn(yl), run_time=1.2)
        self.play(FadeIn(S1), run_time=0.8)
        self.wait(2.5)

        self.mark("Ex3: domain is a region of the plane")
        self.play(FadeIn(S2), run_time=0.8)
        self.wait(3.0)
        self.play(FadeIn(S3), FadeIn(disk), run_time=1.2)
        self.wait(3.0)

        self.mark("Ex3: test points")
        p1 = Dot(ax.c2p(0, 0), color=YELLOW)
        p2 = Dot(ax.c2p(0.6, 0.8), color=YELLOW)
        p3 = Dot(ax.c2p(1, 1), color=BAD)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(S4), run_time=1.0)
        self.wait(3.0)
        self.play(FadeIn(p3), FadeIn(S5), run_time=1.0)
        self.wait(3.0)

        self.mark("Ex3: range")
        self.play(Create(nl), FadeIn(nl_lab), run_time=0.8)
        self.play(Create(nl_cod), run_time=0.6)
        self.play(FadeIn(S6), Create(nl_ran), run_time=1.2)
        self.wait(5.0)
        self.clear()

    # ----------------------------------------- scene 5: interpretation
    def scene5_interpretation(self):
        self.mark("Scene 5 - Interpretation: same rule, different codomain")
        h = self.heading("Codomain is a choice. Range is a result.")
        nl = NumberLine(x_range=[-4, 4, 1], length=11, include_numbers=False, color=GREY_B).shift(DOWN * 0.3)
        lab0 = T("0", 22, GREY_B).next_to(nl.n2p(0), DOWN, buff=0.15)
        cod = Line(nl.n2p(-4), nl.n2p(4), color=COD, stroke_width=10, stroke_opacity=0.6)
        ran = Line(nl.n2p(0), nl.n2p(4), color=RAN, stroke_width=12)
        t1 = T("f(x) = x\u00b2   with   f : \u211d \u2192 \u211d", 30).shift(UP * 2.0)
        self.play(FadeIn(t1), Create(nl), FadeIn(lab0), run_time=1.0)
        self.play(Create(cod), run_time=1.0)
        c1 = T("Codomain = \u211d  (green)", 28, COD).next_to(nl, UP, buff=0.6).shift(LEFT * 3)
        self.play(FadeIn(c1), run_time=0.6)
        self.play(Create(ran), run_time=1.0)
        c2 = T("Range = [0, \u221e)  (orange)", 28, RAN).next_to(nl, DOWN, buff=0.6).shift(RIGHT * 3)
        self.play(FadeIn(c2), run_time=0.6)
        self.wait(2.5)

        self.mark("Interpretation: shrink codomain to [0, inf)")
        t2 = T("Same rule,   but now   f : \u211d \u2192 [0, \u221e)", 30).shift(UP * 2.0)
        self.play(Transform(t1, t2),
                  cod.animate.put_start_and_end_on(nl.n2p(0), nl.n2p(4)),
                  Transform(c1, T("Codomain = [0, \u221e)", 28, COD).move_to(c1)),
                  run_time=1.5)
        self.wait(1.0)
        cap = self.note(None, "Now every element of the codomain is hit. Range = codomain.", YELLOW_B)
        self.wait(4.0)
        self.clear()

        self.mark("Interpretation: comparison")
        h = self.heading("Putting it together")
        rows = VGroup(
            T("Domain:   the inputs we are allowed to use.", 30, t2c={"Domain": DOM}),
            T("Codomain:   where outputs are declared to land.", 30, t2c={"Codomain": COD}),
            T("Range:   the outputs that actually occur.", 30, t2c={"Range": RAN}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(UP * 0.7)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(1.2)
        rule = T("Range \u2286 Codomain.\nThey are equal only when every element of the codomain is hit.", 28, YELLOW_B)
        rule.next_to(rows, DOWN, buff=0.9)
        self.mark("Interpretation: range is a subset of codomain")
        self.play(FadeIn(rule), run_time=0.8)
        self.wait(5.0)
        self.clear()

    # ------------------------------------------------ scene 6: summary
    def scene6_summary(self):
        self.mark("Scene 6 - Summary")
        h = self.heading("Three takeaways")
        pts = VGroup(
            T("1.  A function gives every input exactly one output.", 28),
            T("2.  Domain = inputs allowed.   Codomain = declared target.", 28),
            T("3.  Range = outputs actually reached, and Range \u2286 Codomain.", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).shift(DOWN * 0.1)
        for p in pts:
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(2.2)
        self.wait(1.5)
        self.clear()

        self.mark("Closing frame: credits and AI disclosure")
        h = T("Credits", 40, weight=BOLD).to_edge(UP, buff=0.5)
        lines = [
            f"Created by {STUDENT_NAME}  ({STUDENT_ID})",
            "Animation: Manim Community Edition (Python)",
            "Voice-over: recorded by the student",
            MUSIC_CREDIT if MUSIC_CREDIT else "Background music: none",
            "AI disclosure: Claude (Anthropic) helped draft the storyboard,",
            "script and Manim code. The mathematics was checked by the student.",
        ]
        g = VGroup(*[T(s, 26, GREY_A) for s in lines]).arrange(DOWN, buff=0.28)
        g.next_to(h, DOWN, buff=0.7)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(g, lag_ratio=0.15), run_time=2.0)
        self.wait(5.0)
        self.play(FadeOut(h), FadeOut(g), run_time=0.8)
