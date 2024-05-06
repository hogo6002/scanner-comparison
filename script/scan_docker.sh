ecosystem=$1
buildImage=$2
json=$3

if [[ $1 == "-h" || $1 == "--help" || $# -lt 3 ]]; then  # Check for help flags or insufficient arguments
    echo "Usage: run.sh ecosystem buildImage json"
    echo "Where:"
    echo "  ecosystem:  The name of the ecosystem"
    echo "  buildImage: 'true' to indicate image build"
    echo "  json:       'true' to output the results in JSON format"
    exit 0 
fi

docker="$ecosystem-tester"
result="../result/docker/$ecosystem"
source="../docker/$ecosystem"
if [[ "$buildImage" == "true" ]]; then
  echo "building docker image from $source"
  docker image rm $docker
  docker build -t $docker $source
fi

mkdir -p $result

if [[ "$json" == "true" ]]; then
  echo "Generating JSON results."
  trivy image --format json --scanners vuln $docker > $result/trivy.json
  grype $docker -o json > $result/grype.json
  SNYK_TOKEN=$token snyk container test --json $docker > $result/snyk.json
  docker scout cves --format sarif --details $docker > $result/docker_scout.json
  exit 0
fi

echo "$(date +"%Y-%m-%d %T") Running trivy"
trivy image --scanners vuln $docker > $result/trivy.txt

echo "$(date +"%Y-%m-%d %T") Running grype"
grype $docker > $result/grype.txt

echo "$(date +"%Y-%m-%d %T") Running snyk"
snyk container test $docker > $result/snyk.txt

echo "$(date +"%Y-%m-%d %T") Running docker scout"
docker scout cves $docker > $result/docker_scout.txt

echo "$(date +"%Y-%m-%d %T") Finished"