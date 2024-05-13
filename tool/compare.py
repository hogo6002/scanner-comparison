import json
import sys

ecosystem = ''
path_base = ''
scan_type = ''

def get_cves_from_trivy(parsed_json):
  cve_ids = set()
  all = []
  for type in parsed_json['Results']:
    for vuln in type['Vulnerabilities']:
      id = vuln['VulnerabilityID']
      cve_ids.add(id)
      all.append(id)
  return all, cve_ids

def get_cves_from_grype(parsed_json):
  cve_ids = set()
  all = []
  for entry in parsed_json['matches']:
    id = entry['vulnerability']['id']
    cve_ids.add(id)
    all.append(id)
  return all, cve_ids

def get_cves_from_docker_scout(parsed_json):
  cve_ids = set()
  all = []
  duplicate = set()
  for entry in parsed_json['runs'][0]['results']:
    id = entry['ruleId']
    if id in cve_ids:
      duplicate.add(id)
    cve_ids.add(id)
    all.append(id)
  return all, cve_ids, duplicate

def get_cves_from_snyk(parsed_json):
  cve_ids = set()
  all = []
  duplicate = set()
  for vuln in parsed_json['vulnerabilities']:
    id = vuln['identifiers']["CVE"][0]
    if id in cve_ids:
      duplicate.add(id)
    cve_ids.add(id)
    all.append(id)
  return all, cve_ids, duplicate

def load_json(tool):
  file_path = f'{path_base}/{tool}.json'
  print(f'checking {file_path}')
  with open(file_path) as json_file:
    parsed_json = json.load(json_file)
    return parsed_json

def main():
  args = sys.argv[1:]
  global ecosystem, scan_type, path_base
  scan_type = args[0]
  ecosystem = args[1]
  path_base = f'../result/{scan_type}/{ecosystem}'

  parsed_json = load_json('trivy')
  trivy_result = get_cves_from_trivy(parsed_json)

  parsed_json = load_json('grype')
  grype_result = get_cves_from_grype(parsed_json)

  parsed_json = load_json('docker_scout')
  docker_scout_result = get_cves_from_docker_scout(parsed_json)

  parsed_json = load_json('snyk')
  snyk_result = get_cves_from_snyk(parsed_json)

  common_ids = trivy_result[1] & grype_result[1] & docker_scout_result[1] & snyk_result[1]
  all_ids = trivy_result[1].union(grype_result[1]).union(docker_scout_result[1]).union(snyk_result[1])

  only_in_trivy = trivy_result[1] - grype_result[1] - docker_scout_result[1] - snyk_result[1]
  only_in_grype= grype_result[1] - trivy_result[1] - docker_scout_result[1] - snyk_result[1]
  only_in_docker_scout = docker_scout_result[1] - trivy_result[1] - grype_result[1] - snyk_result[1]
  only_in_snyk = snyk_result[1] - docker_scout_result[1] - trivy_result[1] - grype_result[1]

  docker_scout_missing = all_ids - docker_scout_result[1]
  snyk_missing = all_ids - snyk_result[1]
  trivy_missing = all_ids - trivy_result[1]
  grype_missing = all_ids - grype_result[1]

  common_trivy_and_grype = trivy_result[1] & grype_result[1]
  diff_trivy_and_grype = trivy_result[1].union(grype_result[1]) - common_trivy_and_grype
  common_snyk_and_docker_scout = snyk_result[1] & docker_scout_result[1]
  diff_snyk_and_docker_scout = snyk_result[1].union(docker_scout_result[1]) - common_snyk_and_docker_scout

  

  f = open(f'{path_base}/comparison.txt', 'w+')
  f.write(f'{ecosystem}\n\n')
  f.write(f'Trivy:\nOriginal: {len(trivy_result[0])}\nfinal: {len(trivy_result[1])}\n{trivy_result[1]}\n\n')
  f.write(f'Grype:\nOriginal: {len(grype_result[0])}\nfinal: {len(grype_result[1])}\n{grype_result[1]}\n\n')
  f.write(f'Docker scout:\nOriginal: {len(docker_scout_result[0])}\nfinal: {len(docker_scout_result[1])}\n{docker_scout_result[1]}\nduplicate: {docker_scout_result[2]}\n\n')
  f.write(f'Snyk:\nOriginal: {len(snyk_result[0])}\nfinal: {len(snyk_result[1])}\n{snyk_result[1]}\nduplicate: {snyk_result[2]}\n\n')

  f.write(f'\nMore results:\n')
  f.write(f'Common ones: {len(common_ids)}\n{common_ids}\n\n')
  f.write(f'All vulns: {len(all_ids)}\n{all_ids}\n\n')
  f.write(f'only_in_trivy ones: {len(only_in_trivy)}\n{only_in_trivy}\n')
  f.write(f'only_in_grype ones: {len(only_in_grype)}\n{only_in_grype}\n')
  f.write(f'only_in_docker_scout ones: {len(only_in_docker_scout)}\n{only_in_docker_scout}\n')
  f.write(f'only_in_snyk ones: {len(only_in_snyk)}\n{only_in_snyk}\n\n')

  f.write(f'trivy_missing ones: {len(trivy_missing)}\n{trivy_missing}\n')
  f.write(f'grype_missing ones: {len(grype_missing)}\n{grype_missing}\n')
  f.write(f'docker_scout_missing ones: {len(docker_scout_missing)}\n{docker_scout_missing}\n')
  f.write(f'snyk_missing ones: {len(snyk_missing)}\n{snyk_missing}\n\n')

  f.write(f'diff_trivy_and_grype ones: {len(diff_trivy_and_grype)}\n{diff_trivy_and_grype}\n')
  f.write(f'diff_snyk_and_docker_scout ones: {len(diff_snyk_and_docker_scout)}\n{diff_snyk_and_docker_scout}\n\n')



  f.close()

if __name__ == '__main__':
  main()