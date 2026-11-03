# START HERE / Version 2

Keep your old download. Extract this new ZIP into a separate folder.

1. Open `FilterSense_v2` and double-click `Start_FilterSense.bat`.
2. Stop the old app first: press Ctrl+C in its black terminal window. This frees port 8501.
3. Wait for setup messages. No email address is needed.
4. Open http://localhost:8501 if the browser does not open.
5. For 3D CAD without installing anything: open `cad/FilterSense_3D_Viewer.html` in Chrome or Edge. Internet is not needed for the viewer.

Text visibility fix: forced white backgrounds are removed; cards now inherit the selected theme. Default theme is Light, but Dark can still be selected. If an old browser session looks stale, press Ctrl+F5.

The MP4 is a silent captioned demo, not a screen recording of your laptop or a physical purifier. The supplied speaking script can be used for team narration.

# FilterSense v2 — start here

Team Spartans / Thiagarajar College of Engineering / Track 2, atomQUEST 2026.

This package contains a working **simulated software prototype** and **concept CAD**. No physical prototype, experimentally validated remaining life, drinking-water certification, or native SOLIDWORKS execution is claimed.

## Run on Windows
1. Extract the entire ZIP to a folder such as `Desktop\FilterSense_v2`.
2. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ if absent. Enable the Python launcher during installation.
3. Double-click `Start_FilterSense.bat`. First run installs dependencies and needs internet access.
4. The browser opens at http://localhost:8501. Keep the terminal open. Ctrl+C stops it.
5. Choose a scenario; move Replay day; inject a leak; clear the fault and reset the latch.

Manual equivalent, in the extracted folder:
```
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r software\requirements.txt
.venv\Scripts\python.exe -m streamlit run software\app.py
```

Run repeatable checks:
```
.venv\Scripts\python.exe software\validate.py
.venv\Scripts\python.exe software\test_ui.py
```

## Open CAD
In SOLIDWORKS, File > Open, choose STEP files, and open `cad/FilterSense_assembly.step`. Import may use 3D Interconnect depending on your installation. Open individual files in `cad/parts` for isolated geometry. Save imported documents as SOLIDWORKS parts/assemblies if desired. These are imported solids; they do not contain native parametric feature histories or mechanical mates. Use the modelling handbook to recreate native features. SOLIDWORKS import was not executed here.

`cad/build_cad.py` regenerates geometry using CadQuery. The dashboard does NOT require CadQuery. To regenerate separately: install `cadquery` and `matplotlib`, then run that file. All dimensions are design assumptions; fittings, seals, fasteners, supports and pressure ratings require detailed engineering before manufacture. CAD is a spatial concept, not a functioning hydraulic assembly.

## Where everything is
- `software/`: complete dashboard, simulator, analysis, functional tests and UI tests.
- `data/simulated_scenarios.csv`: five clearly labelled synthetic histories.
- `cad/`: STEP parts, assemblies, exploded assembly, renders and reproducible CAD source.
- `docs/`: progress report, modelling handbook, architecture, formulas, video script, plans.
- `evidence/`: actual test results and leave-one-run-out predictions.

## Build documentation and video again
Optional build dependencies are in `docs/build_assets_requirements.txt` (separate from the lightweight dashboard requirements). Run `docs/build_documents.py` for PDFs, `docs/build_architecture.py` for diagrams, and `docs/build_video.py` for the 86-second silent captioned MP4. The video renderer also needs FFmpeg on PATH. Its frames are generated from core.py outputs, not captured from a physical device or the Streamlit browser.

## Evidence and limitations
The user confirmed v1 opens on their laptop. Version 2 was tested in this development environment; its local laptop run is not yet confirmed. See evidence files for actual results. Initial spending is recorded as INR 0 based on the supplied brief, against the approximate INR 12,000 estimate. The original submitted abstract is unavailable; compare the report against it before uploading. No submission has been made on your behalf.

The software estimates time to assumed intervention thresholds. It cannot distinguish sediment from carbon restriction with only P1/P2. Carbon adsorption exhaustion may occur without pressure rise. Salt rejection is not a complete measure of safety. The synthetic generator and evaluators share assumptions, so small errors cannot support a field-accuracy claim.

## Troubleshooting
- `py` missing: repair/install Python with launcher, or substitute `python` if it is available.
- Package install failed: check network; rerun the BAT file. Do not run it inside the ZIP viewer.
- Port occupied: add `--server.port 8502` to the Streamlit command.
- STEP import issues: open a single part first; use SOLIDWORKS Import Diagnostics where available.
- Do not paste your SOLIDWORKS licence key into source files, screenshots or reports.
