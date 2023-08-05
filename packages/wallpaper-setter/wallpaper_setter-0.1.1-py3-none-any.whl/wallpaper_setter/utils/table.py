from easy_table import EasyTable

def get_table():
    table = EasyTable("Table")
    table.setCorners("", "", "", "")
    table.setOuterStructure("", "")
    table.setInnerStructure("│", "─", "┼")

    return table
