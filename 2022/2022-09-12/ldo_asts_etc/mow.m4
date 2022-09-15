dnl
dnl Example m4 implementation of the GPM example output shown on page 64
dnl of Bryan Higman's "A Comparative Study of Programming Languages", 1st ed.
dnl
dnl Created 2008 September 10 by Lawrence D'Oliveiro <ldo@geek-central.gen.nz>.
dnl
define(`repeat', `ifelse($2, 0, `', $2, 1, `$1', `$1`'repeat(`$1', eval($2 - 1))')')dnl
dnl repeat(str, n) outputs n consecutive repetitions of str
define(`n', `regexp(` x one two three four five six seven eight nine ten', `^\'repeat(` [^ ]+', $1)` \([^ ]+\)', `\1')')dnl
dnl n(i) returns the word representation of i. Need to use the "repeat" macro
dnl because m4's regexps don't support \{n\} repeat coefficients.
define(`cap', `regexp(`$1', `^\(.\)\(.*\)$', `translit(`\1', `a-z', `A-Z')\2')')dnl
dnl cap(s) returns s with the first letter capitalized.
dnl
define(`nrverses', 10)dnl
define(`nmen', `cap(n($1)) ifelse($1, 1, man, men)')dnl
dnl nmen(i) outputs the phrase "<i> man/men"
define(`tomow', ` went to mow')dnl
define(`mow1', `tomow a meadow')dnl
define(`firstline', `nmen($1)`'tomow,mow1')dnl
dnl firstline(i) outputs the first line of verse i.
define(`restlines', `ifelse($1, 1, `nmen(1) and his dog,mow1', `nmen($1)
restlines(eval($1 - 1))')')dnl
dnl restlines(i) outputs the remaining lines of verse i
define(`verse', `firstline($1)
restlines($1)')dnl
dnl verse(i) outputs the complete verse i
define(`verses', `verse($1)`'ifelse($1, nrverses, `', `

verses(eval($1 + 1))')')dnl
dnl verses(i) outputs the verses from i up to the last one.
dnl here we go...
verses(1)
