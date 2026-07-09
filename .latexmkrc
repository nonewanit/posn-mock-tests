# Build with XeLaTeX (required for Thai font via fontspec)
$xelatex = 'xelatex -no-pdf -interaction=nonstopmode %O %S';
$pdf_mode = 5;  # xdvipdfmx
$out_dir = '.';