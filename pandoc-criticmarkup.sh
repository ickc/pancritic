#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

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

##debug
## echo "accept: "$accept "; reject: " $reject "; permanent: " $permanent "; output extension: " $output_EXT "."

# preparation

## get paths and extension
PATHNAME="$@"
PATHNAMEWOEXT=${PATHNAME%.*}
EXT=${PATHNAME##*.}
### ext="${EXT,,}" #This does not work on Mac's default, old version of, bash.

## copy or permanent?
if [ $permanent = false ]; then
	cp "$PATHNAME" "$PATHNAMEWOEXT-critic.$EXT"
	PATHNAME="$PATHNAMEWOEXT-critic.$EXT"
fi

# cooking the result

## if d then show diff (CriticMarkup)
if [ "$output_EXT" = "html" ] || [ "$output_EXT" = "latex" ] || [ "$output_EXT" = "pdf" ]; then
### if html then show CriticMarkup in html
	if [ "$output_EXT" = "html" ]; then
		#### sub
		sed -i '' s/'~~}'/'<\/ins>'/g "$PATHNAME"
		sed -i '' s/'{~~'/'<del>'/g "$PATHNAME"
		sed -i '' s/'~>'/'<\/del><ins>'/g "$PATHNAME"
		#### del
		sed -i '' s/'{--'/'<del>'/g "$PATHNAME"
		sed -i '' s/'--}'/'<\/del>'/g "$PATHNAME"
		#### ins
		sed -i '' s/'{++'/'<ins>'/g "$PATHNAME"
		sed -i '' s/'++}'/'<\/ins>'/g "$PATHNAME"
		#### mark
		sed -i '' s/'{=='/'<mark>'/g "$PATHNAME"
		sed -i '' s/'==}'/'<\/mark>'/g "$PATHNAME"
		#### comment
		sed -i '' s/'{>>'/'<aside>'/g "$PATHNAME"
		sed -i '' s/'<<}'/'<\/aside>'/g "$PATHNAME"
### else (latex/pdf) then show CriticMarkup in latex
	else
		#### sub
		sed -i '' s/'~~}'/'}'/g "$PATHNAME"
		sed -i '' s/'{~~'/'\\st{'/g "$PATHNAME"
		sed -i '' s/'~>'/'}\\underline{'/g "$PATHNAME"
		#### del
		sed -i '' s/'{--'/'\\st{'/g "$PATHNAME"
		sed -i '' s/'--}'/'}'/g "$PATHNAME"
		#### ins
		sed -i '' s/'{++'/'\\underline{'/g "$PATHNAME"
		sed -i '' s/'++}'/'}'/g "$PATHNAME"
		#### mark
		sed -i '' s/'{=='/'\\hl{'/g "$PATHNAME"
		sed -i '' s/'==}'/'}'/g "$PATHNAME"
		#### comment
		sed -i '' s/'{>>'/'\\marginpar{'/g "$PATHNAME"
		sed -i '' s/'<<}'/'}'/g "$PATHNAME"
## else (not d, not showing CriticMarkup)
	fi
else
### if r or a then remove highlights and archive comments
	if [ $reject = true ] || [ $accept = true ]; then
		#### mark
		sed -i '' s/'{=='/''/g "$PATHNAME"
		sed -i '' s/'==}'/''/g "$PATHNAME"
		#### comment
		sed -i '' s/'{>>'/'<\!-- '/g "$PATHNAME"
		sed -i '' s/'<<}'/' -->'/g "$PATHNAME"
#### if r then reject
		if [ $reject = true ]; then
			./criticmarkup-reject.py "$PATHNAME" > "$PATHNAMEWOEXT-temp.$EXT"
			cp "$PATHNAMEWOEXT-temp.$EXT" "$PATHNAME"
			mv "$PATHNAMEWOEXT-temp.$EXT" ~/.Trash/
#### else (a then accept)
		else
			./criticmarkup-accept.py "$PATHNAME" > "$PATHNAMEWOEXT-temp.$EXT"
			cp "$PATHNAMEWOEXT-temp.$EXT" "$PATHNAME"
			mv "$PATHNAMEWOEXT-temp.$EXT" ~/.Trash/
		fi
	fi
fi

# put result in stdout
cat "$PATHNAME"
# cleanup if not permanent
if [ $permanent = false ]; then
	mv "$PATHNAMEWOEXT-critic.$EXT" ~/.Trash/
fi