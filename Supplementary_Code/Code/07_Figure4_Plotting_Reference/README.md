# Figure 4 plotting reference (historical source, not certified final renderer)

This script is an archived August 2026 version for a 25-journal bubble chart. It accepts a user-provided locally licensed `.xlsx` workbook with columns Journal, Publications, Average_Citations, Total_Citations, Local_H_Index. Figure 4 in the November 2026 manuscript displays 25 bubbles and 8 labels; for a matching count use `--top-n 25 --label-n 8`. This historical source has not been independently demonstrated to reproduce the final figure's exact label placement or all graphical details. It is retained for code traceability, not as a certified final plotting workflow.

Run (with local input; output remains local):

```powershell
python -m pip install -r requirements_figure4.txt
python journal_bubble_plot_reference.py "C:\path\to\journal_bubble_plot_data.xlsx" --top-n 25 --label-n 8 --output "C:\path\to\Figure4_local.png"
```

The example path above is a generic placeholder and does not reflect the authors' private path. Original licensed journals workbook is not distributed. The original script may display an optional `adjustText` warning; numeric summaries and chart provenance are in main text and Supplementary Table S2.
