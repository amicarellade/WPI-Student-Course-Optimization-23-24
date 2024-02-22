import tabula

# Read PDF into list of DataFrame
aero = tabula.io.read_pdf("electrical-and-computer-engineering-major.pdf", pages='all')

# Read remote PDF into list of DataFrame
#dataframe_2 = tabula.read_pdf("https://github.com/tabulapdf/tabula-java/raw/master/src/test/resources/technology/tabula/arabic.pdf")

# Convert PDF into CSV file
#tabula.convert_into("input.pdf", "output.csv", output_format="csv", pages='all')

print(aero)
