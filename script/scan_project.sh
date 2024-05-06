ecosystem=$1
installOSV=$2

source="../docker/$ecosystem/src"
result="../result/project/$ecosystem"

if [[ "$installOSV" == "true" ]]; then
  # Install OSV-Scanner
  curl -L https://github.com/google/osv-scanner/releases/download/v1.6.2/osv-scanner_1.6.2_linux_amd64 --output osv-scanner
  chmod 755 ./osv-scanner
fi
./osv-scanner scan -r $source > $result/osv-scanner.txt
trivy filesystem $source > $result/trivy.txt
grype $source --by-cve > $result/grype.txt
SNYK_TOKEN=$token SNYK_TOKEN=$token snyk test $source > $result/snyk.txt