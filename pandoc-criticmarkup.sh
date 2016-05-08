#!/bin/bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# getopts

## reset getopts
OPTIND=1

## Initialize parameters
accept=false
reject=false
permanent=false
output_EXT=''

## get the options
while getopts "arpd:" opt; do
	case "$opt" in
	a)  accept=true
		;;
	r)  reject=true
		;;
	p)  permanent=true
		;;
	d)  output_EXT=$OPTARG
		;;
	esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

## check output_EXT
if [ "$output_EXT" != '' ] && [ "$output_EXT" != "html" ] && [ "$output_EXT" != "latex" ] && [ "$output_EXT" != "pdf" ]; then
	echo "Output format should be either html or latex/pdf."
	exit 1
fi

# preparation

## get the content of the file
CONTENT=$(<$@)

# cooking the result

## if d then show diff (CriticMarkup)
if [ "$output_EXT" = "html" ] || [ "$output_EXT" = "latex" ] || [ "$output_EXT" = "pdf" ]; then
### if html then show CriticMarkup in html
	if [ "$output_EXT" = "html" ]; then
		#### sub
		CONTENT=$(echo "$CONTENT" | sed -e s/'~~}'/'<\/ins>'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'{~~'/'<del>'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'~>'/'<\/del><ins>'/g)
		#### del
		CONTENT=$(echo "$CONTENT" | sed -e s/'{--'/'<del>'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'--}'/'<\/del>'/g)
		#### ins
		CONTENT=$(echo "$CONTENT" | sed -e s/'{++'/'<ins>'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'++}'/'<\/ins>'/g)
		#### mark
		CONTENT=$(echo "$CONTENT" | sed -e s/'{=='/'<mark>'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'==}'/'<\/mark>'/g)
		#### comment
		CONTENT=$(echo "$CONTENT" | sed -e s/'{>>'/'<aside>'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'<<}'/'<\/aside>'/g)
### else (latex/pdf) then show CriticMarkup in latex
	else
		#### sub
		CONTENT=$(echo "$CONTENT" | sed -e s/'~~}'/'}'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'{~~'/'\\st{'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'~>'/'}\\underline{'/g)
		#### del
		CONTENT=$(echo "$CONTENT" | sed -e s/'{--'/'\\st{'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'--}'/'}'/g)
		#### ins
		CONTENT=$(echo "$CONTENT" | sed -e s/'{++'/'\\underline{'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'++}'/'}'/g)
		#### mark
		CONTENT=$(echo "$CONTENT" | sed -e s/'{=='/'\\hl{'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'==}'/'}'/g)
		#### comment
		CONTENT=$(echo "$CONTENT" | sed -e s/'{>>'/'\\marginpar{'/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'<<}'/'}'/g)
## else (not d, not showing CriticMarkup)
	fi
else
### if r or a then remove highlights and archive comments
	if [ $reject = true ] || [ $accept = true ]; then
		#### mark
		CONTENT=$(echo "$CONTENT" | sed -e s/'{=='/''/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'==}'/''/g)
		#### comment
		CONTENT=$(echo "$CONTENT" | sed -e s/'{>>'/'<\!-- '/g)
		CONTENT=$(echo "$CONTENT" | sed -e s/'<<}'/' -->'/g)
#### if r then reject
		if [ $reject = true ]; then
			CONTENT=$(./criticmarkup-reject.py "$CONTENT")
#### else (a then accept)
		else
			CONTENT=$(./criticmarkup-accept.py "$CONTENT")
		fi
	fi
fi

# output
if [ $permanent = false ]; then
	echo "$CONTENT"
else
	echo "$CONTENT" > "$@"
fi