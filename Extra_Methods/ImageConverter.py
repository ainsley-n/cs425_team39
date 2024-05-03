#This segment of code was found in various locations in the Lcapy package.
#This is an extracted helper function that converts a LaTeX string to a PNG image.

from lcapy.system import tmpfilename, LatexRunner, PDFConverter

def get_latex_file(s, tex_filename):
    # Need amsmath for operatorname
    template = ('\\documentclass[a4paper, margin=1mm, varwidth]{standalone}\n'
                '\\usepackage{amsmath}\n'
                '\\begin{document}\n$%s$\n'
                '\\end{document}\n')
    content = template % s

    open(tex_filename, 'w').write(content)
    return tex_filename

def get_pdf_file(tex_filename, pdf_filename):
    pdf_filename = tex_filename.replace('.tex', '.pdf')
    latexrunner = LatexRunner()
    latexrunner.run(tex_filename)
    return pdf_filename

def get_png_file(pdf_filename, png_filename):
    pdfconverter = PDFConverter()
    pdfconverter.to_png(pdf_filename, png_filename, dpi=300)
    return png_filename

def latex_to_png(s, png_filename = None):
    tex_filename = tmpfilename('.tex')
    tex_filename = get_latex_file(s, tex_filename)
    pdf_filename = tex_filename.replace('.tex', '.pdf')
    pdf_filename = get_pdf_file(tex_filename, pdf_filename)

    if png_filename is None:
        png_filename = "temp/temp.png"
    png_filename = get_png_file(pdf_filename, png_filename)
    latexrunner = LatexRunner()
    latexrunner.cleanup(tex_filename, pdf_filename)

    return pdf_filename