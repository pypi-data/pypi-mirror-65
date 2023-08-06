#!/usr/bin/env bash

# GPL v3 License
#
# Copyright (c) 2018-2020 Blake Huber
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


function _complete_4_horsemen_commands(){
    local cmds="$1"
    local split='5'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_4_horsemen_commands -->
}


function _complete_4_horsemen_subcommands(){
    local cmds="$1"
    local split='3'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_4_horsemen_subcommands -->
}


function _complete_profile_subcommands(){
    local cmds="$1"
    local split='7'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_profile_subcommands -->
}


function _complete_region_subcommands(){
    local cmds="$1"
    local split='6'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_region_subcommands -->
}


function _complete_rulemanager_commands(){
    local cmds="$1"
    local split='6'       # times to split screen width
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${COMP_WORDS[1]}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_rulemanager_commands -->
}


function _complete_settime_subcommands(){
    ##
    ##  $ buildpy --download <subcommands>
    ##
    local IFS=$' \t\n'
    local subcmds="$1"
    local split='3'       # times to split screen width
    declare -a formatted_cmds=( $(compgen -W "${subcmds}" -- ${cur}) )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_buildpy_commands -->
}


function _cron_expressions_am(){
    ##
    ##  Construct Cloudwatch rule schedule expressions
    ##
    declare -a arr_subcmds

    for hour in $(seq 0 11); do
        if [[ ${#hour} -lt 2 ]]; then
            time="0${hour}00-AM"
        else
            time="${hour}00-AM"
        fi
        arr_subcmds=( "${arr_subcmds[@]}"  "' '${time}" )
    done
    printf -- '%s' "${arr_subcmds[@]}"
}


function _cron_expressions_pm(){
    ##
    ##  Construct Cloudwatch rule schedule expressions
    ##
    declare -a arr_subcmds

    for hour in $(seq 12 23); do
        time="${hour}00-PM"
        arr_subcmds=( "${arr_subcmds[@]}"  "' '${time}" )
    done
    printf -- '%s' "${arr_subcmds[@]}"
}


# 24 hour cron times
declare -a _cron_accumulator=(

        $(_cron_expressions_am)
        $(_cron_expressions_pm)


    )


function _numargs(){
    ##
    ## Returns count of number of parameter args passed
    ##
    local parameters="$1"
    local numargs=0

    if [[ ! "$parameters" ]]; then
        printf -- '%s\n' "0"
    else
        for i in $(echo $parameters); do
            numargs=$(( $numargs + 1 ))
        done
        printf -- '%s\n' "$numargs"
    fi
    return 0
    #
    # <-- end function _numargs -->
}


function _parse_compwords(){
    ##
    ##  Interogate compwords to discover which of the  5 horsemen are missing
    ##
    compwords=("${!1}")
    four=("${!2}")

    declare -a missing_words

    # Remove mutually exclusive entries
    if [[ "$(echo "${compwords[@]}" | grep "\-\-enable")" ]]; then
        delete=( '--disable' '--view' '--set-time' )
        for target in "${delete[@]}"; do
            for i in "${!four[@]}"; do
                if [[ ${four[i]} = "$target" ]]; then
                    unset "four[i]"
                fi
            done
        done

    elif [[ "$(echo "${compwords[@]}" | grep "\-\-disable")" ]]; then
        delete=( '--enable' '--view' '--set-time' )
        for target in "${delete[@]}"; do
            for i in "${!four[@]}"; do
                if [[ ${four[i]} = "$target" ]]; then
                    unset "four[i]"
                fi
            done
        done

    elif [[ "$(echo "${compwords[@]}" | grep "\-\-view")" ]]; then
        delete=( '--enable' '--disable' '--set-time' )
        for target in "${delete[@]}"; do
            for i in "${!four[@]}"; do
                if [[ ${four[i]} = "$target" ]]; then
                    unset "four[i]"
                fi
            done
        done

    elif [[ "$(echo "${compwords[@]}" | grep "\-\-set-time")" ]]; then
        delete=( '--enable' '--disable' '--view' )
        for target in "${delete[@]}"; do
            for i in "${!four[@]}"; do
                if [[ ${four[i]} = "$target" ]]; then
                    unset "four[i]"
                fi
            done
        done

    fi

    # Find & return missing members in compwords
    for key in "${four[@]}"; do
        if [[ ! "$(echo "${compwords[@]}" | grep ${key##*-})" ]]; then
            missing_words=( "${missing_words[@]}" "$key" )
        fi
    done
    printf -- '%s\n' "${missing_words[@]}"
    #
    # <-- end function _parse_compwords -->
}


function _rulemanager_completions(){
    ##
    ##  Completion structures for xlines exectuable
    ##
    local commands                  #  commandline parameters (--*)
    local subcommands               #  subcommands are parameters provided after a command
    local numargs                   #  num arg words: integer count of number of commands, subcommands
    local cur                       #  completion word at index position 0 in COMP_WORDS array
    local prev                      #  completion word at index position -1 in COMP_WORDS array
    local initcmd                   #  completion word at index position -2 in COMP_WORDS array

    config_dir="$HOME/.config/rulemanager"
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    initcmd="${COMP_WORDS[COMP_CWORD-2]}"

    # initialize vars
    COMPREPLY=()
    numargs="${#COMP_WORDS[@]}"

    options='--help --keyword --profile --region --debug --version'
    commands='--enable --disable --set-time --view'

    case "${initcmd}" in

        '--keyword')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--enable' '--disable' '--profile' '--region' '--set-time' '--view' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

        '--profile')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--debug' '--enable' '--disable' '--region' '--set-time' '--view' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

        '--region')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--debug' '--enable' '--disable' '--profile' '--set-time' '--view' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

        '--set-time')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--debug' '--keyword' '--profile' '--region')
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

    esac
    case "${cur}" in

        '--h'*)
            COMPREPLY=( $(compgen -W '--help' -- ${cur}) )
            return 0
            ;;

        '--e'*)
            COMPREPLY=( $(compgen -W '--enable' -- ${cur}) )
            return 0
            ;;

        '--d'*)
            COMPREPLY=( $(compgen -W '--disable' -- ${cur}) )
            return 0
            ;;

        '--k'*)
            COMPREPLY=( $(compgen -W '--keyword' -- ${cur}) )
            return 0
            ;;

        '--p'*)
            COMPREPLY=( $(compgen -W '--profile' -- ${cur}) )
            return 0
            ;;

        '--r'*)
            COMPREPLY=( $(compgen -W '--region' -- ${cur}) )
            return 0
            ;;

        '--s'*)
            COMPREPLY=( $(compgen -W '--set-time' -- ${cur}) )
            return 0
            ;;

        '--vi'*)
            COMPREPLY=( $(compgen -W '--view' -- ${cur}) )
            return 0
            ;;

        '--ve'*)
            COMPREPLY=( $(compgen -W '--version' -- ${cur}) )
            return 0
            ;;

        'rule'*)
            COMPREPLY=( $(compgen -W 'rulemanager' -- ${cur}) )
            return 0
            ;;

        '00'*)
            COMPREPLY=( $(compgen -W '0000-AM' -- ${cur}) )
            return 0
            ;;

        '01'*)
            COMPREPLY=( $(compgen -W '0100-AM' -- ${cur}) )
            return 0
            ;;

        '02'*)
            COMPREPLY=( $(compgen -W '0200-AM' -- ${cur}) )
            return 0
            ;;

        '03'*)
            COMPREPLY=( $(compgen -W '0300-AM' -- ${cur}) )
            return 0
            ;;

        '04'*)
            COMPREPLY=( $(compgen -W '0400-AM' -- ${cur}) )
            return 0
            ;;

        '05'*)
            COMPREPLY=( $(compgen -W '0500-AM' -- ${cur}) )
            return 0
            ;;

        '06'*)
            COMPREPLY=( $(compgen -W '0600-AM' -- ${cur}) )
            return 0
            ;;

        '07'*)
            COMPREPLY=( $(compgen -W '0700-AM' -- ${cur}) )
            return 0
            ;;

        '08'*)
            COMPREPLY=( $(compgen -W '0800-AM' -- ${cur}) )
            return 0
            ;;

        '09'*)
            COMPREPLY=( $(compgen -W '0900-AM' -- ${cur}) )
            return 0
            ;;

        '10'*)
            COMPREPLY=( $(compgen -W '1000-AM' -- ${cur}) )
            return 0
            ;;

        '11'*)
            COMPREPLY=( $(compgen -W '1100-AM' -- ${cur}) )
            return 0
            ;;

        '12'*)
            COMPREPLY=( $(compgen -W '1200-AM' -- ${cur}) )
            return 0
            ;;

        '13'*)
            COMPREPLY=( $(compgen -W '1300-PM' -- ${cur}) )
            return 0
            ;;

        '14'*)
            COMPREPLY=( $(compgen -W '1400-PM' -- ${cur}) )
            return 0
            ;;

        '15'*)
            COMPREPLY=( $(compgen -W '1500-PM' -- ${cur}) )
            return 0
            ;;

        '16'*)
            COMPREPLY=( $(compgen -W '1600-PM' -- ${cur}) )
            return 0
            ;;

        '17'*)
            COMPREPLY=( $(compgen -W '1700-PM' -- ${cur}) )
            return 0
            ;;

        '18'*)
            COMPREPLY=( $(compgen -W '1800-PM' -- ${cur}) )
            return 0
            ;;

        '19'*)
            COMPREPLY=( $(compgen -W '1900-PM' -- ${cur}) )
            return 0
            ;;

        '20'*)
            COMPREPLY=( $(compgen -W '2000-PM' -- ${cur}) )
            return 0
            ;;

        '21'*)
            COMPREPLY=( $(compgen -W '2100-PM' -- ${cur}) )
            return 0
            ;;

        '22'*)
            COMPREPLY=( $(compgen -W '2200-PM' -- ${cur}) )
            return 0
            ;;

        '23'*)
            COMPREPLY=( $(compgen -W '2300-PM' -- ${cur}) )
            return 0
            ;;

    esac
    case "${prev}" in

        '--debug' | '--help' | '--keyword' | '--version')
            return 0
            ;;

        '--enable')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--debug' '--keyword' '--profile' '--region' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

        '--disable')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--debug' '--keyword' '--profile' '--region'  )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

        '--view')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--keyword' '--profile' '--region' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

        '--profile')
            python3=$(which python3)
            iam_users=$($python3 "$config_dir/iam_identities.py")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ]; then
                # display full completion subcommands
                _complete_profile_subcommands "${iam_users}"
            else
                COMPREPLY=( $(compgen -W "${iam_users}" -- ${cur}) )
            fi
            return 0
            ;;

        '--set-time')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            expressions=$(echo "${_cron_accumulator[@]}")
            _complete_settime_subcommands "${expressions}"
            return 0
            ;;

        "[0-9][0-9]-AM" | "[0-9][0-9]-PM" | 'cron'*)
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--debug' '--keyword' '--profile' '--region' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

        '--region' | "--re*")
            ##  complete AWS region codes
            python3=$(which python3)
            regions=$($python3 "$config_dir/regions.py")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ]; then

                _complete_region_subcommands "${regions}"

            else
                COMPREPLY=( $(compgen -W "${regions}" -- ${cur}) )
            fi
            return 0
            ;;

        'rulemanager')
            if [ "$cur" = "" ] || [ "$cur" = "--" ]; then

                _complete_rulemanager_commands "${commands} ${options}"
                return 0

            fi
            ;;

    esac

    COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )

} && complete -F _rulemanager_completions rulemanager
