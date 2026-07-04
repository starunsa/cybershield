import subprocess
import json
import requests
import shutil
from pathlib import Path
from typing import Dict, List


class SecurityAgent:
    def __init__(self):
        pass

    def _trivy_command(self) -> str:
        local_trivy = Path(__file__).resolve().parents[2] / '.bin' / 'trivy'
        if local_trivy.exists():
            return str(local_trivy)
        return shutil.which('trivy') or ''

    def analyze_api(self, api_url: str, method: str = 'GET', headers: Dict = None, data: Dict = None) -> Dict:
        report = {
            'url': api_url,
            'method': method,
            'status_code': None,
            'risks': [],
            'resolutions': [],
            'headers': {}
        }

        try:
            response = requests.request(method, api_url, headers=headers or {}, json=data or {}, timeout=15)
            report['status_code'] = response.status_code
            report['headers'] = {k.lower(): v for k, v in response.headers.items()}

            if response.status_code == 200:
                content_lower = response.text.lower()
                if 'password' in content_lower or 'token' in content_lower or 'secret' in content_lower:
                    report['risks'].append('Potential sensitive data exposure in response body')
                    report['resolutions'].append('Do not return credentials or secrets from API endpoints')

            if 'x-frame-options' not in report['headers']:
                report['risks'].append('Missing X-Frame-Options header')
                report['resolutions'].append('Add X-Frame-Options header to prevent clickjacking')

            if 'x-content-type-options' not in report['headers']:
                report['risks'].append('Missing X-Content-Type-Options header')
                report['resolutions'].append('Add X-Content-Type-Options: nosniff')

            if 'content-security-policy' not in report['headers']:
                report['risks'].append('Missing Content-Security-Policy header')
                report['resolutions'].append('Implement a Content-Security-Policy header')

            if 'strict-transport-security' not in report['headers'] and api_url.startswith('https://'):
                report['risks'].append('Missing Strict-Transport-Security header')
                report['resolutions'].append('Use HSTS for HTTPS endpoints')

        except requests.exceptions.RequestException as exc:
            report['error'] = str(exc)
        except Exception as exc:
            report['error'] = str(exc)

        return report

    def analyze_image(self, image_name: str) -> Dict:
        report = {
            'image': image_name,
            'vulnerabilities': [],
            'risks': [],
            'resolutions': [],
            'error': None
        }
        trivy = self._trivy_command()
        if not trivy:
            report['error'] = (
                'Trivy is not installed or is not available on PATH. '
                'Install Trivy and restart the application.'
            )
            report['resolutions'].append('Install Trivy CLI: sh install_trivy.sh')
            return report

        try:
            result = subprocess.run(
                [trivy, 'image', '--quiet', '--format', 'json', image_name],
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )

            if result.stdout:
                data = json.loads(result.stdout)
                for entry in data.get('Results', []):
                    for vuln in entry.get('Vulnerabilities', []):
                        report['vulnerabilities'].append({
                            'id': vuln.get('VulnerabilityID'),
                            'severity': vuln.get('Severity'),
                            'package': vuln.get('PkgName'),
                            'installed_version': vuln.get('InstalledVersion'),
                            'fixed_version': vuln.get('FixedVersion'),
                            'title': vuln.get('Title'),
                            'description': vuln.get('Description', ''),
                        })
                        if vuln.get('Severity') in ('HIGH', 'CRITICAL'):
                            report['risks'].append(f"High severity vulnerability: {vuln.get('VulnerabilityID')}")
                            if vuln.get('FixedVersion'):
                                report['resolutions'].append(
                                    f"Upgrade {vuln.get('PkgName')} to {vuln.get('FixedVersion')} or newer"
                                )
                            else:
                                report['resolutions'].append(
                                    f"Investigate {vuln.get('VulnerabilityID')} and apply remediation"
                                )
            if result.returncode not in (0, 1) and not report['vulnerabilities']:
                report['error'] = result.stderr.strip() or result.stdout.strip() or 'Trivy scan failed'

        except subprocess.TimeoutExpired:
            report['error'] = 'Trivy scan timed out. Please try again with a smaller image or increase the timeout.'
        except Exception as exc:
            report['error'] = str(exc)

        return report

    def generate_report(self, api_reports: List[Dict], image_reports: List[Dict]) -> str:
        report = '# Security Analysis Report\n\n'
        report += '## API Analysis\n\n'
        if not api_reports:
            report += 'No API analysis was requested.\n\n'

        for api_rep in api_reports:
            report += f"### {api_rep.get('url', 'Unknown API')}\n"
            report += f"Status: {api_rep.get('status_code', 'N/A')}\n"
            if api_rep.get('error'):
                report += f"Error: {api_rep['error']}\n"
            if api_rep.get('risks'):
                report += 'Risks:\n'
                for risk in api_rep['risks']:
                    report += f"- {risk}\n"
            if api_rep.get('resolutions'):
                report += 'Resolutions:\n'
                for res in api_rep['resolutions']:
                    report += f"- {res}\n"
            report += '\n'

        report += '## Image Analysis\n\n'
        if not image_reports:
            report += 'No image analysis was requested.\n\n'

        for img_rep in image_reports:
            report += f"### {img_rep.get('image', 'Unknown image')}\n"
            if img_rep.get('error'):
                report += f"Error: {img_rep['error']}\n"
            if img_rep.get('vulnerabilities'):
                report += 'Vulnerabilities:\n'
                for vuln in img_rep['vulnerabilities']:
                    report += f"- {vuln.get('id')} ({vuln.get('severity')}): {vuln.get('title', '')}\n"
            if img_rep.get('risks'):
                report += 'Risks:\n'
                for risk in img_rep['risks']:
                    report += f"- {risk}\n"
            if img_rep.get('resolutions'):
                report += 'Resolutions:\n'
                for res in img_rep['resolutions']:
                    report += f"- {res}\n"
            report += '\n'

        return report


if __name__ == '__main__':
    agent = SecurityAgent()
    api_report = agent.analyze_api('https://httpbin.org/get')
    image_report = agent.analyze_image('alpine:latest')
    full_report = agent.generate_report([api_report], [image_report])
    print(full_report)
