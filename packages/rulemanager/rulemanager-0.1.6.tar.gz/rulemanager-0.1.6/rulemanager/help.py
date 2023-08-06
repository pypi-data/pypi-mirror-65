"""
Display of help menu contents and available options

"""
from rulemanager import Colors, PACKAGE

c = Colors()


def help_menu():
    """
    Summary.

        Command line parameter options (Help Menu)

    """
    # formatting
    act = c.ORANGE                         # accent highlight (bright orange)
    bcy = c.BRIGHT_CYAN
    bd = c.BOLD + c.BRIGHT_WHITE           # title formatting
    rst = c.RESET
    lbct = bcy + '[' + rst
    rbct = bcy + ']' + rst
    ctr = bcy + '|' + rst

    menu = '''
                      ''' + bd + PACKAGE + rst + ''' help contents

  ''' + bd + '''DESCRIPTION''' + rst + '''

        Rulemanager is a command line utility used to display, sort,
        and update CloudWatch rules in an AWS Account.

  ''' + bd + '''SYNOPSIS''' + rst + '''

        $ ''' + act + PACKAGE + rst + ' --display ' + lbct + ' --keyword <WORD> ' + rbct + '  ' + ctr + ' ' + ' --set-time <UTCTIME> '  + '''

                         -d, --display
                        [-k, --keyword <value>  ]
                        [-r, --region <value>  ]
                        [-s, --set-time <value>  ]
                        [-d, --debug  ]
                        [-h, --help   ]

  ''' + bd + '''OPTIONS''' + rst + '''

        ''' + bd + '''-D''' + rst + ''', ''' + bd + '''--debug''' + rst + ''': Debugging mode, verbose output for bug tracing.

        ''' + bd + '''-d''' + rst + ''', ''' + bd + '''--display''' + rst + ''': Display all CloudWatch rules in the specified
            AWS region.

        ''' + bd + '''-h''' + rst + ''', ''' + bd + '''--help''' + rst + ''':  Print this help menu and detailed option info.

        ''' + bd + '''-k''' + rst + ''', ''' + bd + '''--keyword''' + rst + ''': CloudWatch rules may be filtered by specifying
            a search keyword that may be found in the rule name.

        ''' + bd + '''-r''' + rst + ''', ''' + bd + '''--region''' + rst + ''': AWS region where a specific CloudWatch rule of
            interest may be found.

        ''' + bd + '''-s''' + rst + ''', ''' + bd + '''--set-time''' + rst + ''': Reset the rule trigger time to a new value.
            All trigger times in UTC timezone.

        ''' + bd + '''-V''' + rst + ''', ''' + bd + '''--version''' + rst + ''': Print app package version and copyright info.
    '''
    print(menu)
    return True
