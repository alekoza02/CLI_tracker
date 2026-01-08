# CLI based plotting system. 
### No external modules required.

Will be made to plot data from files, and perform ETA for processes.

---

### Launch
```bash
python one_file.py -f \path\to\file
```

### Additional flags
- `-t` ---> typology:
    - \[$\textcolor{#aaffaa}{\mathrm{DEFAULT}}$\] `seconds`
    - \[$\textcolor{#ffffaa}{\mathrm{ACCEPTED}}$\] `seconds`, `elements`
    - \[$\mathrm{DESCRIPTION}$\]: type of elements to track when setting the width of the interpolation plot sliding window.
- `-n` ---> N of elements
    - \[$\textcolor{#aaffaa}{\mathrm{DEFAULT}}$\]: `30`
    - \[$\textcolor{#ffffaa}{\mathrm{ACCEPTED}}$\]: any positive integer
    - \[$\mathrm{DESCRIPTION}$\]: amount of elements to track after which the element is not shown anymore and not considered in further ETA calculations.
- `-i` ---> Show interpolation
    - \[$\textcolor{#aaffaa}{\mathrm{DEFAULT}}$\]: `y`
    - \[$\textcolor{#ffffaa}{\mathrm{ACCEPTED}}$\]: `y`, `n`
    - \[$\mathrm{DESCRIPTION}$\]: Decides to show or not the interpolation plot. Not computing the plot can result in higher performances.
- `-u` ---> max update time frequency 
    - \[$\textcolor{#aaffaa}{\mathrm{DEFAULT}}$\]: `0.5`
    - \[$\textcolor{#ffffaa}{\mathrm{ACCEPTED}}$\]: any positive float
    - \[$\mathrm{DESCRIPTION}$\]: Sets the max update frequency in seconds. You can use floats