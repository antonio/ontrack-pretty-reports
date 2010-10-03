from optparse import OptionParser

class Report:
    """Set of daily reports"""
    def to_html(self):
        pass

class DailyReport:
    """Glucose level and medication intake in a certain day"""
    def to_html(self):
        pass

def read_report(xml):
    """Read the xml file and write a pretty html report

    Arguments:
    - `xml`: xml file
    """
    pass

def parse_cli():
    parser = OptionParser()
    parser.add_option("-i", "--input", help="XML input file")
    parser.add_option("-o", "--output", help="HTML output file", default="report.html")
    (options, args) = parser.parse_args()
    if options.input == None :
        print("\nERROR: Please specify an input file\n")
        parser.print_help()
        exit()
    return options

if __name__ == '__main__':
    options = parse_cli()
    # read file and generate a Report
    # Report to_html (foreach DailyReport in Report, to_html)
