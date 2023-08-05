
# YaLafi: Yet another LaTeX filter

This Python package extracts plain text from LaTeX documents.
Due to the following characteristics, the software may be integrated with a
proofreading tool:
- tracking of character positions during text manipulations,
- simple inclusion of own LaTeX macros and environments with tailored
  treatment,
- careful conservation of text flows,
- detection of trailing interpunction in equations,
- proper handling of nestable LaTeX elements like {} braces.

A more complete description, including an interface to the plug-in
[vim-grammarous](https://github.com/rhysd/vim-grammarous)
for Vim, is available at the
[GitHub page](https://github.com/matze-dd/YaLafi).
For instance, the LaTeX input
```
Only few people\footnote{We use
\textcolor{red}{redx colour.}}
is lazy.
```
will lead to the subsequent output from example application script
yalafi/shell/shell.py.
The script invokes [LanguageTool](https://www.languagetool.org)
as proofreading software, using a local installation or the Web server
hosted by LanguageTool.
```
1.) Line 2, column 17, Rule ID: MORFOLOGIK_RULE_EN_GB
Message: Possible spelling mistake found
Suggestion: red; Rex; reds; redo; Red; Rede; redox; red x
Only few people is lazy.    We use redx colour. 
                                   ^^^^
2.) Line 3, column 1, Rule ID: PEOPLE_VBZ[1]
Message: If 'people' is plural here, don't use the third-person singular verb.
Suggestion: am; are; aren
Only few people is lazy.    We use redx colour. 
                ^^
```
Run with option '--output html', the script produces an HTML report:

![HTML report](https://raw.githubusercontent.com/matze-dd/YaLafi/master/shell.png)

