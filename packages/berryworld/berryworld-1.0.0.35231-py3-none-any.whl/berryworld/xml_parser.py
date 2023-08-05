class XMLparser:
    """ Create an XML file according to a certain dictionary """

    def __init__(self, dict_df, main_cat="report", child="records"):
        """ This function takes a DataFrame an stores it as an xml
        :param dict_df: Dictionary of DataFrames as output from the ETL
        :return: None
        """
        self.main_cat = main_cat
        self.child = child
        xml = ""
        for df_key in dict_df.keys():
            aux_xml = "\n".join(dict_df[df_key].apply(self.row_to_xml, axis=1))
            xml += "\n" + "<%s>" % df_key + "\n" + aux_xml + ("\n</%s>" % df_key)
        xml = "\n" + "<%s>" % self.main_cat + "\n" + xml + ("\n</%s>" % self.main_cat)
        self.xml = '<?xml version="1.0" encoding="UTF-8"?>' + xml

    def row_to_xml(self, row):
        """ Convert each row to XML
        :param row: DataFrame row
        :return: Transformed row
        """
        xml = ["<%s>" % self.child]
        for iindex, col_name in enumerate(row.index):
            xml.append(
                "<%s>%s</%s>"
                % (
                    col_name.replace(" ", ""),
                    row.iloc[iindex],
                    col_name.replace(" ", ""),
                    )
                    )
        xml.append("</%s>" % self.child)
        return "\n".join(xml)
