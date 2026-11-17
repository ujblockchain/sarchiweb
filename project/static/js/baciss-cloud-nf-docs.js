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
      return ph.parts.find((pt) => pt.id === this.activePartId) || ph.parts[0];
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
          item.partId === this.activePartId,
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
          item.partId === this.activePartId,
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
        title: "Repository & Docker Manifests",
        target: "Project Root & frontend/",
        desc: "Dockerfile.backend, frontend/Dockerfile, and GitHub push.",
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
            shortTitle: "Dockerfile.backend",
            tabName: "Backend Dockerfile",
            title: "Step 1: Create Dockerfile.backend in the project root",
            why: `<ol>
  <li><strong><code>python:3.12-slim</code>:</strong> Keeps the container image compact (~200MB vs ~1GB) while providing the exact Python 3.12 runtime required.</li>
  <li><strong><code>ffmpeg</code>:</strong> The application accepts voice notes in various formats (<code>mp3</code>, <code>ogg</code>, <code>m4a</code>, <code>webm</code>, <code>wav</code>). Python audio libraries require system-level <code>ffmpeg</code> to inspect and decode these audio streams.</li>
  <li><strong><code>COPY --from=.../uv /bin/uv</code>:</strong> Copying the precompiled standalone <code>uv</code> binary avoids installing Python packaging build tools via <code>pip</code>, ensuring fast, deterministic installation from <code>uv.lock</code>.</li>
  <li><strong>Layer Caching (<code>COPY pyproject.toml uv.lock ./</code> before <code>COPY . .</code>):</strong> Docker caches layers. By copying dependency manifests and running <code>uv sync</code> <em>before</em> copying the rest of your code, Northflank's CI/CD builds will take only 15–30 seconds on subsequent commits because it skips reinstalling packages when only application code changes.</li>
  <li><strong><code>--host 0.0.0.0</code>:</strong> Binding Uvicorn to <code>0.0.0.0</code> (rather than <code>127.0.0.1</code> or <code>localhost</code>) is required inside containers so Northflank's ingress router can forward network traffic into the container.</li>
</ol>`,
            steps: [
              {
                heading: "Create Dockerfile.backend in Project Root",
                note: `<p><code>Dockerfile.backend</code> is needed for backend deployment:</p>`,
                lang: "docker",
                code: `FROM python:3.12-slim

WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    ffmpeg \\
    libssl-dev \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# install astral uv directly from official binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# copy dependency files first to leverage docker layer caching
COPY pyproject.toml uv.lock ./

# install locked dependencies without installing the project root yet
RUN uv sync --frozen --no-install-project

# copy remaining application source code
COPY . .

# finalize uv installation
RUN uv sync --frozen

# ensure sqlite data directory exists
RUN mkdir -p /app/data

EXPOSE 8800

CMD ["uv", "run", "uvicorn", "community_voice.api.main:app", "--host", "0.0.0.0", "--port", "8800"]`,
              },
            ],
          },
          {
            id: "phase1-b",
            letter: "B",
            shortTitle: "frontend/Dockerfile",
            tabName: "Frontend Dockerfile",
            title:
              "Step 2: Create frontend/Dockerfile (in the frontend/ directory)",
            why: `<ol>
  <li><strong><code>ARG NEXT_PUBLIC_API_URL</code> &amp; <code>ENV NEXT_PUBLIC_API_URL</code>:</strong> Next.js compiles all variables starting with <code>NEXT_PUBLIC_</code> directly into the frontend client-side JavaScript bundle <em>during the <code>npm run build</code> step</em>. If this argument is missing during <code>docker build</code>, the frontend defaults to <code>http://localhost:8800</code>, causing browser requests on the deployed site to fail with <code>Cannot reach the server</code>.</li>
  <li><strong><code>npm run build</code> &amp; <code>npm start</code>:</strong> Runs Next.js in production mode. Running development mode (<code>npm run dev</code>) in production consumes excessive RAM, lacks minification, and exposes internal source maps.</li>
</ol>`,
            steps: [
              {
                heading: "Create frontend/Dockerfile",
                note: `<p><code>Dockerfile</code> is needed to deploy the <code>frontend/</code>:</p>`,
                lang: "docker",
                code: `FROM node:22-slim

WORKDIR /app

# copy dependency manifests
COPY package*.json ./

# clean installation of dependencies
RUN npm install

# copy frontend source code
COPY . .

# next.js requires public api url at build time for client-side embedding
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# build optimized production bundle
RUN npm run build

EXPOSE 3000

ENV PORT=3000
ENV NODE_ENV=production

CMD ["npm", "start"]`,
              },
            ],
          },
          {
            id: "phase1-c",
            letter: "C",
            shortTitle: "Commit & Push",
            tabName: "Git Push",
            title: "Step 3: Commit and Push to GitHub",
            why: `<p>Northflank's CI/CD builds images directly from your remote GitHub branch (<code>main</code>). The files must exist on GitHub for Northflank to detect and verify them.</p>`,
            steps: [
              {
                heading: "Push Manifests to Remote GitHub Branch",
                note: `<p>Stage, commit, and push both Dockerfiles to <code>origin main</code>:</p>`,
                lang: "bash",
                code: `git add Dockerfile.backend frontend/Dockerfile src/community_voice/api/main.py
git commit -m "chore: configure Northflank build manifests and CORS"
git push origin main`,
              },
            ],
          },
        ],
      },
      {
        id: "phase2",
        number: "02",
        title: "Northflank Project & Storage",
        target: "Northflank Dashboard & Persistent Volume",
        desc: "Create project namespace and 6GB SSD volume mounted at /app/data.",
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
            id: "phase2-a",
            letter: "A",
            shortTitle: "Create Project",
            tabName: "Project Setup",
            title: "Step 4: Create a Northflank Project",
            why: `<p>A Northflank Project establishes an isolated Kubernetes namespace where your backend, frontend, and persistent disks share a secure private network and lifecycle management.</p>`,
            steps: [
              {
                heading: "Project Setup in Dashboard",
                note: `<p>Follow these steps in Northflank:</p>
<ol>
  <li>In Northflank, click <strong>Create Project</strong>.</li>
  <li>Name it <code>community-voice</code> and select region <strong>Europe - West (London)</strong>.</li>
</ol>`,
                lang: "text",
                code: `Project Name: community-voice
Region: Europe - West (London)`,
              },
            ],
          },
          {
            id: "phase2-b",
            letter: "B",
            shortTitle: "Persistent Volume",
            tabName: "Persistent SSD",
            title: "Step 5: Create a Persistent Storage Volume",
            why: `<ul>
  <li><strong>Containers are ephemeral:</strong> In cloud PaaS environments like Northflank, when a new commit is pushed, the old container is destroyed and replaced with a fresh one.</li>
  <li>The application stores SQLite databases (<code>app.db</code>, <code>checkpoints.db</code>, <code>memory.db</code>), ChromaDB vector embeddings (<code>data/chroma/</code>), and uploaded photos inside <code>data/</code>.</li>
  <li>Without a persistent volume, <strong>every automated deployment wipes all citizen reports, admin reviews, and user accounts</strong>. Mounting this volume ensures your data survives redeployments permanently.</li>
  <li><strong>Mount Path <code>/app/data</code>:</strong> In <code>src/community_voice/core/config.py</code>, database paths resolve to <code>/app/data/app.db</code>. Mounting the volume at <code>/app/data</code> attaches the persistent SSD directly to that folder.</li>
</ul>`,
            steps: [
              {
                heading: "Create & Mount Storage Volume",
                note: `<p>Inside your project:</p>
<ol>
  <li>Click <strong>Volumes</strong> &gt; <strong>Create Volume</strong>.</li>
  <li><strong>Name:</strong> <code>community-voice-data</code></li>
  <li><strong>Storage Size:</strong> <code>6 GB</code>.</li>
  <li><strong>Mount Path:</strong> <code>/app/data</code></li>
  <li>Click <strong>Create Volume</strong>.</li>
</ol>`,
                lang: "text",
                code: `Volume Name: community-voice-data
Storage Size: 6 GB
Mount Path: /app/data`,
              },
            ],
          },
        ],
      },
      {
        id: "phase3",
        number: "03",
        title: "Deploy Backend Service",
        target: "community-voice-api (Port 8800)",
        desc: "Configure build context, runtime environment keys, and verify /health.",
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
            id: "phase3-a",
            letter: "A",
            shortTitle: "Configure Backend",
            tabName: "Launch Backend",
            title:
              "Step 6: Configure & Launch the Backend (community-voice-api)",
            why: `<ol>
  <li><strong>Context <code>/</code> &amp; Location <code>/Dockerfile.backend</code>:</strong> Tells Northflank to provide the entire repository as the build context (needed so <code>src/</code> and <code>uv.lock</code> are accessible) while explicitly using your custom backend Dockerfile.</li>
  <li><strong>Port 8800 (Public):</strong> Uvicorn runs on port 8800. Enabling public access instructs Northflank's ingress controller to route an HTTPS domain to this internal container port.</li>
  <li><strong>Environment Variables:</strong> FastAPI uses Pydantic's <code>BaseSettings</code>. If keys like <code>GEMINI_API_KEY</code> are missing at runtime, the application will refuse to start and crash with a validation error.</li>
</ol>`,
            steps: [
              {
                heading: "Configure Backend Service Details",
                note: `<p>In Northflank, click <strong>Services</strong> &gt; <strong>Create Service</strong>:</p>
<ol>
  <li><strong>Basic Information:</strong> Service Name: <code>community-voice-api</code></li>
  <li><strong>Source:</strong> Repository: <code>community-voice-app</code> &bull; Branch: <code>main</code></li>
  <li><strong>Build Options:</strong>
    <ul>
      <li><strong>Build Type:</strong> <code>Dockerfile</code></li>
      <li><strong>Build Context:</strong> <code>/</code> <em>(the repository root)</em></li>
      <li><strong>Dockerfile Location:</strong> <code>/Dockerfile.backend</code></li>
      <li>Click <strong>Verify</strong> until it says <em>"Dockerfile loaded"</em>.</li>
    </ul>
  </li>
  <li><strong>Networking:</strong> Click <strong>Add Port</strong> &bull; Port: <code>8800</code> &bull; Protocol: <code>HTTP</code> &bull; Public Access: <strong>Enabled</strong>.</li>
</ol>`,
                lang: "text",
                code: `Service Name: community-voice-api
Branch: main
Build Type: Dockerfile
Build Context: /
Dockerfile Location: /Dockerfile.backend
Port: 8800 (HTTP, Public Access Enabled)`,
              },
              {
                heading: "Add Runtime Environment Variables",
                note: `<p>Under <strong>Environment variables</strong> &gt; <strong>Runtime variables</strong>, configure:</p>`,
                lang: "ini",
                code: `GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
JWT_SECRET=your_secure_random_32_char_string
GEMINI_MODEL=gemini-3.1-flash-lite
GROQ_MODEL=openai/gpt-oss-20b`,
              },
            ],
          },
          {
            id: "phase3-b",
            letter: "B",
            shortTitle: "Verify Backend",
            tabName: "Verify Health",
            title: "Step 7: Verify the Backend is Live",
            why: `<p>Visiting the root path (<code>/</code>) returns <code>{"detail":"Not Found"}</code> because FastAPI has no <code>@app.get("/")</code> route registered. Testing <code>/health</code> confirms that Uvicorn is healthy, the Python environment is working, and ingress routing is operational.</p>`,
            steps: [
              {
                heading: "Copy Public URL & Test Health Endpoint",
                note: `<p>Once the service status turns green (<strong>Running</strong>), test the endpoints in your browser or with cURL:</p>`,
                lang: "bash",
                code: `# health check returns {"status":"ok"}:
curl https://YOUR_BACKEND_URL.run/health

# interactive Swagger documentation:
# Open in browser: https://YOUR_BACKEND_URL.run/docs`,
              },
            ],
          },
        ],
      },
      {
        id: "phase4",
        number: "04",
        title: "Deploy Frontend Service",
        target: "community-voice-frontend (Port 3000)",
        desc: "Build context /frontend, NEXT_PUBLIC_API_URL build argument, public port 3000.",
        theme: {
          text: "text-cyan-400",
          borderLeft: "border-cyan-500",
          activeBorder: "border-cyan-500/60",
          cardBg: "bg-cyan-500/[0.04]",
          badge: "bg-cyan-500/10 text-cyan-300 border-cyan-500/30",
          badgeActive: "bg-cyan-500 text-white border-cyan-400",
          partActive: "bg-cyan-500 text-white",
          bullet: "bg-cyan-400",
        },
        parts: [
          {
            id: "phase4-a",
            letter: "A",
            shortTitle: "Configure Frontend",
            tabName: "Launch Frontend",
            title:
              "Step 8: Configure & Launch the Frontend (community-voice-frontend)",
            why: `<ol>
  <li><strong>Context <code>/frontend</code> &amp; Location <code>/frontend/Dockerfile</code>:</strong> Next.js lives in the <code>frontend/</code> subfolder. Setting the context to <code>/frontend</code> ensures <code>npm install</code> and <code>npm run build</code> run inside the folder containing <code>package.json</code>.</li>
  <li><strong>Why NO <code>/api</code> in <code>NEXT_PUBLIC_API_URL</code>:</strong>
    <ul>
      <li>On Northflank, your backend is exposed directly at its own domain. FastAPI registers routes at <code>/auth/login</code> and <code>/reports</code>.</li>
      <li>If you set <code>NEXT_PUBLIC_API_URL</code> to <code>.../api</code>, browser calls go to <code>.../api/auth/login</code>, which returns <strong>404 Not Found</strong>.</li>
    </ul>
  </li>
  <li><strong>Why in "Build arguments" instead of "Runtime variables":</strong>
    <ul>
      <li>Next.js compiles client components into static JavaScript files during the <code>build</code> step.</li>
      <li>If you only set <code>NEXT_PUBLIC_API_URL</code> as a runtime variable, it will be missing during <code>npm run build</code>, causing the built site to fail to connect to your backend.</li>
    </ul>
  </li>
</ol>`,
            steps: [
              {
                heading: "Configure Frontend Service",
                note: `<p>Click <strong>Services</strong> &gt; <strong>Create Service</strong> &gt; <strong>Combined Service</strong>:</p>
<ol>
  <li><strong>Basic Information:</strong> Service Name: <code>community-voice-frontend</code></li>
  <li><strong>Source:</strong> Repository: Select the same repo &bull; Branch: <code>main</code></li>
  <li><strong>Build Options:</strong>
    <ul>
      <li><strong>Build Type:</strong> <code>Dockerfile</code></li>
      <li><strong>Build Context:</strong> <code>/frontend</code></li>
      <li><strong>Dockerfile Location:</strong> <code>/frontend/Dockerfile</code></li>
      <li>Click <strong>Verify</strong>.</li>
    </ul>
  </li>
  <li><strong>Networking:</strong> Click <strong>Add Port</strong> &bull; Port: <code>3000</code> &bull; Protocol: <code>HTTP</code> &bull; Public Access: <strong>Enabled</strong>.</li>
</ol>`,
                lang: "text",
                code: `Service Name: community-voice-frontend
Branch: main
Build Type: Dockerfile
Build Context: /frontend
Dockerfile Location: /frontend/Dockerfile
Port: 3000 (HTTP, Public Access Enabled)`,
              },
              {
                heading: "Set NEXT_PUBLIC_API_URL Build Argument",
                note: `<p>Under <strong>Environment variables</strong> &gt; click <strong>Build arguments</strong> tab &gt; click <strong>Add argument</strong>:</p>
<p><em>(Point directly to the root backend URL. <strong>Do not</strong> add <code>/api</code> and <strong>do not</strong> add a trailing slash).</em></p>`,
                lang: "text",
                code: `Key: NEXT_PUBLIC_API_URL
Value: https://YOUR_BACKEND_URL.run`,
              },
            ],
          },
        ],
      },
      {
        id: "phase5",
        number: "05",
        title: "Database Seeding & CORS",
        target: "Container Terminal & main.py",
        desc: "Seed users in container terminal, update admin password, and whitelist frontend origin.",
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
            id: "phase5-a",
            letter: "A",
            shortTitle: "Seed Database",
            tabName: "Seed Accounts",
            title: "Step 9: Run the Database Seeder in the Container",
            why: `<ul>
  <li>FastAPI automatically creates SQLite table definitions (<code>users</code>, <code>reports</code>, <code>reviews</code>) when the app boots up, but <strong>the tables start empty</strong>.</li>
  <li>Without running the seeder, entering valid credentials yields <strong><code>401 Incorrect email or password.</code></strong> because the user record does not exist in the database.</li>
  <li>Running this script populates the default admin and citizen accounts. Because the persistent volume is mounted at <code>/app/data</code>, this data is stored on disk permanently and survives all future CI/CD deployments.</li>
</ul>`,
            steps: [
              {
                heading: "Run Seed Script in Container Terminal",
                note: `<p>In Northflank, open your <strong><code>community-voice-api</code></strong> service, open the terminal window, and run:</p>`,
                lang: "bash",
                code: `uv run python -m community_voice.auth.seed`,
              },
              {
                heading: "Expected Seeder Output",
                note: `<p>Confirms initial seed users are populated into <code>data/app.db</code>:</p>`,
                lang: "text",
                code: `Created: admin@communityvoice.test, citizen1@communityvoice.test, citizen2@communityvoice.test`,
              },
            ],
          },
          {
            id: "phase5-b",
            letter: "B",
            shortTitle: "Update Admin Password",
            tabName: "Admin Password",
            title: "Step 10: Change the Default Admin Password for Production",
            why: `<p>The seed script creates the admin password as <code>AdminPass123</code>. Because the project is public, this password is open knowledge. Updating the password immediately protects administrative access to municipal reports and AI review queues. Note: <em>I am using a password of <code>blockflash#5</code>, you can use another of choice</em>)</p>`,
            steps: [
              {
                heading: "Update Password in SQLite Database",
                note: `<p>In the same container terminal, run:</p>`,
                lang: "bash",
                code: `uv run python -c "
from community_voice.auth.security import hash_password
from community_voice.db.repository import _connect
new_pw = 'blockflash#5'
with _connect() as conn:
    conn.execute('UPDATE users SET password_hash = ? WHERE email = ?', 
                 (hash_password(new_pw), 'admin@communityvoice.test'))
print('Admin password successfully updated!')
"`,
              },
            ],
          },
          {
            id: "phase5-c",
            letter: "C",
            shortTitle: "Configure CORS",
            tabName: "CORS Whitelist",
            title: "Step 11: Configure CORS in src/community_voice/api/main.py",
            why: `<ul>
  <li><strong>Preventing CORS Blocking:</strong> The browser loads your frontend from <code>https://YOUR_FRONTEND_URL.run</code>. When JavaScript in the browser attempts to <code>fetch()</code> data from <code>https://YOUR_BACKEND_URL.run</code>, browsers enforce the <strong>Same-Origin Policy</strong>.</li>
  <li>If FastAPI does not return the <code>Access-Control-Allow-Origin</code> header matching the frontend's domain, the browser blocks the response. Adding the frontend URL to <code>FRONTEND_ORIGINS = [...]</code> ensures FastAPI accepts the request.</li>
</ul>`,
            steps: [
              {
                heading: "Add Frontend Domain to FRONTEND_ORIGINS",
                note: `<p>In <code>src/community_voice/api/main.py</code>, update <code>FRONTEND_ORIGINS</code> and add your frontend link:</p>`,
                lang: "python",
                code: `# In src/community_voice/api/main.py:

FRONTEND_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://YOUR_FRONTEND_URL.run",
]`,
              },
              {
                heading: "Commit & Push Updated CORS Origin",
                note: `<p>Push the CORS change to trigger Northflank's automatic rolling deploy:</p>`,
                lang: "bash",
                code: `git add src/community_voice/api/main.py
git commit -m "fix(cors): whitelist Northflank frontend domain"
git push origin main`,
              },
            ],
          },
        ],
      },
      {
        id: "phase6",
        number: "06",
        title: "Automated CI/CD Lifecycle",
        target: "Git Webhooks & Rolling Deployments",
        desc: "Push to main, Docker layer caching, readiness checks, rolling updates.",
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
            id: "phase6-a",
            letter: "A",
            shortTitle: "CI/CD Lifecycle",
            tabName: "Lifecycle Overview",
            title: "How the Automated CI/CD Lifecycle Operates",
            why: `<p>Now that both services are wired up, Northflank manages zero-downtime rolling deploys, volume persistence, and layer caching automatically on every push.</p>`,
            steps: [
              {
                heading: "Triggering an Automated Deployment",
                note: `<p>When you edit backend or frontend code locally, push your changes to GitHub:</p>`,
                lang: "bash",
                code: `git commit -am "feat: improve citizen report notifications"
git push origin main`,
              },
              {
                heading: "What Northflank Does Automatically",
                note: `<p>Northflank executes the following continuous deployment pipeline:</p>
<ol>
  <li><strong>Detects Webhook:</strong> Listens for GitHub push event on branch <code>main</code>.</li>
  <li><strong>Layer-Cached Build:</strong> Rebuilds the affected container image using cached Docker layers (subsequent builds take 15–30s).</li>
  <li><strong>Readiness Probes:</strong> Runs health checks on the newly spun-up container before routing traffic.</li>
  <li><strong>Zero-Downtime Rollout:</strong> Swaps ingress routing from old container to new container with zero dropped connections.</li>
  <li><strong>Preserves Persistent Data:</strong> Re-attaches your 6 GB SSD volume at <code>/app/data</code> so all citizen reports, reviews, embeddings, and accounts persist permanently.</li>
</ol>`,
                lang: "text",
                code: `Pipeline: Webhook -> Layer-Cached Build -> Readiness Probe -> Rolling Swap -> Re-attach /app/data`,
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
