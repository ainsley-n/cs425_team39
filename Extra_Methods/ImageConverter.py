#This segment of code was found in various locations in the Lcapy package.
#This is an extracted helper function that converts a LaTeX string to a PNG image.

from lcapy.system import tmpfilename, LatexRunner, PDFConverter

def latex_to_png(s, png_filename):
    tex_filename = tmpfilename('.tex')
    # Need amsmath for operatorname
    template = ('\\documentclass[a4paper]{standalone}\n'
                '\\usepackage{amsmath}\n'
                '\\begin{document}\n$%s$\n'
                '\\end{document}\n')
    content = template % s

    open(tex_filename, 'w').write(content)
    pdf_filename = tex_filename.replace('.tex', '.pdf')
    latexrunner = LatexRunner()
    latexrunner.run(tex_filename)

    pdfconverter = PDFConverter()
    if png_filename is None:
        png_filename = "temp/temp.png"
    pdfconverter.to_png(pdf_filename, png_filename, dpi=300)
    latexrunner.cleanup(tex_filename, pdf_filename)

    return pdf_filename