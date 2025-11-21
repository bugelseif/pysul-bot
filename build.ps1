$exclude = @("venv", "bot-pysul.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot-pysul.zip" -Force