document.addEventListener("alpine:init", () => {
  Alpine.data("deployPortal", () => ({
    activePhaseId: "phase1",
    activePartId: "phase1-a",
    copiedTarget: null,

    initHighlighting() {
      this.$nextTick(() => {
        if (window.Prism) Prism.highlightAll();
      });
    },

    selectPhase(phaseId) {
      this.activePhaseId = phaseId;
      const ph = this.phases.find((p) => p.id === phaseId);
      if (ph && ph.parts && ph.parts.length > 0) {
        this.activePartId = ph.parts[0].id;
      }
      this.$nextTick(() => {
        if (window.Prism) Prism.highlightAll();
      });
    },

    selectPart(phaseId, partId) {
      this.activePhaseId = phaseId;
      this.activePartId = partId;
      this.$nextTick(() => {
        if (window.Prism) Prism.highlightAll();
      });
    },

    get currentPhase() {
      return (
        this.phases.find((p) => p.id === this.activePhaseId) || this.phases[0]
      );
    },

    get currentPart() {
      const ph = this.currentPhase;
      return (
        ph.parts.find((pt) => pt.id === this.activePartId) || ph.parts[0]
      );
    },

    getAllParts() {
      const list = [];
      this.phases.forEach((ph) => {
        ph.parts.forEach((pt) => {
          list.push({ phaseId: ph.id, partId: pt.id });
        });
      });
      return list;
    },

    isFirstPart() {
      const all = this.getAllParts();
      return (
        all.length === 0 ||
        (all[0].phaseId === this.activePhaseId &&
          all[0].partId === this.activePartId)
      );
    },

    isLastPart() {
      const all = this.getAllParts();
      if (all.length === 0) return true;
      const last = all[all.length - 1];
      return (
        last.phaseId === this.activePhaseId && last.partId === this.activePartId
      );
    },

    goToPrevPart() {
      const all = this.getAllParts();
      const idx = all.findIndex(
        (item) =>
          item.phaseId === this.activePhaseId &&
          item.partId === this.activePartId
      );
      if (idx > 0) {
        const prev = all[idx - 1];
        this.selectPart(prev.phaseId, prev.partId);
      }
    },

    goToNextPart() {
      const all = this.getAllParts();
      const idx = all.findIndex(
        (item) =>
          item.phaseId === this.activePhaseId &&
          item.partId === this.activePartId
      );
      if (idx !== -1 && idx < all.length - 1) {
        const next = all[idx + 1];
        this.selectPart(next.phaseId, next.partId);
      }
    },

    async copyText(text, targetId) {
      let success = false;
      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(text);
          success = true;
        } catch (err) {
          console.warn("navigator.clipboard failed, using fallback...", err);
        }
      }

      if (!success) {
        try {
          const textArea = document.createElement("textarea");
          textArea.value = text;
          textArea.style.position = "fixed";
          textArea.style.left = "-999999px";
          textArea.style.top = "-999999px";
          textArea.setAttribute("readonly", "");
          document.body.appendChild(textArea);
          textArea.focus();
          textArea.select();
          success = document.execCommand("copy");
          document.body.removeChild(textArea);
        } catch (err) {
          console.error("All copy methods failed:", err);
        }
      }

      if (success) {
        this.copiedTarget = targetId;
        setTimeout(() => {
          if (this.copiedTarget === targetId) {
            this.copiedTarget = null;
          }
        }, 2000);
      }
    },

    copyAllPartCommands(part) {
      const allCode = part.steps.map((s) => s.code).join("\n\n");
      this.copyText(allCode, "part-all-" + part.id);
    },

    phases: [
      {
        id: "phase1",
        number: "01",
        title: "SSH Keys & Droplet Sizing",
        target: "Local Machine & DigitalOcean Console",
        desc: "Local key generation and hardware sizing specs.",
        theme: {
          text: "text-sky-400",
          borderLeft: "border-sky-500",
          activeBorder: "border-sky-500/60",
          cardBg: "bg-sky-500/[0.04]",
          badge: "bg-sky-500/10 text-sky-300 border-sky-500/30",
          badgeActive: "bg-sky-500 text-white border-sky-400",
          partActive: "bg-sky-500 text-white",
          bullet: "bg-sky-400",
        },
        parts: [
          {
            id: "phase1-a",
            letter: "A",
            shortTitle: "Creating SSH Keys",
            tabName: "SSH Keys",
            title: "Creating SSH Keys on Local Machine",
            why: `<p>SSH keys allow passwordless, encrypted login to your droplet. If you choose not to use keys, DigitalOcean will email an initial root password to your account.</p>`,
            steps: [
              {
                heading: "Generate Keypair Locally",
                note: `<p>You can choose to create SSH keys to login if you want. If not, you will get the password sent to your email by Digitalocean to login via to server console.</p>
<p>To generate a key on your local machine, hit enter all the way through and it will create a public and private key:</p>`,
                lang: "bash",
                code: `ssh-keygen`,
              },
              {
                heading: "View & Copy Public Key",
                note: `<p>View and copy the public key (<code>.pub</code> file) to paste into DigitalOcean:</p>`,
                lang: "bash",
                code: `cat ~/.ssh/id_rsa.pub`,
              },
            ],
          },
          {
            id: "phase1-b",
            letter: "B",
            shortTitle: "Droplet Provisioning",
            tabName: "Droplet Specs",
            title: "Droplet Provisioning & Sizing Specs",
            why: `<p><strong>Why this size?</strong></p>
<p>Next.js 16 and Tailwind CSS 4 compilation (<code>npm run build</code>) requires significant memory during tree-shaking and bundling. Additionally, the backend uses ChromaDB for local vector embeddings (<code>all-MiniLM-L6-v2</code>), which downloads model weights into RAM on first query. A 1 GB droplet will encounter an Out-Of-Memory (OOM) crash unless protected by swap space.</p>`,
            steps: [
              {
                heading: "Create the Droplet in DigitalOcean",
                note: `<p>Follow these steps in your DigitalOcean account console:</p>
<ol>
  <li>In DigitalOcean, navigate to <strong>Create</strong> &gt; <strong>Droplets</strong>.</li>
  <li><strong>Distribution:</strong> Select <strong>Ubuntu 24.04 LTS x64</strong>.</li>
  <li><strong>Droplet Sizing:</strong>
    <ul>
      <li><strong>Recommended:</strong> <strong>2 GB RAM / 1 CPU Basic Droplet</strong>.</li>
      <li><strong>Budget:</strong> <strong>1 GB RAM / 1 CPU</strong>.</li>
    </ul>
  </li>
  <li><strong>Authentication:</strong> Choose <strong>SSH Key</strong> (preferred) or Root Password.</li>
  <li>Create the Droplet and note your server IP address (<code>YOUR_SERVER_IP</code>).</li>
</ol>`,
                lang: "bash",
                code: `# Note your assigned public IP address:
export YOUR_SERVER_IP="your_server_ip_here"`,
              },
            ],
          },
        ],
      },
      {
        id: "phase2",
        number: "02",
        title: "Security Hardening & User Setup",
        target: "Ubuntu Host & /etc/ssh/sshd_config",
        desc: "Root setup, dedicated voiceadmin user, authorized_keys, disable root login.",
        theme: {
          text: "text-emerald-400",
          borderLeft: "border-emerald-500",
          activeBorder: "border-emerald-500/60",
          cardBg: "bg-emerald-500/[0.04]",
          badge: "bg-emerald-500/10 text-emerald-300 border-emerald-500/30",
          badgeActive: "bg-emerald-500 text-white border-emerald-400",
          partActive: "bg-emerald-500 text-white",
          bullet: "bg-emerald-400",
        },
        parts: [
          {
            id: "phase2-a",
            letter: "A",
            shortTitle: "Create Service User",
            tabName: "Service User",
            title: "Log in as Root & Create Dedicated Service User",
            why: `<p><strong>Why create a dedicated service user?</strong></p>
<p>Running production web servers as <code>root</code> is a security risk. If an application service is compromised, restricting it to an unprivileged user prevents an attacker from having full system control over the entire operating system and filesystem.</p>`,
            steps: [
              {
                heading: "Step 1: Security Hardening & User Setup (Root Login)",
                note: `<p>Log in to the droplet as <code>root</code>:</p>`,
                lang: "bash",
                code: `ssh root@YOUR_SERVER_IP`,
              },
              {
                heading: "Step 2: Create a Dedicated Service User",
                note: `<p>Create a non-root administrative user named <code>voiceadmin</code>:</p>
<p><em>(Enter a strong password. You can press <code>Enter</code> through the optional contact details).</em></p>`,
                lang: "bash",
                code: `adduser voiceadmin`,
              },
              {
                heading: "Add voiceadmin to Sudo Group",
                note: `<p>Grant administrative sudo privileges to <code>voiceadmin</code>:</p>`,
                lang: "bash",
                code: `usermod -aG sudo voiceadmin`,
              },
            ],
          },
          {
            id: "phase2-b",
            letter: "B",
            shortTitle: "Authorize SSH Keys",
            tabName: "SSH Key Auth",
            title: "Setup and Authorize SSH Keys for voiceadmin",
            why: `<p><strong>Why authorize SSH key for voiceadmin?</strong></p>
<p>This allows you to SSH directly into <code>voiceadmin</code> with the same key pair you used for root, keeping root login completely disabled.</p>`,
            steps: [
              {
                heading: "Step 3: Setup SSH Directory & Authorized Keys File",
                note: `<p>Setup SSH keys for the new user. You will need to get them from your local machine using: <code>cat ~/.ssh/id_rsa.pub</code></p>
<p>Navigate to the new user's home folder and create the <code>.ssh</code> directory:</p>`,
                lang: "bash",
                code: `cd /home/voiceadmin
mkdir .ssh
cd .ssh`,
              },
              {
                heading: "Paste Public Key into authorized_keys",
                note: `<p>Open the file, paste your public key, then hit <code>Ctrl+X</code>, <code>Y</code> to save and <code>Enter</code> to exit:</p>`,
                lang: "bash",
                code: `nano authorized_keys`,
              },
              {
                heading: "Step 4: Set Strict Permissions for .ssh",
                note: `<p>Set ownership and strict file mode permissions so SSH allows key-based login:</p>`,
                lang: "bash",
                code: `sudo chown -R voiceadmin:voiceadmin /home/voiceadmin/.ssh
sudo chmod 700 /home/voiceadmin/.ssh
sudo chmod 600 /home/voiceadmin/.ssh/authorized_keys`,
              },
            ],
          },
          {
            id: "phase2-c",
            letter: "C",
            shortTitle: "Disable Root Login",
            tabName: "Disable Root",
            title: "Disable Root SSH Login & Password Authentication",
            why: `<p>Disabling root login and password authentication ensures that automated brute-force attacks on port 22 cannot succeed without your private SSH key.</p>`,
            steps: [
              {
                heading: "Open SSH Daemon Configuration",
                note: `<p>Edit <code>/etc/ssh/sshd_config</code>:</p>`,
                lang: "bash",
                code: `sudo nano /etc/ssh/sshd_config`,
              },
              {
                heading: "Directives to Update",
                note: `<p>Locate these directives inside the file and change both to <code>no</code>:</p>`,
                lang: "text",
                code: `PermitRootLogin no
PasswordAuthentication no`,
              },
              {
                heading: "Reload SSH Daemon",
                note: `<p>Save and exit (<code>Ctrl+O</code>, <code>Enter</code>, <code>Ctrl+X</code>), then reload the SSH service:</p>`,
                lang: "bash",
                code: `systemctl reload ssh`,
              },
              {
                heading: "Verify Connection in a Second Terminal",
                note: `<p>Open a second terminal window on your local machine and verify you can connect (<em>Keep your root terminal open until this verification succeeds</em>):</p>`,
                lang: "bash",
                code: `ssh voiceadmin@YOUR_SERVER_IP`,
              },
            ],
          },
        ],
      },
      {
        id: "phase3",
        number: "03",
        title: "Virtual Memory (Swap Space)",
        target: "/swapfile & /etc/fstab",
        desc: "4GB disk swap allocation to protect compilation and vector searches.",
        theme: {
          text: "text-amber-400",
          borderLeft: "border-amber-500",
          activeBorder: "border-amber-500/60",
          cardBg: "bg-amber-500/[0.04]",
          badge: "bg-amber-500/10 text-amber-300 border-amber-500/30",
          badgeActive: "bg-amber-500 text-white border-amber-400",
          partActive: "bg-amber-500 text-white",
          bullet: "bg-amber-400",
        },
        parts: [
          {
            id: "phase3-a",
            letter: "A",
            shortTitle: "4GB Swap Setup",
            tabName: "Swap Space",
            title: "Configure Virtual Memory (4GB Swap Space)",
            why: `<p><strong>Why?</strong></p>
<p>Building the Next.js frontend with React 19 and installing dependencies takes more RAM than a basic droplet has available. The 4GB swap partition acts as virtual disk-backed memory, preventing the Linux kernel OOM-killer from abruptly terminating <code>npm run build</code> or the Python Uvicorn process.</p>`,
            steps: [
              {
                heading: "Allocate 4GB Swap File",
                note: `<p>Run these commands as <code>voiceadmin</code> (using <code>sudo</code>):</p>`,
                lang: "bash",
                code: `sudo fallocate -l 4G /swapfile`,
              },
              {
                heading: "Set Permissions & Initialize Swap",
                note: `<p>Lock permissions to root, format as swap space, and activate:</p>`,
                lang: "bash",
                code: `sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile`,
              },
              {
                heading: "Make Swap Permanent in /etc/fstab",
                note: `<p>Append the entry to <code>/etc/fstab</code> so swap persists across server reboots:</p>`,
                lang: "bash",
                code: `echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab`,
              },
            ],
          },
        ],
      },
      {
        id: "phase4",
        number: "04",
        title: "Dependencies, Node.js & uv",
        target: "APT Packages, NodeSource & Astral uv",
        desc: "System packages, ffmpeg, Node.js v22 LTS, and Astral uv.",
        theme: {
          text: "text-purple-400",
          borderLeft: "border-purple-500",
          activeBorder: "border-purple-500/60",
          cardBg: "bg-purple-500/[0.04]",
          badge: "bg-purple-500/10 text-purple-300 border-purple-500/30",
          badgeActive: "bg-purple-500 text-white border-purple-400",
          partActive: "bg-purple-500 text-white",
          bullet: "bg-purple-400",
        },
        parts: [
          {
            id: "phase4-a",
            letter: "A",
            shortTitle: "System Packages & ffmpeg",
            tabName: "System Tools",
            title: "Install System Dependencies & ffmpeg",
            why: `<p><strong>Why ffmpeg?</strong></p>
<p><code>community-voice</code> accepts voice notes in various formats (<code>mp3</code>, <code>m4a</code>, <code>ogg</code>, <code>webm</code>, <code>wav</code>). <code>ffmpeg</code> provides system-level audio format inspection and decoding.</p>`,
            steps: [
              {
                heading: "Update Package Lists & Upgrade Core Software",
                note: `<p>Update existing packages:</p>`,
                lang: "bash",
                code: `sudo apt update && sudo apt upgrade -y`,
              },
              {
                heading: "Install System Build Tools & ffmpeg",
                note: `<p>Installs core development tools, Nginx, UFW, SSL libraries, and ffmpeg:</p>`,
                lang: "bash",
                code: `sudo apt install -y curl git build-essential nginx ufw libssl-dev ffmpeg`,
              },
            ],
          },
          {
            id: "phase4-b",
            letter: "B",
            shortTitle: "Node.js v22 LTS",
            tabName: "Node.js",
            title: "Step 6: Install Node.js (v22 LTS)",
            why: `<p>Next.js 16 requires Node.js version 20.9.0 or higher. Installing via the official NodeSource repository provides the current LTS runtime along with npm.</p>`,
            steps: [
              {
                heading: "Setup NodeSource Repository for Node.js 22",
                note: `<p>Add the NodeSource repository:</p>`,
                lang: "bash",
                code: `curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -`,
              },
              {
                heading: "Install Node.js & npm",
                note: `<p>Install the nodejs package:</p>`,
                lang: "bash",
                code: `sudo apt install -y nodejs`,
              },
              {
                heading: "Verify Installation",
                note: `<p>Check the versions of node and npm:</p>`,
                lang: "bash",
                code: `node -v   # output should be v22.x.x
npm -v    # output should be 10.x.x or higher`,
              },
            ],
          },
          {
            id: "phase4-c",
            letter: "C",
            shortTitle: "Astral uv Manager",
            tabName: "Astral uv",
            title: "Step 7: Install Astral uv (Python Package Manager)",
            why: `<p><strong>Why uv?</strong></p>
<p><code>uv</code> installs and manages standalone Python runtimes (like Python 3.12) automatically in user space without conflicting with Ubuntu's system Python (<code>/usr/bin/python3</code>), and handles deterministic package resolution from <code>uv.lock</code>.</p>`,
            steps: [
              {
                heading: "Install Astral uv",
                note: `<p>The project pins all Python libraries using <code>uv.lock</code>. Install <code>uv</code>:</p>`,
                lang: "bash",
                code: `curl -LsSf https://astral.sh/uv/install.sh | sh`,
              },
              {
                heading: "Source Shell & Verify uv",
                note: `<p>Make <code>uv</code> available in your current terminal session and verify:</p>`,
                lang: "bash",
                code: `source ~/.bashrc
uv --version`,
              },
            ],
          },
        ],
      },
      {
        id: "phase5",
        number: "05",
        title: "Clone Repository & Backend Setup",
        target: "/home/voiceadmin/community-voice-app",
        desc: "Repository clone, Python 3.12, locked sync, .env configuration.",
        theme: {
          text: "text-blue-400",
          borderLeft: "border-blue-500",
          activeBorder: "border-blue-500/60",
          cardBg: "bg-blue-500/[0.04]",
          badge: "bg-blue-500/10 text-blue-300 border-blue-500/30",
          badgeActive: "bg-blue-500 text-white border-blue-400",
          partActive: "bg-blue-500 text-white",
          bullet: "bg-blue-400",
        },
        parts: [
          {
            id: "phase5-a",
            letter: "A",
            shortTitle: "Clone Repository",
            tabName: "Clone Repo",
            title: "Clone the Repository & Set Permissions",
            why: `<p>Cloning into <code>/home/voiceadmin/</code> ensures the unprivileged service user owns all application source code, virtual environment packages, and runtime databases.</p>`,
            steps: [
              {
                heading: "Clone Git Repository",
                note: `<p>Clone the repository into <code>/home/voiceadmin/community-voice-app</code>:</p>`,
                lang: "bash",
                code: `cd /home/voiceadmin
git clone https://github.com/ujblockchain/community-voice-app.git
cd community-voice-app`,
              },
              {
                heading: "Enforce voiceadmin Ownership",
                note: `<p>Ensure ownership recursively belongs to <code>voiceadmin</code>:</p>`,
                lang: "bash",
                code: `sudo chown -R voiceadmin:voiceadmin /home/voiceadmin/community-voice-app`,
              },
            ],
          },
          {
            id: "phase5-b",
            letter: "B",
            shortTitle: "Python 3.12 & uv sync",
            tabName: "Python Runtime",
            title: "Step 8: Install Python 3.12 & Synced Packages",
            why: `<p><strong>What this does:</strong></p>
<p>Downloads an isolated Python 3.12 binary, creates a virtual environment at <code>.venv/</code>, and installs all locked dependencies (FastAPI, LangGraph, LangChain, ChromaDB, Pillow, etc.).</p>`,
            steps: [
              {
                heading: "Install Isolated Python 3.12 Runtime",
                note: `<p>From inside <code>/home/voiceadmin/community-voice-app</code>:</p>`,
                lang: "bash",
                code: `uv python install 3.12`,
              },
              {
                heading: "Synchronize Dependencies from uv.lock",
                note: `<p>Installs exact pinned packages into <code>.venv/</code>:</p>`,
                lang: "bash",
                code: `uv sync`,
              },
            ],
          },
          {
            id: "phase5-c",
            letter: "C",
            shortTitle: ".env Configuration",
            tabName: "Env Keys",
            title: "Step 9: Set Up Production Environment Keys (.env)",
            why: `<p><strong>Why JWT_SECRET matters:</strong></p>
<p>If you leave <code>JWT_SECRET</code> empty or default, any user can forge a signed JSON Web Token and impersonate the administrator role.</p>`,
            steps: [
              {
                heading: "Generate Random JWT Secret",
                note: `<p>Generate a secure 32-byte hexadecimal secret:</p>`,
                lang: "bash",
                code: `openssl rand -hex 32`,
              },
              {
                heading: "Copy Example Environment File",
                note: `<p>Copy <code>.env.example</code> to <code>.env</code> and open the editor:</p>`,
                lang: "bash",
                code: `cp .env.example .env
nano .env`,
              },
              {
                heading: "Configure Environment Variables",
                note: `<p>Paste your values into <code>.env</code>. Save and exit (<code>Ctrl+O</code>, <code>Enter</code>, <code>Ctrl+X</code>):</p>`,
                lang: "ini",
                code: `GEMINI_API_KEY="your_gemini_api_key"
GROQ_API_KEY="your_groq_api_key"
TAVILY_API_KEY="your_tavily_api_key"
JWT_SECRET="paste_the_openssl_generated_string_here"

GEMINI_MODEL="gemini-3.1-flash-lite"
GROQ_MODEL="openai/gpt-oss-20b"

# Optional: LangSmith Observability
# LANGSMITH_TRACING=true
# LANGSMITH_PROJECT=community-voice
# LANGSMITH_API_KEY="your_langsmith_key"`,
              },
            ],
          },
        ],
      },
      {
        id: "phase6",
        number: "06",
        title: "CORS & Database Admin Password",
        target: "FastAPI Middleware & SQLite Admin User",
        desc: "Add droplet IP to FRONTEND_ORIGINS and update seed admin password.",
        theme: {
          text: "text-rose-400",
          borderLeft: "border-rose-500",
          activeBorder: "border-rose-500/60",
          cardBg: "bg-rose-500/[0.04]",
          badge: "bg-rose-500/10 text-rose-300 border-rose-500/30",
          badgeActive: "bg-rose-500 text-white border-rose-400",
          partActive: "bg-rose-500 text-white",
          bullet: "bg-rose-400",
        },
        parts: [
          {
            id: "phase6-a",
            letter: "A",
            shortTitle: "Configure CORS",
            tabName: "CORS Config",
            title: "Step 10: Configure CORS in src/community_voice/api/main.py",
            why: `<p><strong>Why?</strong></p>
<p>Browsers send an <code>Origin: http://YOUR_SERVER_IP</code> header when submitting reports or logging in. If the server IP is not explicitly whitelisted in <code>FRONTEND_ORIGINS</code>, FastAPI rejects incoming citizen and admin requests with an HTTP 400/403 CORS error.</p>`,
            steps: [
              {
                heading: "Open API Main Entrypoint",
                note: `<p>Open <code>src/community_voice/api/main.py</code>:</p>`,
                lang: "bash",
                code: `nano src/community_voice/api/main.py`,
              },
              {
                heading: "Add YOUR_SERVER_IP to FRONTEND_ORIGINS",
                note: `<p>Find the <code>FRONTEND_ORIGINS</code> variable and add your server's IP address (and domain name if using one). Save and exit:</p>`,
                lang: "python",
                code: `FRONTEND_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://YOUR_SERVER_IP",
    # "https://yourdomain.com",  # we will use this at the end or domain name additions
]`,
              },
            ],
          },
          {
            id: "phase6-b",
            letter: "B",
            shortTitle: "Database Seed & Password",
            tabName: "Database Seed",
            title: "Step 11: Seed Database & Change the Default Admin Password",
            why: `<p><strong>Why?</strong></p>
<p><code>community_voice.auth.seed</code> uses public credentials documented in the README. Failing to change the admin password exposes the review queue, personal report text, and municipal routing controls to unauthorized access.</p>`,
            steps: [
              {
                heading: "Seed Database Tables & Accounts",
                note: `<p>The seed script creates the initial database schema in <code>data/app.db</code> and populates the test accounts:</p>`,
                lang: "bash",
                code: `uv run python -m community_voice.auth.seed`,
              },
              {
                heading: "Update Default Admin Password",
                note: `<p>The seed script creates the admin account with the default password <code>AdminPass123</code>. <strong>Update this password immediately:</strong></p>
<p><em>(Note that in the command we use an admin password of blockfrost95. You can change it)</em></p>`,
                lang: "bash",
                code: `uv run python -c "
from community_voice.auth.security import hash_password
from community_voice.db.repository import _connect
new_pw = 'blockfrost95'  
with _connect() as conn:
    conn.execute('UPDATE users SET password_hash = ? WHERE email = ?', 
                 (hash_password(new_pw), 'admin@communityvoice.test'))
print('Admin password updated successfully!')
"`,
              },
            ],
          },
        ],
      },
      {
        id: "phase7",
        number: "07",
        title: "Configure & Build Frontend",
        target: "frontend/.env.local & Next.js Bundle",
        desc: "Set NEXT_PUBLIC_API_URL and compile production assets.",
        theme: {
          text: "text-teal-400",
          borderLeft: "border-teal-500",
          activeBorder: "border-teal-500/60",
          cardBg: "bg-teal-500/[0.04]",
          badge: "bg-teal-500/10 text-teal-300 border-teal-500/30",
          badgeActive: "bg-teal-500 text-white border-teal-400",
          partActive: "bg-teal-500 text-white",
          bullet: "bg-teal-400",
        },
        parts: [
          {
            id: "phase7-a",
            letter: "A",
            shortTitle: "Frontend .env.local",
            tabName: "API URL",
            title: "Step 12: Configure Frontend Environment (frontend/.env.local)",
            why: `<p><strong>Why http://YOUR_SERVER_IP/api?</strong></p>
<p><code>NEXT_PUBLIC_</code> variables are baked into client-side JavaScript at build time. Pointing to <code>http://YOUR_SERVER_IP/api</code> ensures browser requests route through Nginx on standard port 80/443 without needing port 8800 exposed directly to the public internet.</p>`,
            steps: [
              {
                heading: "Create frontend/.env.local",
                note: `<p>Move into the <code>frontend</code> directory and create <code>.env.local</code>:</p>`,
                lang: "bash",
                code: `cd /home/voiceadmin/community-voice-app/frontend
nano .env.local`,
              },
              {
                heading: "Set NEXT_PUBLIC_API_URL",
                note: `<p>Set <code>NEXT_PUBLIC_API_URL</code> to route through your Nginx reverse proxy under the <code>/api</code> prefix (<em>If using a domain with SSL, configure <code>NEXT_PUBLIC_API_URL=https://yourdomain.com/api</code></em>). Save and exit:</p>`,
                lang: "ini",
                code: `NEXT_PUBLIC_API_URL=http://YOUR_SERVER_IP/api`,
              },
            ],
          },
          {
            id: "phase7-b",
            letter: "B",
            shortTitle: "NPM Build",
            tabName: "Production Build",
            title: "Step 13: Install Frontend Dependencies & Compile",
            why: `<p><strong>Why npm run build?</strong></p>
<p><em>DO NOT</em> run <code>npm run dev</code> in production. <code>npm run build</code> performs ahead-of-time compilation, minifies JavaScript/CSS, and produces an optimized production bundle in <code>.next</code>.</p>`,
            steps: [
              {
                heading: "Install NPM Dependencies",
                note: `<p>Install frontend packages:</p>`,
                lang: "bash",
                code: `npm install`,
              },
              {
                heading: "Run Next.js Production Build",
                note: `<p>Compile and optimize the bundle, then return to project root:</p>`,
                lang: "bash",
                code: `npm run build
cd /home/voiceadmin/community-voice-app`,
              },
            ],
          },
        ],
      },
      {
        id: "phase8",
        number: "08",
        title: "Daemonize via Systemd",
        target: "/etc/systemd/system/",
        desc: "FastAPI and Next.js background units, auto-restart, and status check.",
        theme: {
          text: "text-orange-400",
          borderLeft: "border-orange-500",
          activeBorder: "border-orange-500/60",
          cardBg: "bg-orange-500/[0.04]",
          badge: "bg-orange-500/10 text-orange-300 border-orange-500/30",
          badgeActive: "bg-orange-500 text-white border-orange-400",
          partActive: "bg-orange-500 text-white",
          bullet: "bg-orange-400",
        },
        parts: [
          {
            id: "phase8-a",
            letter: "A",
            shortTitle: "FastAPI Service",
            tabName: "API Daemon",
            title: "Step 14: Create the FastAPI Service (community-voice-api.service)",
            why: `<p>Systemd ensures your backend starts automatically on boot and restarts if an unhandled error occurs.</p>`,
            steps: [
              {
                heading: "Create FastAPI Unit File",
                note: `<p>Open <code>/etc/systemd/system/community-voice-api.service</code>:</p>`,
                lang: "bash",
                code: `sudo nano /etc/systemd/system/community-voice-api.service`,
              },
              {
                heading: "FastAPI Service Unit Configuration",
                note: `<p>Paste the configuration:</p>`,
                lang: "ini",
                code: `[Unit]
Description=Community Voice FastAPI Backend Service
After=network.target

[Service]
Type=simple
User=voiceadmin
Group=voiceadmin
WorkingDirectory=/home/voiceadmin/community-voice-app
ExecStart=/home/voiceadmin/.local/bin/uv run uvicorn community_voice.api.main:app --host 127.0.0.1 --port 8800 --workers 2
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target`,
              },
            ],
          },
          {
            id: "phase8-b",
            letter: "B",
            shortTitle: "Next.js Service",
            tabName: "Frontend Daemon",
            title: "Step 15: Create the Next.js Service (community-voice-frontend.service)",
            why: `<p>Runs the production Next.js server on loopback port 3000 as <code>voiceadmin</code>, ensuring automatic recovery on crash or host restart.</p>`,
            steps: [
              {
                heading: "Create Next.js Unit File",
                note: `<p>Open <code>/etc/systemd/system/community-voice-frontend.service</code>:</p>`,
                lang: "bash",
                code: `sudo nano /etc/systemd/system/community-voice-frontend.service`,
              },
              {
                heading: "Next.js Service Unit Configuration",
                note: `<p>Paste the configuration:</p>`,
                lang: "ini",
                code: `[Unit]
Description=Community Voice Next.js Frontend Service
After=network.target community-voice-api.service

[Service]
Type=simple
User=voiceadmin
Group=voiceadmin
WorkingDirectory=/home/voiceadmin/community-voice-app/frontend
ExecStart=/usr/bin/npm run start -- -p 3000 -H 127.0.0.1
Restart=always
RestartSec=5
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target`,
              },
            ],
          },
          {
            id: "phase8-c",
            letter: "C",
            shortTitle: "Start & Verify Services",
            tabName: "Start Services",
            title: "Enable, Start & Verify Both Background Services",
            why: `<p>Reloading systemd registers the new units. Enabling them creates symlinks so services auto-start across server reboots.</p>`,
            steps: [
              {
                heading: "Reload Systemd Daemon",
                note: `<p>Tell systemd to read the new unit files:</p>`,
                lang: "bash",
                code: `sudo systemctl daemon-reload`,
              },
              {
                heading: "Enable & Start FastAPI Service",
                note: `<p>Enable and start the backend service:</p>`,
                lang: "bash",
                code: `sudo systemctl enable community-voice-api
sudo systemctl start community-voice-api`,
              },
              {
                heading: "Enable & Start Next.js Service",
                note: `<p>Enable and start the frontend service:</p>`,
                lang: "bash",
                code: `sudo systemctl enable community-voice-frontend
sudo systemctl start community-voice-frontend`,
              },
              {
                heading: "Verify FastAPI Status",
                note: `<p>Verify that the backend is active and running:</p>`,
                lang: "bash",
                code: `sudo systemctl status community-voice-api --no-pager`,
              },
              {
                heading: "Verify Next.js Status",
                note: `<p>Verify that the frontend is active and running:</p>`,
                lang: "bash",
                code: `sudo systemctl status community-voice-frontend --no-pager`,
              },
            ],
          },
        ],
      },
      {
        id: "phase9",
        number: "09",
        title: "Configure Nginx with SSE",
        target: "/etc/nginx/sites-available/community-voice",
        desc: "Reverse proxy, 25MB uploads, unbuffered SSE, rewrite prefix.",
        theme: {
          text: "text-green-400",
          borderLeft: "border-green-500",
          activeBorder: "border-green-500/60",
          cardBg: "bg-green-500/[0.04]",
          badge: "bg-green-500/10 text-green-300 border-green-500/30",
          badgeActive: "bg-green-500 text-white border-green-400",
          partActive: "bg-green-500 text-white",
          bullet: "bg-green-400",
        },
        parts: [
          {
            id: "phase9-a",
            letter: "A",
            shortTitle: "Nginx Server Block",
            tabName: "Nginx Config",
            title: "Step 16: Configure the Nginx Server Block",
            why: `<p>FastAPI streams agent execution steps in real time using Server-Sent Events (<code>/reports</code>, <code>/reports/{id}/review</code>). Standard reverse proxies will buffer and stall these events unless proxy buffering is disabled.</p>`,
            steps: [
              {
                heading: "Create Nginx Configuration File",
                note: `<p>Open <code>/etc/nginx/sites-available/community-voice</code> with <code>sudo nano</code>:</p>`,
                lang: "bash",
                code: `sudo nano /etc/nginx/sites-available/community-voice`,
              },
              {
                heading: "Nginx Server Block Configuration",
                note: `<p>Paste the configuration (replace <code>YOUR_SERVER_IP</code> with your droplet IP or domain):</p>`,
                lang: "nginx",
                code: `server {
    listen 80;
    server_name YOUR_SERVER_IP;

    # allow audio notes (up to 10MB) and photos (up to 5MB)
    client_max_body_size 25M;

    # serve static Next.js assets with long-term cache headers
    location /_next/static/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_cache_bypass $http_upgrade;
        expires 365d;
        access_log off;
    }

    # proxy api requests to astAPI on port 8800
    location /api/ {
        # Strip '/api/' prefix so FastAPI receives /auth/login, /reports, etc.
        rewrite ^/api/(.*)$ /$1 break;
        proxy_pass http://127.0.0.1:8800;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # prevent nginx from buffering server-sent events (sse)
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
        chunked_transfer_encoding off;
    }

    # proxy frontend requests to Next.js on port 3000
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}`,
                subWhy: `<p><strong>Explanations:</strong></p>
<ul>
  <li><code>client_max_body_size 25M;</code>: The application accepts voice notes up to 10 MB and photos up to 5 MB. Nginx's default limit is 1 MB. Without this directive, file uploads will fail with <code>413 Request Entity Too Large</code>.</li>
  <li><code>proxy_buffering off;</code>: In standard HTTP responses, Nginx holds bytes in memory before sending them to the client. For SSE, this prevents live status updates from streaming to the browser as agents complete their steps.</li>
  <li><code>rewrite ^/api/(.*)$ /$1 break;</code>: Next.js sends requests to <code>/api/auth/login</code>, but FastAPI defines routes at <code>/auth/login</code>. This directive strips the <code>/api</code> prefix before forwarding.</li>
</ul>`,
              },
            ],
          },
          {
            id: "phase9-b",
            letter: "B",
            shortTitle: "Activate & Reload Nginx",
            tabName: "Reload Nginx",
            title: "Step 17: Enable Configuration & Restart Nginx",
            why: `<p>Validating syntax with <code>nginx -t</code> prevents broken configurations from taking down active web ports.</p>`,
            steps: [
              {
                heading: "Disable Default Site & Symlink Configuration",
                note: `<p>Disable the default welcome page and activate <code>community-voice</code>:</p>`,
                lang: "bash",
                code: `sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/community-voice /etc/nginx/sites-enabled/`,
              },
              {
                heading: "Test Nginx Configuration Syntax",
                note: `<p>Check for syntax errors (should output: <code>nginx: configuration file /etc/nginx/nginx.conf test is successful</code>):</p>`,
                lang: "bash",
                code: `sudo nginx -t`,
              },
              {
                heading: "Restart Nginx Service",
                note: `<p>Reload Nginx to apply changes:</p>`,
                lang: "bash",
                code: `sudo systemctl restart nginx`,
              },
            ],
          },
        ],
      },
      {
        id: "phase10",
        number: "10",
        title: "Configure UFW Firewall",
        target: "Ubuntu Firewall (ufw)",
        desc: "Restrict server access to SSH (22) and Web traffic (80/443).",
        theme: {
          text: "text-red-400",
          borderLeft: "border-red-500",
          activeBorder: "border-red-500/60",
          cardBg: "bg-red-500/[0.04]",
          badge: "bg-red-500/10 text-red-300 border-red-500/30",
          badgeActive: "bg-red-500 text-white border-red-400",
          partActive: "bg-red-500 text-white",
          bullet: "bg-red-400",
        },
        parts: [
          {
            id: "phase10-a",
            letter: "A",
            shortTitle: "Apply Firewall Rules",
            tabName: "UFW Rules",
            title: "Configure UFW Firewall Rules",
            why: `<p><strong>Why?</strong></p>
<p>Direct access to internal services on port 8800 (FastAPI) and port 3000 (Next.js) is blocked from the outside world. All external traffic must pass through Nginx on port 80/443.</p>`,
            steps: [
              {
                heading: "Set Default Incoming & Outgoing Policies",
                note: `<p>Deny incoming traffic by default and allow outgoing:</p>`,
                lang: "bash",
                code: `sudo ufw default deny incoming
sudo ufw default allow outgoing`,
              },
              {
                heading: "Allow OpenSSH & Nginx Full",
                note: `<p>Permit port 22 (SSH) and ports 80/443 (HTTP/HTTPS):</p>`,
                lang: "bash",
                code: `sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'`,
              },
              {
                heading: "Enable Firewall & Check Status",
                note: `<p>Enable UFW and display active rules:</p>`,
                lang: "bash",
                code: `sudo ufw --force enable
sudo ufw status`,
              },
            ],
          },
        ],
      },
      {
        id: "phase11",
        number: "11",
        title: "Verification & End-to-End Testing",
        target: "Browser Smoke Test & Endpoints",
        desc: "Check /api/health, sign in with blockfrost95, test report submission.",
        theme: {
          text: "text-lime-400",
          borderLeft: "border-lime-500",
          activeBorder: "border-lime-500/60",
          cardBg: "bg-lime-500/[0.04]",
          badge: "bg-lime-500/10 text-lime-300 border-lime-500/30",
          badgeActive: "bg-lime-500 text-white border-lime-400",
          partActive: "bg-lime-500 text-white",
          bullet: "bg-lime-400",
        },
        parts: [
          {
            id: "phase11-a",
            letter: "A",
            shortTitle: "Backend Health Check",
            tabName: "Health Check",
            title: "1. Verify Backend Health",
            why: `<p>Checks whether the reverse proxy rewrite rule correctly reaches Uvicorn on port 8800 and returns a valid JSON health response.</p>`,
            steps: [
              {
                heading: "Test /api/health Endpoint with cURL",
                note: `<p>Visit <code>http://YOUR_SERVER_IP/api/health</code> directly. It should return:</p>
<pre class="bg-black/40 p-2 rounded text-xs">{"status":"ok"}</pre>`,
                lang: "bash",
                code: `curl http://YOUR_SERVER_IP/api/health`,
              },
            ],
          },
          {
            id: "phase11-b",
            letter: "B",
            shortTitle: "Admin Sign-In",
            tabName: "Admin Test",
            title: "2. Test Admin Sign-In & Dashboard",
            why: `<p>Verifies JWT token issuance, cookie handling through Nginx, and permission to query the SQLite review queue.</p>`,
            steps: [
              {
                heading: "Open Admin Sign-In URL",
                note: `<p>Navigate in your browser to <code>http://YOUR_SERVER_IP/login</code>:</p>`,
                lang: "bash",
                code: `http://YOUR_SERVER_IP/login`,
              },
              {
                heading: "Admin Credentials",
                note: `<p>Sign in with your seeded administrator credentials:</p>
<ul>
  <li><strong>Email:</strong> <code>admin@communityvoice.test</code></li>
  <li><strong>Password:</strong> <code>blockfrost95</code> (or the one you created)</li>
  <li>Verify you land on the <strong>Review Queue</strong> (<code>/review</code>) and can view the <strong>Dashboard</strong> (<code>/dashboard</code>).</li>
</ul>`,
                lang: "text",
                code: `Email: admin@communityvoice.test
Password: blockfrost95`,
              },
            ],
          },
          {
            id: "phase11-c",
            letter: "C",
            shortTitle: "Citizen SSE Stream",
            tabName: "SSE Report Test",
            title: "3. Test Report Submission & SSE Streaming",
            why: `<p>Verifies that Nginx does not buffer Server-Sent Events, allowing each agent step (Triage, Routing, Context Check, Duplicate Check) to stream to the citizen UI in real time.</p>`,
            steps: [
              {
                heading: "Citizen Login & Submission URL",
                note: `<p>Log out of admin and sign in as a citizen:</p>
<ul>
  <li><strong>Email:</strong> <code>citizen1@communityvoice.test</code></li>
  <li><strong>Password:</strong> <code>Citizen1Pass123</code></li>
  <li>Go to <strong>Submit a Report</strong> (<code>/submit</code>):</li>
</ul>`,
                lang: "bash",
                code: `http://YOUR_SERVER_IP/submit`,
              },
              {
                heading: "Verify Agent Execution Stream",
                note: `<p>Pick a sample report (or type one) and click <strong>Submit report</strong>. Verify that the agent steps stream live in sequence in the progress box:</p>`,
                lang: "text",
                code: `Triage -> Routing -> Context Check -> Duplicate Check`,
              },
            ],
          },
        ],
      },
      {
        id: "phase12",
        number: "12",
        title: "Logs, Updates & SSL",
        target: "Maintenance, Git & Let's Encrypt",
        desc: "journalctl logging, git pull deployment script, and Certbot SSL.",
        theme: {
          text: "text-fuchsia-400",
          borderLeft: "border-fuchsia-500",
          activeBorder: "border-fuchsia-500/60",
          cardBg: "bg-fuchsia-500/[0.04]",
          badge: "bg-fuchsia-500/10 text-fuchsia-300 border-fuchsia-500/30",
          badgeActive: "bg-fuchsia-500 text-white border-fuchsia-400",
          partActive: "bg-fuchsia-500 text-white",
          bullet: "bg-fuchsia-400",
        },
        parts: [
          {
            id: "phase12-a",
            letter: "A",
            shortTitle: "Checking Service Logs",
            tabName: "Service Logs",
            title: "Checking Service Logs",
            why: `<p>Fast access to systemd and web server logs is essential for diagnosing unhandled API exceptions or reverse proxy connection drops.</p>`,
            steps: [
              {
                heading: "FastAPI Backend & Agent Trace Logs",
                note: `<p>Inspect live FastAPI backend errors or agent traces:</p>`,
                lang: "bash",
                code: `sudo journalctl -u community-voice-api -f`,
              },
              {
                heading: "Next.js Server Logs",
                note: `<p>Inspect live Next.js server logs:</p>`,
                lang: "bash",
                code: `sudo journalctl -u community-voice-frontend -f`,
              },
              {
                heading: "Nginx Error Logs",
                note: `<p>Inspect live Nginx web server errors:</p>`,
                lang: "bash",
                code: `sudo tail -f /var/log/nginx/error.log`,
              },
            ],
          },
          {
            id: "phase12-b",
            letter: "B",
            shortTitle: "Deploying Code Updates",
            tabName: "Code Updates",
            title: "Deploying Future Code Updates",
            why: `<p>Ensures a deterministic process for pulling updates from git without leaving dangling build artifacts or service interruptions.</p>`,
            steps: [
              {
                heading: "Pull Latest Changes from Git",
                note: `<p>When you push code updates to <code>https://github.com/ujblockchain/community-voice-app</code>, update the droplet:</p>`,
                lang: "bash",
                code: `cd /home/voiceadmin/community-voice-app
git pull origin main`,
              },
              {
                heading: "Update Backend Dependencies",
                note: `<p>Update backend dependencies if <code>pyproject.toml</code> or <code>uv.lock</code> changed:</p>`,
                lang: "bash",
                code: `uv sync`,
              },
              {
                heading: "Rebuild Frontend Assets",
                note: `<p>Rebuild frontend if <code>frontend/src</code> or <code>package.json</code> changed:</p>`,
                lang: "bash",
                code: `cd frontend
npm install
npm run build
cd ..`,
              },
              {
                heading: "Restart Both Services",
                note: `<p>Restart both application background services:</p>`,
                lang: "bash",
                code: `sudo systemctl restart community-voice-api
sudo systemctl restart community-voice-frontend`,
              },
            ],
          },
          {
            id: "phase12-c",
            letter: "C",
            shortTitle: "Custom Domain & SSL",
            tabName: "Certbot SSL",
            title: "Custom Domain & Free SSL (Certbot)",
            why: `<p>Production web applications handling citizen voice notes and credentials must encrypt all traffic in transit via TLS.</p>`,
            steps: [
              {
                heading: "Install Certbot for Nginx",
                note: `<p>Install Certbot and the Python Nginx plugin:</p>`,
                lang: "bash",
                code: `sudo apt install -y certbot python3-certbot-nginx`,
              },
              {
                heading: "Request SSL Certificate",
                note: `<p>Ensure your DNS A-Record points to <code>YOUR_SERVER_IP</code>, update <code>server_name</code> in Nginx and <code>FRONTEND_ORIGINS</code> in <code>main.py</code>, then obtain the certificate:</p>`,
                lang: "bash",
                code: `sudo certbot --nginx -d reports.yourdomain.com`,
              },
              {
                heading: "Restart All Services",
                note: `<p>Restart services to complete the SSL activation:</p>`,
                lang: "bash",
                code: `sudo systemctl restart community-voice-api
sudo systemctl restart community-voice-frontend
sudo systemctl restart nginx`,
              },
            ],
          },
        ],
      },
    ],
  }));
});

(async () => {
  if (window.tsParticles) {
    await window.tsParticles.load("particles-container", {
      background: { color: { value: "transparent" } },
      fpsLimit: 60,
      particles: {
        color: { value: ["#ffffff", "#F26522"] },
        links: {
          color: "#ffffff",
          distance: 130,
          enable: true,
          opacity: 0.08,
          width: 1,
        },
        move: { enable: true, speed: 0.5 },
        number: { density: { enable: true, area: 900 }, value: 30 },
        opacity: { value: 0.25 },
        shape: { type: "circle" },
        size: { value: { min: 1, max: 2.5 } },
      },
    });
  }
})();