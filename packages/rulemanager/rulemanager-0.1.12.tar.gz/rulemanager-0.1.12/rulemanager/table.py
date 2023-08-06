"""
Table Generation Module:
    - Constructs table of data
    - Displays table with appropriate cli positioning

Module Functions:
    - setup_table:
        Main module function controller for constructing a table of data
    - display_table:
        renders VeryPrettyTable table to cli stdout
    - print_header:
        Separate module function for contructing the table title row (first row)
    - _postprocessing:
        Facility for initating any post-table construction operations
"""

import os
import sys
import inspect
import unicodedata

# 3rd party
from veryprettytable import VeryPrettyTable
from cron_descriptor import get_description, ExpressionDescriptor
from libtools.js import export_iterobject
from libtools import stdout_message, logd, Colors


c = Colors()


try:
    from libtools.oscodes_unix import exit_codes
    os_type = 'Linux'
    splitchar = '/'                             # character for splitting paths (linux)
    text = c.BRIGHT_CYAN
except Exception:
    from libtools.oscodes_win import exit_codes    # non-specific os-safe codes
    os_type = 'Windows'
    splitchar = '\\'                            # character for splitting paths (windows)
    text = c.CYAN


# universal colors; unicode symbols
yl = c.YELLOW + c.BOLD
fs = c.GOLD3
bd = c.BOLD
titlec = c.BRIGHT_WHITE
gn = c.BRIGHT_GREEN
btext = text + c.BOLD
bdwt = c.BOLD + c.BRIGHT_WHITE
dgray = c.DARK_GRAY1
frame = text
ub = c.UNBOLD
bullet = unicodedata.lookup('bullet')
rst = c.RESET


tablespec = {
    'border': True,
    'header': True,
    'padding': 2,
    'field_max_width': 70
}

column_widths = {
    'name': 31,
    'expression': 36,
    'state': 8,
    'arn': 70
}


def display_table(table, tabspaces=4):
    """
    Print Table Object offset from left by tabspaces
    """
    indent = ('\t').expandtabs(tabspaces)
    table_str = table.get_string()
    for e in table_str.split('\n'):
        print(indent + frame + e)
    sys.stdout.write(Colors.RESET + '\n\n')
    return True


def print_header(title, indent=4, spacing=4):
    """
    Paints title header grid of a vpt Table
    """
    divbar = frame + '-'
    upbar = frame + '|' + rst
    ltab = '\t'.expandtabs(indent)              # lhs indentation of title bar
    spac = '\t'.expandtabs(7)                   # rhs indentation of legend from divider bar
    tab3 = '\t'.expandtabs(3)                   # space between legend items
    tab4 = '\t'.expandtabs(4)                   # space between legend items
    tab5 = '\t'.expandtabs(5)                   # space between legend items
    tab6 = '\t'.expandtabs(6)                   # space between legend items
    # output header
    print('\n\n')
    print(tab4, end='')
    print(divbar * 91, end='\n')
    print(tab4 + '|' + ' ' * 89 + '|', end='\n')
    print('{}{}'.format(tab4 + '|' + tab3 * 5, title))
    print(tab4 + upbar + rst + ' ' + tab3 * 29 + frame + ' |' + rst)
    return True


def spacing(days):
    s = ''
    for digit in str(days):
        s = s + ' '
    return s


def _postprocessing():
    return True


def setup_table(rule_list, aws_account, rgn):
    """
    Renders Table containing data elements via cli stdout
    """
    # guarding clause in case no cw rules in region
    if len(rule_list) < 1:
        msg = 'No CloudWatch rules found in region {} of AWS Account {}.'.format(rgn, aws_account)
        stdout_message(msg)
        return _postprocessing()

    # setup table
    x = VeryPrettyTable(
            border=tablespec['border'],
            header=tablespec['header'],
            padding_width=tablespec['padding']
        )

    title_cell1 = '           Rule Name'              # forward leading spaces req to center title
    title_cell2 = '       Trigger Frequency (UTC)'
    title_cell3 = 'State'

    x.field_names = [
        titlec + title_cell1 + frame,
        titlec + title_cell2 + frame,
        titlec + title_cell3 + frame,
    ]

    # cell max width
    x.max_width[titlec + title_cell1 + frame] = column_widths['name']
    x.max_width[titlec + title_cell2 + frame] = column_widths['expression']
    x.max_width[titlec + title_cell3 + frame] = column_widths['state']

    # cell min = max width
    x.min_width[titlec + title_cell1 + frame] = column_widths['name']
    x.min_width[titlec + title_cell2 + frame] = column_widths['expression']
    x.min_width[titlec + title_cell3 + frame] = column_widths['state']

    # cell alignment
    x.align[titlec + title_cell1 + frame] = 'l'
    x.align[titlec + title_cell2 + frame] = 'l'
    x.align[titlec + title_cell3  + frame] = 'c'

    for rule in rule_list:

        try:

            # convert cron expression to human-readable
            root = str(ExpressionDescriptor(rule['ScheduleExpression'][5:-2]))

            # prepend to expression root if daily event
            expression = 'Daily ' + root if (len(root) == 11) and ('At' in root) else root

        except Exception:
            expression = rule['ScheduleExpression'] if rule.get('ScheduleExpression') else 'N/A'

        # populate table
        rule_name = rule['Name'] if len(rule['Name']) < 29 else rule['Name'][:28]
        rule_expression = c.BOLD + c.BRIGHT_WHITE + expression + rst
        rule_state = (c.BRIGHT_GREEN if rule['State'] == 'ENABLED' else c.RED) + rule['State'] + rst

        x.add_row(
            [
                rst + ' ' + c.ORANGE +  bullet + ' ' + c.BRIGHT_BLUE + rule_name + rst + frame,
                rst + c.ORANGE + bullet + ' ' + rule_expression + frame,
                rst + rule_state + frame,
            ]
        )

    # Table
    account = aws_account
    vtab_int = 10
    vtab = '\t'.expandtabs(vtab_int)
    init = rst + bd + frame
    acct = rst + account + frame
    rgn_c = rst + rgn + frame
    bar =  ' ' + vtab
    msg = '{}CloudWatch Rules | {}AWS ACcount: {}, Region: {}{}|{}'.format(init, ub, acct, rgn_c, bar, rst)
    print_header(title=msg, indent=10, spacing=vtab_int)
    display_table(x, tabspaces=4)
    return _postprocessing()
