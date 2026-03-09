# DOSMaster

[![PyPI](https://img.shields.io/pypi/v/dosmaster.svg)](https://pypi.org/project/dosmaster/)
[![GitHub](https://img.shields.io/badge/GitHub-DOSMaster-green)](https://github.com/pyj6767/DOSMaster)

**Program Name:** DOSMaster  
**Author:** Youngjun Park (yjpark29@postech.ac.kr)  
**Inspired by:** Jaeseon Kim (CNMD)  
**Tested by:** Changhun Kim (CNMD), Suyun Chae (CNMD)  
**Description:** Smartly plot Density of States (DOS) in a terminal environment.

> Version 1.8.3 and above will be publicly released to all CNMD members.

<p align="center">
  <img src="https://github.com/user-attachments/assets/e01ac05e-5180-4485-a01d-306459d4a4d6" style="width:400px"/>

  <img src="https://github.com/user-attachments/assets/859c7b95-6acb-49f6-bf01-2ecfadc00ba6" style="width:400px"/>
</p>

---

## Release History

| Version | Changes |
|---------|---------|
| 1.1 | Improved loading speed on restart (by Jaeseon Kim) |
| 1.2 | Added final data file export feature |
| 1.3 | Bug fixes |
| 1.4.2 | Refactored for PyPI packaging |
| 1.7.13 | Full packaging; added DOS_Sum, Average_DOS, Axis_Optimization, and various performance improvements |
| 1.8.1 | Fixed label bugs; added settings save/load, DOS plot save/load, shift_x_axis, extended sequential number input, and legend display toggle |
| 1.8.3 | Added ISPIN = 1 calculation support; various bug fixes |
| 1.8.4 | License update |
| 1.8.5 | Fixed f-orbital error |
| 1.8.8 | Fixed ylim optimization error when saving plot in current directory |
| 1.8.10 | Fixed f-orbital sum error |
| 1.8.12 | Fixed import order error |
| 1.8.15 | Fixed graph_editor back feature (suggested by Hyeongbin Park, CNMD) |
| 1.8.16 | Added Gaussian smearing feature (contributed by Siyeong Park, CNMD) |
| 1.8.22 | Added package version check feature |
| 1.8.24 | Fixed PROCAR bug; code generator in development |

---

## Features

1. **Add Atom DOS** — Add the DOS of a desired atom to the plot.
2. **DOS Projection** — Project a specific DOS onto a desired orbital.
3. **Sum DOS** — Sum the contributions of selected DOS entries.
4. **Average DOS** — Average the contributions of selected DOS entries.
5. **Remove DOS** — Remove a specific DOS from the plot.
6. **Plot only Positive/Negative Part** — Display only the positive or negative region of the DOS plot.
7. **Edit Graph Style** — Customize the graph style to your preference.
8. **Axis Optimization** — Automatically optimize the y-axis limits to fit the current DOS.
9. **Import Global Custom Setting** — Load your personal graph settings from the package folder.
10. **Save Global Custom Setting** — Save your personal graph settings to the package folder.
11. **Import DOSMaster Plot** — Load a previously saved DOSMaster plot from the current directory.
12. **Save DOSMaster Plot** — Save the current DOSMaster plot to the current directory.

---

## Installation

### Install via PyPI

```bash
pip install dosmaster
```

### Install from Source

1. Copy the SSH key from your server:
   ```bash
   cat ~/.ssh/id_rsa.pub
   ```
2. Go to your GitHub account → **Settings** → **SSH and GPG Keys** → **New SSH Key**, then paste the copied key.
3. Clone the repository on your server:
   ```bash
   git clone git@github.com:pyj6767/DOSMaster.git
   ```

---

## Requirements

```bash
pip install matplotlib numpy pandas ase colorama
```

---

## Usage

### Set Permissions

```bash
chmod 775 dosmaster
```

### Run DOSMaster

Navigate to the directory containing your DOS calculation results and run:

```bash
cd [your DOS calculation folder]
dosmaster
```

---

## License

DOSMaster is released under the [MIT License](https://opensource.org/licenses/MIT).
