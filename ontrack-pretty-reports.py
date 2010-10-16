from optparse import OptionParser
from xml.dom import minidom, Node
from datetime import datetime

import dateutil.parser

class DailyRecord(dict):
    """
    Glucose level and medication intake in a certain day
    """
    def __init__(self, date_str):
        self.date_str = date_str

    def to_html(self, output):
        print self.date_str

class Report(dict):
    """
    Report object. It is simply a dictionary of DailyRecords
    """
    def start_html(self, output):
        """
        Write html report head
        """
        output.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es-ES" lang="es-ES">
  <head>
    <title>Diabetes Report - """ + datetime.now().__str__() + """</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <link rel="stylesheet" href="css/styles.css" type="text/css" media="screen" />

    <script src="js/jquery-1.4.2.min.js" type="text/javascript" charset="utf-8"></script>
    <script src="js/jquery.scrollTo.min.js" type="text/javascript" charset="utf-8"></script>
    <script src="js/main.js" type="text/javascript" charset="utf-8"></script>
  </head>
  <body>
    <table cellspacing="0">
      <caption>""" + sorted(self.keys())[0] + " - " + sorted(self.keys())[-1] +
      """</caption>
      <tbody>
      """)

    def end_html(self, output):
        """
        Write html report ending
        """
        output.write("</tbody>\n")
        output.write("</body>\n")
        output.write("</html>")

    def to_html(self, file_out):
        """
        Write html report
        """
        try:
            output = open(file_out, "w")
            self.start_html(output)
            for day in sorted(self.keys()):
                self[day].to_html(output)
            self.end_html(output)
            output.close()
        except RuntimeError as e:
            print "Error writing to file %s" % (file_out)
            print e

def parse_xml_report(input_file):
    """
    Read the xml file and create the corresponding report

    Arguments:
    - `input_file`: xml input file
    """
    report = Report()
    xml_report = minidom.parse(input_file)
    record_list = xml_report.getElementsByTagName("record")
    for item in record_list:
        r = {}
        for node in item.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                r[node.nodeName] = node.childNodes[0].nodeValue if node.childNodes else None
        date = dateutil.parser.parse(r["datetime"])
        date_str = date.date().__str__()
        if date_str not in report:
            report[date_str] = DailyRecord(date_str)
        dr = report[date_str]

        r_category = r["category"]
        r_type = r["type"]
        r_value = r["value"]

        if r_category not in dr:
            dr[r_category] = {}
        dr[r_category][r_type] = r_value

    return report

def parse_options():
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
    options = parse_options()
    report = parse_xml_report(options.input)
    report.to_html(options.output)
