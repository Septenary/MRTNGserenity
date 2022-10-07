# What this is.

To generate [Method Raid Tools](https://www.curseforge.com/wow/addons/method-raid-tools) notes for WoW raids from a set of templates, and a set of assignments.

# How do I use it.

```console
$ generate.py --templates <PATH/TO/TEMPLATEDIR> --raid <RAID.JSON> --output <OUTPUT.JSON> --assignments <ASSIGNMENTS.JSON>

$ generate.py
```

You can find default templates in `templates/sharks/WOTLK-Phase1`. The raid.json should be exported from [Raid Helper](https://raid-helper.com/commands) as a JSON file.

If run with no options, generate.py will use the templates in `templates/sharks/WOTLK-Phase1`, will look for the raid.json in the current directory `raid.json`, will write output to `output.json` and will look for assignments in `assignments.yaml`.

# What will it do.

Produce a JSON file for use with the [MRTNoteImporter](https://github.com/davidgroves/MRTNoteImporter) addon.


