## License
This program contains free software licensed under a number of licenses, including the GNU Lesser General Public License. A complete list of software is available at [Ren'Py License Documentation](https://www.renpy.org/doc/html/license.html)

## Description 

A portable cli unarchiver for the `.rpa` format used by the Ren'Py visual novel engine. Currently supports only RPA 3.0 archives.

## Usage
Via CLI
```bash
.\unpacker.exe "C:\game\archive.rpa" -o "C:\result" 
```

## Arguments

| Argument | Type | Description |
| :--- | :--- | :--- |
| `input_path` | `str` | Path to the input `.rpa` archive. *(Positional, required)* |
| `-o`, `--output` | `str` | Path to the target output directory. *(Required, **the directory must already exist**)* |

## Credits
* Compiled and packaged using [Nuitka](https://nuitka.net/).
