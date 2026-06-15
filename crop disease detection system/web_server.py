"""
Simple web server for the interactive frontend
Serves the HTML file and handles diagnosis API requests
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
from text_diagnosis import PlantDiseaseDiagnosis


class DiagnosisHandler(SimpleHTTPRequestHandler):
    """Custom handler for serving files and handling diagnosis requests"""
    
    def do_GET(self):
        """Serve the interactive frontend"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/frontend_interactive.html'
        return super().do_GET()
    
    def do_POST(self):
        """Handle diagnosis API requests"""
        if self.path == '/api/diagnose':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Perform diagnosis
            diagnosis = PlantDiseaseDiagnosis()
            result = diagnosis.diagnose(
                plant_type=data.get('plant_type', ''),
                symptoms=data.get('symptoms', []),
                additional_info=data.get('additional_info', {})
            )
            
            # Generate report
            report = diagnosis.generate_report(result, output_format='json')
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(report.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"🌐 [{self.log_date_time_string()}] {args[0]}")


def run_server(port=3000):
    """Start the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DiagnosisHandler)
    
    print("\n" + "="*70)
    print("🌿 PLANT DISEASE DIAGNOSIS WEB SERVER")
    print("="*70)
    print(f"\n✅ Server running at: http://localhost:{port}")
    print(f"📱 Open in browser: http://localhost:{port}")
    print(f"📁 Serving files from: {Path(__file__).parent.absolute()}")
    print("\nPress CTRL+C to stop the server")
    print("="*70 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        httpd.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Plant Disease Diagnosis Web Server')
    parser.add_argument('-p', '--port', type=int, default=3000, 
                       help='Port to run the server on (default: 3000)')
    
    args = parser.parse_args()
    run_server(args.port)
