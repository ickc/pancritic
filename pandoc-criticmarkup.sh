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
CONTENT=$(<"$@")

# cooking the result

## if d then show diff (CriticMarkup)
if [ "$output_EXT" = "html" ] || [ "$output_EXT" = "latex" ] || [ "$output_EXT" = "pdf" ]; then
### if html then show CriticMarkup in html (sub, del, ins, mark, comment)
	if [ "$output_EXT" = "html" ]; then
		CONTENT=$(echo "$CONTENT" | sed \
			-e s/'~~}'/'<\/ins>'/g \
			-e s/'{~~'/'<del>'/g \
			-e s/'~>'/'<\/del><ins>'/g \
			-e s/'{--'/'<del>'/g \
			-e s/'--}'/'<\/del>'/g \
			-e s/'{++'/'<ins>'/g \
			-e s/'++}'/'<\/ins>'/g \
			-e s/'{=='/'<mark>'/g \
			-e s/'==}'/'<\/mark>'/g \
			-e s/'{>>'/'<aside>'/g \
			-e s/'<<}'/'<\/aside>'/g)
### else (latex/pdf) then show CriticMarkup in latex (sub, del, ins, mark, comment)
	else
		CONTENT=$(echo "$CONTENT" | sed \
			-e s/'~~}'/'}'/g \
			-e s/'{~~'/'\\st{'/g \
			-e s/'~>'/'}\\underline{'/g \
			-e s/'{--'/'\\st{'/g \
			-e s/'--}'/'}'/g \
			-e s/'{++'/'\\underline{'/g \
			-e s/'++}'/'}'/g \
			-e s/'{=='/'\\hl{'/g \
			-e s/'==}'/'}'/g \
			-e s/'{>>'/'\\marginpar{'/g \
			-e s/'<<}'/'}'/g)
## else (not d, not showing CriticMarkup)
	fi
else
### if r or a then remove highlights and archive comments
	if [ $reject = true ] || [ $accept = true ]; then
		CONTENT=$(echo "$CONTENT" | sed \
			-e s/'{=='/''/g \
			-e s/'==}'/''/g \
			-e s/'{>>'/'<\!-- '/g \
			-e s/'<<}'/' -->'/g)
#### if r then reject sub, del, ins
		if [ $reject = true ]; then
			CONTENT=$(./criticmarkup-reject.py "$CONTENT")
#### else (a then accept sub, del, ins)
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