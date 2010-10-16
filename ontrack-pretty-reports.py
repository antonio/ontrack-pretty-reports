from optparse import OptionParser
from xml.dom import minidom, Node

import dateutil.parser

class Record:
    """A single record. A record may be a glucose one, or a medication one"""
    def to_html(self):
        pass

class DailyRecord(list):
    """Glucose level and medication intake in a certain day (list single Record instances)"""
    def to_html(self):
        pass

class Report(dict):
    """Report object. It is simply a dictionary of DailyRecords"""
    def start_html(self):
        """
        Write html report head
        """
        pass

    def end_html(self):
        """Write html report ending
        """
        pass

    def to_html(self):
        """
        Write html report
        """
        self.start_html()
        self.end_html()

def parse_xml_report(input_file):
    """Read the xml file and create the corresponding report

    Arguments:
    - `input_file`: xml input file
    """
    report = Report()
    xml_report = minidom.parse(input_file)
    record_list = xml_report.getElementsByTagName("record")
    for record in record_list:
        r = Record()
        for node in record.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                setattr(r, node.nodeName, node.childNodes[0].nodeValue if node.childNodes else None)
        date = dateutil.parser.parse(r.datetime)
        date_str = date.date().__str__()
        if date_str not in report:
            report[date_str] = DailyRecord()
        dr = report[date_str]
        dr.append(r)
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
    report.to_html()
