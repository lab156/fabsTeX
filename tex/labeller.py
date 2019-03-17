import re

filename = "fsg.tex"

tags = dict()
labels = dict()
inactive = []

with open("tags") as f:
  for line in f:
    # actual tag
    if not line.startswith("#"):
      tags[line.split(",")[0]] = line.strip().split(",")[1]
      labels[line.strip().split(",")[1]] = line.strip().split(",")[0]

    # check for inactive tags too
    elif len(line.split(",")) == 2 and len(line.split(",")[0]) == 4:
      inactive.append(line.split(",")[0])

# recursively read a TeX file
def read(filename):
  # \input doesn't have the .tex
  if filename[-4:] != ".tex":
    filename = filename + ".tex"

  tex = ""

  with open(filename) as f:
    for line in f:
      # remove comments
      line = line.split("%")[0]

      # look for \input's
      matches = re.findall("\\\\input{([^}]+)", line)
      for match in matches:
        line = line.replace("\\input{" + match + "}", read(match))

      tex = tex + line

  return tex

tex = ""
with open(filename) as f:
  tex = read(filename)

  matches = re.findall("\\\\label{([^}]+)}", tex)
  for match in matches:
    if match not in labels:
      print("ERROR: " + match + "not in tags")

    label = "\\label{" + match + "}"
    marginnote = ""
    # don't do this for parts
    if match[:5] != "Part:":
      marginnote = "\\reversemarginpar\\marginnote{\\normalfont\\texttt{\\href{http://127.0.0.1:8000/tag/" + labels[match] + "}{" + labels[match] + "}}}"
    hypertarget = "\\hypertarget{" + labels[match] + "}{}"
    replacement = label + hypertarget + marginnote

    tex = tex.replace(label, replacement)

  print(tex)
