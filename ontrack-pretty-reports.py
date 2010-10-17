from optparse import OptionParser
from xml.dom import minidom, Node
from datetime import datetime

import dateutil.parser
import codecs
import ConfigParser

# TODO: Statistics
# TODO: Graphs

class DailyRecord(dict):
    """
    Glucose level and medication intake in a certain day
    """
    def __init__(self, date_str):
        self.date_str = date_str

    def get_record_class(self, config, value):
        """
        Gets the corresponding 'td' class depending on the record value
        Arguments:
        - `config`: configuration
        - `value`: value
        """
        if int(value) in range(int(config.get("limits", "low")), int(config.get("limits", "medium"))):
            return "ok"
        elif int(value) in range(int(config.get("limits", "medium")), int(config.get("limits", "high"))):
            return "warning"
        else:
            return "alert"

    def get_single_record_html(self, config, category, type):
        """
        Return the HTML code  corresponding to the given selection cell
        Arguments:
        - `category`: category of the record. May be one of the following
           * breakfast
           * after_breakfast
           * lunch
           * after_lunch
           * dinner
           * after_dinner
        - `type`: glucose or medication
        """
        if config.get("strings", category) not in self or config.get("strings", type) not in self[config.get("strings", category)]:
            return "<td class='no_value'>-</td>"
        else:
            value = self[config.get("strings", category)][config.get("strings", type)]
            if type == "glucose":
                return "<td class='%s'>%s</td>" % (self.get_record_class(config, value), value)
            else:
                return "<td class='no_value'>%s</td>" % (value)

    def to_html(self, output, config):
        output.write("<tr>")
        output.write("<th scope='row'>" + self.date_str + "</th>")
        output.write(self.get_single_record_html(config, "breakfast", "glucose"))
        output.write(self.get_single_record_html(config, "breakfast", "medication"))
        output.write(self.get_single_record_html(config, "after_breakfast", "glucose"))
        output.write(self.get_single_record_html(config, "lunch", "glucose"))
        output.write(self.get_single_record_html(config, "lunch", "medication"))
        output.write(self.get_single_record_html(config, "after_lunch", "glucose"))
        output.write(self.get_single_record_html(config, "dinner", "glucose"))
        output.write(self.get_single_record_html(config, "dinner", "medication"))
        output.write(self.get_single_record_html(config, "after_dinner", "glucose"))
        output.write("</tr>")

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
      <caption>""" + sorted(self.keys())[0] + " .. " + sorted(self.keys())[-1] +
      """</caption>
      <tbody>
        <tr>
        """)
        output.write("<th scope='col' class='nobg'></th>")
        output.write("<th scope='col'>" + config.get("strings", "breakfast") + "</th>")
        output.write("<th scope='col'>" + config.get("strings", "medication") + "</th>")
        output.write("<th scope='col'>" + config.get("strings", "after_breakfast") + "</th>")
        output.write("<th scope='col'>" + config.get("strings", "lunch") + "</th>")
        output.write("<th scope='col'>" + config.get("strings", "medication") + "</th>")
        output.write("<th scope='col'>" + config.get("strings", "after_lunch") + "</th>")
        output.write("<th scope='col'>" + config.get("strings", "dinner") + "</th>")
        output.write("<th scope='col'>" + config.get("strings", "medication") + "</th>")
        output.write("<th scope='col'>" + config.get("strings", "after_dinner") + "</th>")
        output.write("</tr>")


    def end_html(self, output):
        """
        Write html report ending
        """
        output.write("</tbody>\n")
        output.write("</body>\n")
        output.write("</html>")

    def to_html(self, file_out, config):
        """
        Write html report
        """
        try:
            output = codecs.open(file_out, "w", "utf8")
            self.start_html(output)
            for day in sorted(self.keys()):
                self[day].to_html(output, config)
            self.end_html(output)
            output.close()
        except RuntimeError:
            print "Error writing to file %s" % (file_out)

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
    parser.add_option("-c", "--config", help="Configuration file", default="config")
    (options, args) = parser.parse_args()
    if options.input == None :
        print("\nERROR: Please specify an input file\n")
        parser.print_help()
        exit()
    return options

if __name__ == '__main__':
    options = parse_options()
    config = ConfigParser.SafeConfigParser()
    try:
        config.readfp(codecs.open(options.config, "r", "utf8"))
    except IOError:
        print "Error reading configuration file"
    report = parse_xml_report(options.input)
    report.to_html(options.output, config)
