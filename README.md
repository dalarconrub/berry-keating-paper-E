# Spectral gap functions bounded below by band-limited functions: a 2D uniqueness phenomenon

**Author:** David Alarcon, Universidad Pablo de Olavide, Sevilla, Spain

**Venue:** Journal of Fourier Analysis and Applications (Springer)

## Abstract

We study functions h on R^2 whose Fourier transform is supported outside
the unit square and which satisfy the one-sided bound h >= -g, where g is
a fixed non-negative band-limited function. Using linear programming, we
show that all bounded linear functionals of h vanish, forcing h = 0 in L^1.
The result is genuinely two-dimensional: the 1D analogue admits nontrivial
solutions. Applications to determinantal point processes and the Riemann
Hypothesis are discussed.

## Repository structure

```
main.tex              Main manuscript (~10 pages)
references.bib        Bibliography (10 references)
figures/
  fig1_lp_bound       V(N) scaling law (20 points, N=20..128)
src/
  (scripts to be added)
```

## Compile

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## Key result

V(N) = 35.5/N^2 (CV = 0.5%, R^2 = 0.9997, alpha = 1.991)

This is a pure result in Fourier analysis, independent of number theory.
The application to RH is developed in the companion paper (Paper C).

## License

CC BY 4.0
