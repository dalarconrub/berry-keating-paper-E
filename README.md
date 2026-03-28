# Spectral gap functions bounded below by band-limited functions: a 2D uniqueness phenomenon

**Author:** David Alarcon, Universidad Pablo de Olavide, Sevilla, Spain

**Zenodo DOI:** [10.5281/zenodo.19268994](https://doi.org/10.5281/zenodo.19268994)

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
main.tex              Main manuscript (6 pages)
references.bib        Bibliography (10 references)
cover_letter.tex      Cover letter
figures/
  fig1_lp_bound       V(N) scaling law (20 points, N=20..128)
src/
  01_lp_bound.py              Section 3: LP solver, V(N) = 35.5/N^2
  02_1d_fails.py              Section 4: 1D gives constant bound
  03_band_decomposition.py    Section 5: A+B+C cooperation, ablation
  04_fourier_orthogonality.py Section 6: disjoint supports, sinc(n)=0
  05_relaxation_proof.py      Section 3.2: strict relaxation, V_cont = 0
```

## Compile

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## Companion papers

- **Paper C** — [DOI: 10.5281/zenodo.19267745](https://doi.org/10.5281/zenodo.19267745) — [GitHub](https://github.com/dalarconrub/berry-keating-paper-C)
- **Data & code** — [GitHub](https://github.com/dalarconrub/berry-keating-riemann)

## License

CC BY 4.0
