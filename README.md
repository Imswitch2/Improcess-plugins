# Improcess-plugins

The online plugin registry for **ImProcess** (the post-acquisition analysis
module of [ImSwitch2](https://github.com/Imswitch2)) drop-in analysis plugins.

An ImProcess drop-in plugin is a single `.py` file that defines one or more
`imswitch.improcess.processors.base.Processor` subclasses. Dropped into the user
plugins folder (`~/.imswitch/improcess_plugins/`), it becomes a fully integrated
analysis tool — parameter panel, result-kind gating, results table / graph — with
no packaging.

ImProcess browses this repository from **Analyze → Drop-in plugins → Browse
online plugins…**, where plugins can be installed, updated and uninstalled.

## Repository layout

```
index.json          # the manifest: the list of available plugins
plugins/            # the plugin .py files
  invert.py
  gaussian_blur.py
  median_filter.py
  percentile_normalize.py
```

## Manifest (`index.json`)

```json
{
  "schema_version": "1",
  "plugins": [
    {
      "id": "invert",                         // unique registry id; installed as <id>.py
      "display_name": "Invert",               // shown in the store
      "description": "…",
      "version": "1.0.0",                      // bump to offer an update
      "file": "plugins/invert.py",             // path in this repo
      "author": "…",
      "min_improcess_version": "0.1"           // hide on older ImProcess
    }
  ]
}
```

The store installs a plugin by downloading `file` into the user plugins folder
as `<id>.py`, and records the installed version in a hidden `.installed.json`
sidecar there. Bumping an entry's `version` offers an update.

## Contributing a plugin

1. Add your `plugins/<name>.py` (an ordinary `Processor` subclass — give it a
   unique, dotted `id` such as `"me.myfilter"` and set `kinds`).
2. Add a matching entry to `index.json`.
3. Open a pull request.

Keep plugins dependency-light; import any optional dependency lazily inside
`apply()` and raise a clear error if it is missing.

> **Trust:** installing a plugin downloads and runs arbitrary Python on your
> machine at ImProcess startup. Only install plugins you trust.

## License

GPL-3.0-or-later, matching ImSwitch.
