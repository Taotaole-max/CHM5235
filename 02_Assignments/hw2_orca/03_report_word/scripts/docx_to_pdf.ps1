# 用 Word 把 docx 转成同名 PDF（放在 docx 旁边），用来检查排版。
# 用法：powershell -ExecutionPolicy Bypass -File docx_to_pdf.ps1 <docx 完整路径>
param([string]$DocxPath)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($DocxPath, $false, $true)
    $pdf = [System.IO.Path]::ChangeExtension($DocxPath, ".pdf")
    $doc.SaveAs2($pdf, 17)
    $doc.Close($false)
    Write-Output "PDF: $pdf"
} finally {
    $word.Quit()
}
