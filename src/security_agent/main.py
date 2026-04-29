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
        """
        Analyze API for security threats.
        Basic checks: response codes, headers, etc.
        """
        report = {
            'url': api_url,
            'method': method,
            'risks': [],
            'resolutions': []
        }
        try:
            response = requests.request(method, api_url, headers=headers, json=data, timeout=10)
            report['status_code'] = response.status_code
            # Check for common issues
            if response.status_code == 200:
                # Check if sensitive data in response
                if 'password' in response.text.lower() or 'token' in response.text.lower():
                    report['risks'].append('Potential sensitive data exposure')
                    report['resolutions'].append('Ensure sensitive data is not returned in API responses')
            # Check headers
            if 'x-frame-options' not in response.headers:
                report['risks'].append('Missing X-Frame-Options header')
                report['resolutions'].append('Add X-Frame-Options header to prevent clickjacking')
            # More checks can be added
        except Exception as e:
            report['error'] = str(e)
        return report

    def analyze_image(self, image_name: str) -> Dict:
        """
        Analyze container image for vulnerabilities using Trivy.
        """
        report = {
            'image': image_name,
            'vulnerabilities': [],
            'risks': [],
            'resolutions': []
        }
        trivy = self._trivy_command()
        if not trivy:
            report['error'] = (
                "Trivy is not installed or is not available on PATH. "
                "Run `sh install_trivy.sh` from the project folder, then restart the app."
            )
            report['resolutions'].append('Install Trivy CLI: sh install_trivy.sh')
            return report

        try:
            # Run trivy scan
            result = subprocess.run([trivy, 'image', '--format', 'json', image_name], capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for vuln in data.get('Results', []):
                    for v in vuln.get('Vulnerabilities', []):
                        report['vulnerabilities'].append({
                            'id': v['VulnerabilityID'],
                            'severity': v['Severity'],
                            'description': v.get('Description', ''),
                            'package': v.get('PkgName', ''),
                            'fixed_version': v.get('FixedVersion', '')
                        })
                        if v['Severity'] in ['HIGH', 'CRITICAL']:
                            report['risks'].append(f"High severity vulnerability: {v['VulnerabilityID']}")
                            report['resolutions'].append(f"Update {v.get('PkgName', '')} to version {v.get('FixedVersion', '')} or later")
            else:
                report['error'] = result.stderr
        except Exception as e:
            report['error'] = str(e)
        return report

    def generate_report(self, api_reports: List[Dict], image_reports: List[Dict]) -> str:
        """
        Generate a complete report.
        """
        report = "# Security Analysis Report\n\n"
        report += "## API Analysis\n"
        for api_rep in api_reports:
            report += f"### {api_rep['url']}\n"
            report += f"Status: {api_rep.get('status_code', 'N/A')}\n"
            if api_rep.get('risks'):
                report += "Risks:\n"
                for risk in api_rep['risks']:
                    report += f"- {risk}\n"
                report += "Resolutions:\n"
                for res in api_rep['resolutions']:
                    report += f"- {res}\n"
            report += "\n"

        report += "## Image Analysis\n"
        for img_rep in image_reports:
            report += f"### {img_rep['image']}\n"
            if img_rep.get('vulnerabilities'):
                report += "Vulnerabilities:\n"
                for vuln in img_rep['vulnerabilities']:
                    report += f"- {vuln['id']} ({vuln['severity']}): {vuln['description']}\n"
            if img_rep.get('risks'):
                report += "Risks:\n"
                for risk in img_rep['risks']:
                    report += f"- {risk}\n"
                report += "Resolutions:\n"
                for res in img_rep['resolutions']:
                    report += f"- {res}\n"
            report += "\n"
        return report

if __name__ == "__main__":
    agent = SecurityAgent()
    # Example usage
    api_report = agent.analyze_api('https://httpbin.org/get')
    image_report = agent.analyze_image('alpine:latest')
    full_report = agent.generate_report([api_report], [image_report])
    print(full_report)
