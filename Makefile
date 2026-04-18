.PHONY: all full html pdf preview

all:
	quarto render

preview:
	quarto preview --port 8889 src/audience-aware-variation-in-agent-generated-language.qmd

headless:
	quarto preview --port 8889 --no-browser --ip 0.0.0.0 src/audience-aware-variation-in-agent-generated-language.qmd

full/all:
	quarto render --cache-refresh


html:
	quarto render --to html

full/html:
	quarto render --cache-refresh --to html

pdf:
	quarto render --to pdf

full/pdf:
	quarto render --cache-refresh --to pdf

unfreeze:
	rm -rf ./_freeze/
	rm -rf ./.ipynb_checkpoints/
	rm -rf ./src/.ipynb_checkpoints/
