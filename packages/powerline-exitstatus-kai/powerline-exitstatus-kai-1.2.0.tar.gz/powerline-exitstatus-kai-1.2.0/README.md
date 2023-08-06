# Powerline Exitstatus Kai

A [Powerline][1] segment for showing exit status or code. Modified from [Powerline Exitstatus][4].

It will show last exit status or code depending on your configuration.

![screenshot](./screenshot.png)

## Glossary

With `symbol` style enabled (default showing codes):

* `✔`: exit success
* `✕`: exit fail

## Installation
```bash
pip install powerline-exitstatus-kai
```

The Exitstatus segment a couple of custom highlight groups. You'll need to define those groups in your colorscheme, for example in `.config/powerline/colorschemes/default.json`:

```json
{
    "groups": {
        "exit_status_success":        { "fg": "mediumgreen",     "bg": "gray2", "attrs": [] },
        "exit_status_fail":           { "fg": "brightestred",    "bg": "gray2", "attrs": [] }
  }
}
```

Then you can activate the Exitstatus segment by adding it to your segment configuration, for example in `.config/powerline/themes/shell/default.json`:

```json
{
    "function": "powerline_exitstatus.exit_status",
    "priority": 10
}
```

If you want to show exit status only failed, you can enable by setting `only_failed` argument to `true`.

```json
{
    "function": "powerline_exitstatus.exit_status",
    "args": {
        "only_failed": true
    }
}
```

If you want to show a status rather than exit codes, you can enable by setting `style` argument to `symbol`.

```json
{
    "function": "powerline_exitstatus.exit_status",
    "args": {
        "style": "symbol"
    }
}
```

To become even more simplistic, set `style` to `color` and only a colored block will be shown. Note you'll need to change bg color in your colorscheme for this to work, by default both success and fail are gray.<br>
Any value other than these three mentioned will cause an error.

## License
Licensed under [the MIT License][3].

[1]: http://powerline.readthedocs.io/en/master/index.html
[2]: https://github.com/shimtom/powerline-exitstatus/blob/master/screenshot.png 
[3]: https://github.com/shimtom/powerline-exitstatus/blob/master/LICENSE
[4]: https://github.com/shimtom/powerline-exitstatus
