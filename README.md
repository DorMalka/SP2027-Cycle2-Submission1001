# Biometric Authentication Mechanisms: reproduction guide

This repository contains simulation code and numerical results accompanying the paper. There are three reproduction routes:

| Route | LivDet fingerprint images needed? | Java/Maven needed? |
|---|---|---|
| Synthetic uniform, quadratic, and Gaussian simulations | No | No |
| Histogram fitting and downstream optimization from supplied aggregate results | No | No |
| Recompute biometric matching scores from images | Yes, independently authorized access | Yes |

## LivDet access and restrictions

The empirical experiments use the **LivDet 2015 fingerprint dataset, Digital Persona sensor**, with Training and Testing partitions. The fingerprint images are not distributed in this repository.

The authors obtained authorization to use the data for a four-week period. This describes the authors' particular authorization, not a standard access period promised to reviewers. The dataset release agreement itself does not specify a four-week duration. Reviewers must obtain their own approval and follow the conditions and access period granted by the dataset providers; this artifact does not transfer the authors' authorization.

The LivDet release agreement requires a completed, signed request and case-by-case approval. It prohibits redistribution of all or part of the biometric dataset without prior approval from the Principal Investigator, and requires written approval before publishing captured biometric features. It also specifies dataset citation requirements. Therefore, downloading this repository does not provide access to the original fingerprint images or permission to redistribute them.

To request access:

1. Visit the [official LivDet website](https://livdet.org/) and its database/contact information. The site currently lists `livdet@gmail.com` for inquiries.
2. Request the **2015 fingerprint Digital Persona Training and Testing data**, including Live images and the available Fake materials needed below.
3. Complete the providers' release process and obtain authorization before using the images. Ask the providers about any duration, retention, and reuse conditions applicable to your request.

The [CITeR dataset listing](https://github.com/CITeR-Research/Datasets-Liveness-Detection-Competition-Fingerprint-and-Iris) also identifies these datasets as available to researchers under a release agreement. Approval and response time are controlled by the providers.

The signed agreement is not included because it contains identifying information. The aggregate result files support inspection and downstream calculations without distributing fingerprint photographs. Their inclusion does not grant rights to the underlying dataset or establish permission for other forms of data redistribution.

## Environment

Run the commands below from the repository root, using a POSIX shell. Use Python 3.10 or later. The code uses `numpy.trapezoid`, so NumPy 2.0 or later is required. Install the Python dependencies in an isolated environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install 'numpy>=2.0' scipy matplotlib Pillow
export MPLBACKEND=Agg
```

These are dependency requirements inferred from the source, not a pinned record of the original experiment environment. Exact package versions and original hardware/runtime measurements are not supplied. Numerical optimizations can vary with package versions and optimizer settings.

Only the image-to-score route additionally needs a **JDK 17 or later** and **Maven** on `PATH`. The Maven project specifies **SourceAFIS 3.18.1**. Internet access is needed for the initial dependency downloads.

## Output layout and supplied results

The supplied numerical tables are in the root-level `fig_*` directories. Most scripts write new results under `figs/fig_*` instead. Keep these locations distinct when comparing supplied and regenerated results. Scripts can overwrite existing outputs at their destination; use a working copy for reproduction.

Create output directories before running the simulations:

```sh
mkdir -p figs/fig_1continuous_1discrete figs/fig_2continuous \
  figs/fig_uniform figs/fig_parabola figs/fig_different_users_sourceafsi \
  figs/fig_spoofed_users figs/fig_theoretical_k_attempts
```

The `.txt` tables have column headers describing their quantities. Some scripts generate PDF plots directly; others export numerical tables and TikZ/PGFPlots snippets. Producing a complete typeset paper from those snippets is a separate LaTeX step, not performed by the Python commands.

## Route 1: synthetic simulations, without biometric images

```sh
python python_codes/intro_fig.py
python python_codes/uniform_graphs.py
python python_codes/parabolic_graphs.py
python python_codes/1dis1con.py
python python_codes/2contcred_opt.py
python python_codes/theoretical_k_attempt_curves.py
```

| Script | Calculation | Main output directory |
|---|---|---|
| `intro_fig.py` | Illustrative Gaussian densities and FAR/FRR regions | `figs/fig_2continuous/` |
| `uniform_graphs.py` | Uniform distributions, operating curves, and parameter sweeps | `figs/fig_uniform/` |
| `parabolic_graphs.py` | Quadratic distributions and success/threshold comparisons | `figs/fig_parabola/` |
| `1dis1con.py` | One discrete and one continuous credential | `figs/fig_1continuous_1discrete/` |
| `2contcred_opt.py` | Two continuous Gaussian credentials | `figs/fig_2continuous/` |
| `theoretical_k_attempt_curves.py` | Optimized repeated-attempt policies for three distribution families | `figs/fig_theoretical_k_attempts/` |

Most parameters are constants in each script. The theoretical repeated-attempt script also provides command-line options:

```sh
python python_codes/theoretical_k_attempt_curves.py --help
```

For a smaller exploratory run (not the full reported experiment):

```sh
python python_codes/theoretical_k_attempt_curves.py \
  --models uniform --max-k 2 --optimizer-starts 2 --de-maxiter 10
```

## Route 2: reuse supplied aggregate results, without biometric images

Fit distributions to the supplied spoof-score histogram:

```sh
python python_codes/ks_histogram_test.py \
  fig_spoofed_users/livdet_sourceafis_histogram_best_of_probes_data.txt
```

For downstream empirical optimization, first copy the supplied aggregate checkpoint into the location expected by the code:

```sh
cp fig_spoofed_users/psafe_sweep_inputs.npz figs/fig_spoofed_users/
```

This NPZ contains numerical threshold, FAR, FRR, and EER-threshold arrays, not fingerprint images. Then choose the desired analysis:

```sh
# Sweep the discrete credential's safe probability.
python python_codes/fingerprint_scores_spoof.py --sweep-only

# Compare repeated-attempt policies.
python python_codes/fingerprint_scores_spoof.py --attempts-only

# Compare success constraints and conditional mean-attempt limits.
python python_codes/fingerprint_scores_spoof.py --compare-policy-constraints-only
```

These modes use saved empirical inputs and do not rerun SourceAFIS. They reproduce downstream calculations, not the extraction of scores from images. For other policies and optimizer controls:

```sh
python python_codes/fingerprint_scores_spoof.py --help
python python_codes/ks_histogram_test.py --help
```

The full default runs can be computationally expensive; runtime has not been benchmarked for this artifact. Reducing optimizer budgets is useful for a smoke test but is not equivalent to reproducing the reported results.

## Route 3: recompute scores from independently obtained LivDet images

### Build the matcher

```sh
java -version
mvn -version
mvn -f sourceafis-demo/pom.xml -DskipTests compile
```

The Python drivers invoke Maven and `LivDetBatchScorer` themselves when scoring images. Retain `sourceafis-demo/pom.xml` and the Java sources; compiled build folders are unnecessary.

### Prepare images

After obtaining authorization, arrange lossless PNG images under:

```text
sourceafis-demo/livdet_preproc_png/
  Training/Digital_Persona/
    Live/
    Fake/
      Gelatine/
      Woodglue/
      Ecoflex/
      Latex/
  Testing/Digital_Persona/
    Live/
    Fake/
      Gelatine/
      Woodglue/
      Ecoflex/
      Latex/
```

Only populate material directories available in the authorized dataset. Preserve the original partition, material, and filename associations. Filenames must follow the pattern `002_0_5.png`: the first two numeric components identify a fingerprint within a partition, and the last component identifies a sample. Equal numeric identifiers in Training and Testing are treated as separate populations.

`python_codes/livedet_preprocess.py` is a **single-directory PNG re-saving helper**. By default, it reads `data/LivDet 2015/Testing/Digital_Persona/Live/` and writes the corresponding prepared Testing/Live directory. It does not recursively prepare the entire dataset and does not convert non-PNG input files. If using this helper, set `SRC_DIR` and `DST_DIR` for each required Live/material directory and run:

```sh
python python_codes/livedet_preprocess.py
```

If the supplied images use another format, convert them losslessly to PNG while preserving the original pixel data and filename stems. Do not assume the helper has prepared all partitions merely because one invocation succeeded.

### Run the empirical analyses

```sh
# Genuine comparisons and comparisons against other live fingerprints.
python python_codes/sourceafis_scoring.py

# Genuine comparisons and targeted spoof comparisons, followed by the safe-probability sweep.
python python_codes/fingerprint_scores_spoof.py
```

`sourceafis_scoring.py` uses Live images only, with five enrollment probes per eligible fingerprint by default. It considers Training and Testing enrollment populations separately; impostor candidates come from other Training identities. Outputs go to `figs/fig_different_users_sourceafsi/` and its raw-score cache is `sourceafis_livdet_training_live_one_scan_impostor_scores/`.

`fingerprint_scores_spoof.py` uses four probes per eligible fingerprint by default, considers partitions independently, and searches the listed Fake materials within the same partition. It writes aggregate tables, score caches, and `psafe_sweep_inputs.npz` under `figs/fig_spoofed_users/`. Missing materials or different image selections can change the resulting distributions; a successful run alone does not establish an exact match to the paper.

After this full run, the Route 2 policy commands use the newly generated checkpoint. To fit the regenerated histogram:

```sh
python python_codes/ks_histogram_test.py \
  figs/fig_spoofed_users/livdet_sourceafis_histogram_best_of_probes_data.txt
```

The spoof script's `KS_*` constants contain previously fitted parameters; running the fitting script prints results but does not automatically update those constants. The Live-only scoring script intentionally disables its theoretical KS curves pending a fit to its histogram.

## Verification and limitations

Compare regenerated table headers and numerical values with the corresponding supplied root-level `fig_*` tables. Check that all expected cohorts and materials were processed, rather than skipped. Record dependency versions, command-line options, and any edited configuration constants. Exact agreement with every supplied table has not been established by an end-to-end run of this packaged artifact.

The README commands were checked against the source and repository layout. The full empirical workflow requires authorized images, and is not validated merely by the availability of aggregate data. Synthetic simulations and aggregate-data analyses do not require requesting the fingerprint photographs.

Do not include downloaded images, converted images, access credentials, or signed access agreements in a public reproduction package. The repository's ignore rules are not a substitute for checking the files selected for publication.

## Dataset citations

The dataset release agreement requests citations to the LivDet competition publications. See the `LivDet2009`, `LivDet2011`, `LivDet2013`, and `LivDet2015` entries in `main.bib`. The 2015 reference is:

V. Mura, L. Ghiani, G. L. Marcialis, F. Roli, D. A. Yambay, and S. A. Schuckers, "LivDet 2015 fingerprint liveness detection competition 2015," BTAS, 2015, pp. 1-6. DOI: [10.1109/BTAS.2015.7358776](https://doi.org/10.1109/BTAS.2015.7358776).
