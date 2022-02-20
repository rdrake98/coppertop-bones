// PGM course example - we can capture unconditional PMF with a dictionary and conditional PMF with a table
from my_first_bones.lang uses __all__       // defines op+, op-, op*, op/, tNum, tStr, tRmu, tUnary, tBinary, tAny in global scope
from db_bones.lang.types uses tProb
from db_bones.lang.inspect uses meta
from db_bones.pgm uses BayesNet
from std_bones.bones.stdio uses stdout :cout

difficulty:   `d0`d1 ! (0.6;0.4)<:prob>
intelligence: `i0`i1 ! (0.7;0.3)<:prob>
sat: ([int: `i0`i1]
    s0: (0.95;0.2)<:prob>,
    s1: (0.05;0.8)<:prob>
)
grade: ([intDiff: (`i0`d0;`i0`d1;`i1`d0;`i1`d1)]
    gA: (0.3;0.05;0.9;0.5)<:prob>,
    gB: (0.4;0.25;0.08;0.3)<:prob>,
    gC: (0.3;0.7;0.02;0.2)<:prob>
)
letter: ([grd: `gA`gB`gC]
    l0: (0.1;0.4;0.99)<:prob>,
    l1: (0.9;0.6;0.01)<:prob>
)

sat meta >> cout
difficulty meta >> cout                  // >> is a noun pipe     b >> a is same as a op>>(b), i.e. cout (difficulty meta)
1.0 meta >> cout
1.0<:height> meta >> cout

P: {[d,i,s,g,l] difficulty(d) * intelligence(i) * sat(i)(s) * grade(i;d)(g) * letter(g)(l)}

difficulty(`d0) * intelligence(`i0) * sat(`i0)(`s0) * grade(`i0`d0)(`gA) * letter(`gA)(`l0) \
    assert(P(`d0,`i0,`s0,`gA,`l0))

BayesNet(difficulty;intelligence;sat;grade;letter).P(`d0,`i0,`s0,`gA,`l0) >> cout


difficulty:   ([D:`d0`d1] P:(0.60,0.40)<:prob>)
intelligence: ([I:`i0`i1] P:(0.70,0.30)<:prob>)
sat:          ([I:`i0`i0`i1`i1, S:`s0`s1`s0`s1] P:(0.95,0.05,0.20,0.80)<:prob>)
grade:        (
    [
        I: `i0`i0`i1`i1`i0`i0`i1`i1`i0`i0`i1`i1,
        D: `d0`d1`d0`d1`d0`d1`d0`d1`d0`d1`d0`d1,
        G: `gA`gA`gA`gA`gB`gB`gB`gB`gC`gC`gC`gC
    ]
    P: (0.3;0.05;0.9;0.5;0.4;0.25;0.08;0.3;0.3;0.7;0.02;0.2)<:prob>
)
letter:       (
    [G:`gA`gB`gC`gA`gB`gC L:`l0`l0`l0`l1`l1`l1]
    P: (0.10;0.40;0.99;0.90;0.60;0.01)<:prob>
)
net = BayesNet(difficulty;intelligence;sat;grade;letter)
net >> cout
net P(`d0,`i0,`s0,`gA,`l0) >> cout
net pmfGiven(`D, `I)
net pGiven(`d1, `i0)

