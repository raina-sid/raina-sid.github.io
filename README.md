# raina-sid.github.io

Personal writing site — LLM evaluation, model audit, measurement validity.
Built with [Quarto](https://quarto.org), served by GitHub Pages from the `gh-pages` branch.

Quarto installed to a user-local path, so it may not be on `PATH` in a fresh shell:

```bash
export PATH="$HOME/Applications/quarto/bin:$PATH"   # add to ~/.zshrc to make permanent
quarto --version                                     # 1.10.18

quarto preview          # local, live-reloading
quarto render           # build to _site/
quarto publish gh-pages # build + push to the gh-pages branch
```

Posts live in `posts/`. Bibliography support is pre-configured — add
`bibliography: references.bib` to a post's front matter and cite with `[@key]`.
