const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 1. Detect a working Python command
function getPythonCommand() {
  // Try default 'python' first
  try {
    execSync('python -c "import encodings"', { stdio: 'ignore' });
    return 'python';
  } catch (e) {
    // If on Windows, check common Python installation paths dynamically
    const userProfile = process.env.USERPROFILE || '';
    const localAppData = process.env.LOCALAPPDATA || path.join(userProfile, 'AppData', 'Local');
    
    const candidates = [
      path.join(localAppData, 'Programs', 'Python', 'Python313', 'python.exe'),
      path.join(localAppData, 'Programs', 'Python', 'Python312', 'python.exe'),
      path.join(localAppData, 'Programs', 'Python', 'Python311', 'python.exe'),
      path.join(localAppData, 'Programs', 'Python', 'Python310', 'python.exe'),
      'C:\\Python313\\python.exe',
      'C:\\Python312\\python.exe',
      'C:\\Python311\\python.exe',
    ];

    for (const candidate of candidates) {
      if (fs.existsSync(candidate)) {
        try {
          execSync(`"${candidate}" -c "import encodings"`, { stdio: 'ignore' });
          console.log(`[Launcher] Detected valid Python: ${candidate}`);
          return candidate;
        } catch (err) {
          // Continue searching candidates
        }
      }
    }
    
    // Check if python3 works
    try {
      execSync('python3 -c "import encodings"', { stdio: 'ignore' });
      return 'python3';
    } catch (e2) {
      // Check py launcher
      try {
        execSync('py -3 -c "import encodings"', { stdio: 'ignore' });
        return 'py -3';
      } catch (e3) {
        console.warn('[Launcher] Warning: Could not locate a fully working Python. Defaulting to "python".');
        return 'python';
      }
    }
  }
}

const pythonCmd = getPythonCommand();
const args = process.argv.slice(2);

// Check if we are running in install-only mode
if (args.includes('--install-only')) {
  console.log('[Launcher] Installing dependencies...');
  try {
    console.log('[Launcher] Running npm install for frontend...');
    execSync('npm install', { cwd: path.join(__dirname, 'frontend'), stdio: 'inherit' });
    
    console.log('[Launcher] Running pip install for backend...');
    execSync(`"${pythonCmd}" -m pip install -r requirements.txt`, { cwd: path.join(__dirname, 'backend'), stdio: 'inherit' });
    
    console.log('[Launcher] Installation completed successfully.');
    process.exit(0);
  } catch (err) {
    console.error('[Launcher] Installation failed:', err.message);
    process.exit(1);
  }
}

// Check if we are running in backend-only mode
const startFrontend = !args.includes('--backend-only');
const startBackend = !args.includes('--frontend-only');

let backendProcess = null;
let frontendProcess = null;

if (startBackend) {
  console.log(`[Launcher] Starting backend with ${pythonCmd}...`);
  backendProcess = spawn(pythonCmd, ['main.py'], {
    cwd: path.join(__dirname, 'backend'),
    shell: true
  });

  // Prefix backend logs
  backendProcess.stdout.on('data', (data) => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
      if (line.trim()) console.log(`[Backend] ${line.trim()}`);
    });
  });

  backendProcess.stderr.on('data', (data) => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
      if (line.trim()) console.error(`[Backend] [Err] ${line.trim()}`);
    });
  });

  backendProcess.on('close', (code) => {
    console.log(`[Launcher] Backend process exited with code ${code}`);
    if (frontendProcess) frontendProcess.kill();
    process.exit(code);
  });
}

if (startFrontend) {
  console.log('[Launcher] Starting frontend dev server...');
  frontendProcess = spawn('npm', ['run', 'dev'], {
    cwd: path.join(__dirname, 'frontend'),
    shell: true
  });

  // Prefix frontend logs
  frontendProcess.stdout.on('data', (data) => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
      if (line.trim()) console.log(`[Frontend] ${line.trim()}`);
    });
  });

  frontendProcess.stderr.on('data', (data) => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
      if (line.trim()) console.error(`[Frontend] [Err] ${line.trim()}`);
    });
  });

  frontendProcess.on('close', (code) => {
    console.log(`[Launcher] Frontend process exited with code ${code}`);
    if (backendProcess) backendProcess.kill();
    process.exit(code);
  });
}

// Clean termination handling
function shutdown() {
  console.log('\n[Launcher] Shutting down servers...');
  if (backendProcess) {
    try {
      backendProcess.kill();
    } catch (e) {}
  }
  if (frontendProcess) {
    try {
      frontendProcess.kill();
    } catch (e) {}
  }
  process.exit(0);
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
