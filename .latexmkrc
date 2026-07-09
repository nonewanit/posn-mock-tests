# Override system default — use XeLaTeX (required for Thai font)
$pdf_mode = 5;

# XeLaTeX command: generate XDV first
$xelatex = 'xelatex -no-pdf -interaction=nonstopmode %O %S';

# Disable PDF viewer (terminal-only environment)
$pdf_previewer = 'none';
$pdf_update_method = 0;
