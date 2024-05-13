ecosystem=$1

source="../docker/$ecosystem"
result="../result/project/$ecosystem"

mkdir -p $result

osv-scanner scan -r $source > $result/osv-scanner.txt
trivy filesystem $source > $result/trivy.txt
grype $source --by-cve > $result/grype.txt
SNYK_TOKEN=$token snyk test --all-projects $source > $result/snyk.txt