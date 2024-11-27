import subprocess

# Run secondary script
subprocess.run(["python", "./web/interactive_plot.py"])

# Create HTML file with embedded result
main_content = """
<!DOCTYPE html>
<html>
<head>
    <title>ARMP Summary Page</title>
</head>
<body>
    <h1>Atmospheric River Metrics Package (ARMP) Interactive Results</h1>
    <iframe src="spatial_corr_plot_01.html" width="1000" height="1200" style="border:1px solid black;">
        Your browser does not support iframes.
    </iframe>
</body>
</html>
"""

# Save this file
with open("./web/ARMP_summary_page.html", "w") as main_file:
    main_file.write(main_content)

print("ARMP Summary page created as: ARMP_summary_page.html")