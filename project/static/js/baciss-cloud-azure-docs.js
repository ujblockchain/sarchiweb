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
        title: "Codebase & Docker Manifests",
        target: "Project Root & frontend/",
        desc: "Dockerfile.backend, frontend/Dockerfile, and CORS configuration.",
        theme: {
          text: "text-blue-400",
          borderLeft: "border-blue-500",
          activeBorder: "border-blue-500/60",
          cardBg: "bg-blue-500/[0.04]",
          badge: "bg-blue-500/10 text-blue-300 border-blue-500/30",
          badgeActive: "bg-blue-600 text-white border-blue-400",
          partActive: "bg-[#0078d4] text-white",
          bullet: "bg-blue-400",
        },
        parts: [
          {
            id: "phase1-a",
            letter: "A",
            shortTitle: "Dockerfile.backend",
            tabName: "Backend Dockerfile",
            title: "Step 1: Create Dockerfile.backend (in project root)",
            why: `<ol>
  <li><strong><code>python:3.12-slim</code>:</strong> Reduces image size from ~1.2 GB to ~220 MB, significantly speeding up container pull times in Azure.</li>
  <li><strong><code>ffmpeg</code>:</strong> Voice notes arrive as <code>.mp3</code>, <code>.m4a</code>, <code>.ogg</code>, or <code>.webm</code>. Audio libraries rely on <code>ffmpeg</code> binary bindings to decode audio streams before sending them to Google Gemini for speech-to-text.</li>
  <li><strong><code>COPY --from=ghcr.io/astral-sh/uv /bin/uv</code>:</strong> Bypasses <code>pip</code>, ensuring the environment builds in seconds directly from <code>uv.lock</code>.</li>
  <li><strong><code>RUN cp -r /app/data /app/data_defaults</code> &amp; Startup check:</strong>
    <ul>
      <li><strong>The Problem:</strong> When Azure mounts an external cloud disk to <code>/app/data</code>, it overlays the empty disk over whatever was inside the container, hiding <code>directory.json</code> and triggering <code>FileNotFoundError: [Errno 2] No such file or directory: '/app/data/knowledge_base/directory.json'</code>.</li>
      <li><strong>The Solution:</strong> We save a backup copy at <code>/app/data_defaults</code>. On container boot, the script checks if <code>/app/data/knowledge_base/directory.json</code> exists. If not (first boot), it copies the default charters, sample reports, and directories onto the Azure File Share.</li>
    </ul>
  </li>
  <li><strong><code>uv run python -m community_voice.auth.seed</code> in <code>CMD</code>:</strong>
    <ul>
      <li><strong>The Problem:</strong> Azure Container Apps serverless instances frequently drop WebSocket terminals with <code>ClusterExecFailure: code 500</code>, making manual CLI seeding unreliable.</li>
      <li><strong>The Solution:</strong> The seed script is <strong>idempotent</strong> (<code>if find_user(email) is None:</code>). Running it automatically on container startup ensures the admin and citizen accounts are seeded into <code>app.db</code> without requiring manual CLI intervention.</li>
    </ul>
  </li>
</ol>`,
            steps: [
              {
                heading: "Create Dockerfile.backend in Project Root",
                note: `<p>Create <code>Dockerfile.backend</code> in the repository root with data restoration and auto-seeding:</p>`,
                lang: "docker",
                code: `FROM python:3.12-slim

WORKDIR /app

# install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \\
    ffmpeg \\
    libssl-dev \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# install astral uv directly from official binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# cache and install python dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# copy application source code
COPY . .
RUN uv sync --frozen

# backup static data directory before volume mount overlay
RUN cp -r /app/data /app/data_defaults

EXPOSE 8800

# startup sequence
# restore static files, seed database & launch uvicorn
CMD ["sh", "-c", "if [ ! -f /app/data/knowledge_base/directory.json ]; then cp -r /app/data_defaults/* /app/data/; fi && uv run python -m community_voice.auth.seed && uv run uvicorn community_voice.api.main:app --host 0.0.0.0 --port 8800"]`,
              },
            ],
          },
          {
            id: "phase1-b",
            letter: "B",
            shortTitle: "frontend/Dockerfile",
            tabName: "Frontend Dockerfile",
            title: "Step 2: Create frontend/Dockerfile (in frontend/ directory)",
            why: `<ol>
  <li><strong><code>ARG NEXT_PUBLIC_API_URL</code> &amp; <code>ENV NEXT_PUBLIC_API_URL</code>:</strong> Next.js compiles <code>NEXT_PUBLIC_*</code> environment variables directly into client-side JavaScript bundles at <code>npm run build</code> time. If this argument is missing during build time, client API calls fall back to <code>http://localhost:8800</code>, causing browser requests on the deployed site to fail with <code>Cannot reach the server</code>.</li>
  <li><strong><code>npm run build</code> &amp; <code>npm start</code>:</strong> Compiles Tailwind CSS 4 and React 19 into an optimized production bundle. Running <code>npm run dev</code> in production wastes memory and leaks development source maps.</li>
</ol>`,
            steps: [
              {
                heading: "Create frontend/Dockerfile",
                note: `<p>Create <code>frontend/Dockerfile</code> for production Ahead-Of-Time compilation:</p>`,
                lang: "docker",
                code: `FROM node:22-slim

WORKDIR /app

# copy dependency manifests
COPY package*.json ./
RUN npm install

# copy frontend source code
COPY . .

# embed backend api url during next.js compilation
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
            shortTitle: "CORS & Git Push",
            tabName: "CORS & Push",
            title: "Step 3 & 4: Configure CORS and Push to GitHub",
            why: `<p>FastAPI enforces the <strong>Same-Origin Policy</strong> via <code>CORSMiddleware</code>. Because the frontend runs on a separate Azure domain (<code>...frontend...azurecontainerapps.io</code>) from the backend (<code>...api...azurecontainerapps.io</code>), the browser will refuse to read API responses unless FastAPI returns <code>Access-Control-Allow-Origin</code>. Setting <code>FRONTEND_ORIGINS = ["*"]</code> ensures cross-origin requests succeed across any domain.</p>`,
            steps: [
              {
                heading: "Configure CORS in src/community_voice/api/main.py",
                note: `<p>In <code>src/community_voice/api/main.py</code> (around line 25), update <code>FRONTEND_ORIGINS</code>:</p>`,
                lang: "python",
                code: `# In src/community_voice/api/main.py:

FRONTEND_ORIGINS = ["*"] # you can also specify your frontend domain instead of "*" 
# after deployment and getting the link, e.g. ["https://yourfrontend.azurecontainerapps.io"]`,
              },
              {
                heading: "Commit and Push Codebase Updates",
                note: `<p>Push the Dockerfiles and CORS changes to GitHub:</p>`,
                lang: "bash",
                code: `git add Dockerfile.backend frontend/Dockerfile src/community_voice/api/main.py
git commit -m "chore: configure production dockerfiles, persistent data restoration, and CORS"
git push origin main`,
              },
            ],
          },
        ],
      },
      {
        id: "phase2",
        number: "02",
        title: "CLI Init & Resource Group",
        target: "Azure Subscription & switzerlandnorth",
        desc: "Register Azure resource providers and create resource group.",
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
            id: "phase2-a",
            letter: "A",
            shortTitle: "Register Providers",
            tabName: "Resource Providers",
            title: "Step 5: Register Azure Resource Providers",
            why: `<p>New Azure subscriptions have resource providers disabled by default. If <code>Microsoft.ContainerRegistry</code> or <code>Microsoft.App</code> are not registered, resource creation commands will fail with <code>MissingSubscriptionRegistration</code>.</p>`,
            steps: [
              {
                heading: "Register Required Azure Namespaces",
                note: `<p>Run in your terminal to register the Container Apps, Storage, and ACR providers:</p>`,
                lang: "bash",
                code: `az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
az provider register --namespace Microsoft.Storage
az provider register --namespace Microsoft.ContainerRegistry`,
              },
              {
                heading: "Verify Registration Status",
                note: `<p>Verify that both show <code>Registered</code>:</p>`,
                lang: "bash",
                code: `az provider show -n Microsoft.App --query "registrationState" -o tsv
az provider show -n Microsoft.ContainerRegistry --query "registrationState" -o tsv`,
              },
            ],
          },
          {
            id: "phase2-b",
            letter: "B",
            shortTitle: "Resource Group Setup",
            tabName: "Resource Group",
            title: "Step 6: Define Deployment Variables & Create Resource Group",
            why: `<ul>
  <li><strong><code>switzerlandnorth</code>:</strong> Microsoft's data center in Zurich. Deploying all resources to the same region eliminates cross-region data transfer fees and complies with subscription regional policies.</li>
  <li><strong><code>$RANDOM</code>:</strong> Azure Storage Accounts and Container Registries require globally unique names across all Azure customers worldwide.</li>
  <li><strong>Resource Group:</strong> Establishes a shared billing and lifecycle boundary. Deleting this single group tears down every resource cleanly.</li>
</ul>`,
            steps: [
              {
                heading: "Export Environment Variables",
                note: `<p>Define unique variables for your Zurich deployment:</p>`,
                lang: "bash",
                code: `export RESOURCE_GROUP="community-voice-rg"
export LOCATION="switzerlandnorth"
export ENVIRONMENT_NAME="community-voice-env"
export ACR_NAME="communityvoiceacr$RANDOM"
export STORAGE_ACCOUNT="cvstorage$RANDOM"
export FILE_SHARE_NAME="appdata"`,
              },
              {
                heading: "Create the Resource Group",
                note: `<p>Create the resource group in <code>switzerlandnorth</code>:</p>`,
                lang: "bash",
                code: `az group create --name $RESOURCE_GROUP --location $LOCATION`,
              },
            ],
          },
        ],
      },
      {
        id: "phase3",
        number: "03",
        title: "Persistent Storage (Azure Files)",
        target: "Storage Account & SMB File Share",
        desc: "Create 10GB SMB share for SQLite, ChromaDB, and static knowledge base.",
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
            shortTitle: "Azure Files SMB Share",
            tabName: "Storage & Key",
            title: "Step 7: Create Storage Account & File Share",
            why: `<ol>
  <li><strong><code>Standard_LRS</code>:</strong> Locally Redundant Storage keeps three copies of your data within the Zurich data center, providing durability at minimal cost.</li>
  <li><strong><code>storage share-rm create</code>:</strong> Allocates an SMB cloud file share named <code>appdata</code>.</li>
  <li><strong><code>STORAGE_KEY</code>:</strong> The access secret required by Container Apps to authenticate with the storage account.</li>
</ol>`,
            steps: [
              {
                heading: "Create the Azure Storage Account",
                note: `<p>Create the storage account in your resource group:</p>`,
                lang: "bash",
                code: `az storage account create \\
  --name $STORAGE_ACCOUNT \\
  --resource-group $RESOURCE_GROUP \\
  --location $LOCATION \\
  --sku Standard_LRS \\
  --kind StorageV2`,
              },
              {
                heading: "Create the 10 GB SMB File Share",
                note: `<p>Create the file share named <code>appdata</code> with a 10 GB quota:</p>`,
                lang: "bash",
                code: `az storage share-rm create \\
  --storage-account $STORAGE_ACCOUNT \\
  --resource-group $RESOURCE_GROUP \\
  --name $FILE_SHARE_NAME \\
  --quota 10`,
              },
              {
                heading: "Retrieve Storage Account Key",
                note: `<p>Export the access key required to link storage to the Container Apps Environment:</p>`,
                lang: "bash",
                code: `export STORAGE_KEY=$(az storage account keys list \\
  --resource-group $RESOURCE_GROUP \\
  --account-name $STORAGE_ACCOUNT \\
  --query "[0].value" --output tsv)`,
              },
            ],
          },
        ],
      },
      {
        id: "phase4",
        number: "04",
        title: "ACR & GitHub Actions CI/CD",
        target: "Azure Container Registry & GitHub Workflows",
        desc: "Create private ACR, set repo secrets, and automated dual image build workflow.",
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
            shortTitle: "ACR & GitHub Secrets",
            tabName: "Registry Setup",
            title: "Step 8 & 9: Create Azure Container Registry & Configure Secrets",
            why: `<p>Basic SKU provides private Docker image hosting. Setting <code>--admin-enabled true</code> allows GitHub Actions and Azure Container Apps to pull and push images using standard Docker token authentication without hardcoding passwords in git commits.</p>`,
            steps: [
              {
                heading: "Create Private Azure Container Registry",
                note: `<p>Create the registry and enable admin credentials:</p>`,
                lang: "bash",
                code: `az acr create \\
  --resource-group $RESOURCE_GROUP \\
  --name $ACR_NAME \\
  --sku Basic \\
  --admin-enabled true`,
              },
              {
                heading: "Retrieve Registry Credentials",
                note: `<p>Display credentials to use in GitHub Secrets:</p>`,
                lang: "bash",
                code: `az acr credential show --name $ACR_NAME`,
              },
              {
                heading: "Configure GitHub Repository Secrets",
                note: `<p>Navigate to <strong>GitHub Repository &gt; Settings &gt; Secrets and variables &gt; Actions &gt; New repository secret</strong> and add:</p>
<ul>
  <li><code>AZURE_ACR_USERNAME</code>: Paste your ACR username</li>
  <li><code>AZURE_ACR_PASSWORD</code>: Paste your ACR password (from <code>passwords[0].value</code>)</li>
</ul>`,
                lang: "text",
                code: `Secret 1: AZURE_ACR_USERNAME = (your ACR username)
Secret 2: AZURE_ACR_PASSWORD = (your ACR access password)`,
              },
            ],
          },
          {
            id: "phase4-b",
            letter: "B",
            shortTitle: "GitHub Actions Workflow",
            tabName: "CI/CD Workflow",
            title: "Step 10: Create GitHub Actions Workflow for Dual-Image Builds",
            why: `<ul>
  <li><strong>Bypassing the <code>TasksOperationsNotAllowed</code> restriction:</strong> Microsoft disables cloud-based compilation (<code>az acr build</code>) on free/credit-based subscriptions. GitHub Actions provides free cloud compute with Docker pre-installed, building your images on GitHub and pushing the finished artifacts to Azure ACR.</li>
  <li><strong>Automated CI/CD:</strong> Future pushes to <code>main</code> automatically compile new container versions.</li>
</ul>`,
            steps: [
              {
                heading: "Create .github/workflows/deploy-azure.yml",
                note: `<p>Create <code>.github/workflows/deploy-azure.yml</code> in your local repository (replace <code>ACR_LOGIN_SERVER</code> with your <code>$ACR_NAME.azurecr.io</code>):</p>`,
                lang: "yaml",
                code: `name: Build and Push to Azure ACR

on:
  push:
    branches: [ main ]
  workflow_dispatch:

env:
  ACR_LOGIN_SERVER: communityvoiceacr18754.azurecr.io # use your ACR name

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Log in to Azure Container Registry
        uses: docker/login-action@v3
        with:
          registry: \${{ env.ACR_LOGIN_SERVER }}
          username: \${{ secrets.AZURE_ACR_USERNAME }}
          password: \${{ secrets.AZURE_ACR_PASSWORD }}

      # build and push backend image
      - name: Build & Push Backend Container
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile.backend
          push: true
          tags: \${{ env.ACR_LOGIN_SERVER }}/community-voice-api:latest

      # build and push frontend image
      - name: Build & Push Frontend Container
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: ./frontend/Dockerfile
          push: true
          tags: \${{ env.ACR_LOGIN_SERVER }}/community-voice-frontend:latest`,
              },
              {
                heading: "Push Workflow & Verify Image Push",
                note: `<p>Commit and push the workflow to trigger initial builds:</p>`,
                lang: "bash",
                code: `git add .github/workflows/deploy-azure.yml
git commit -m "ci: automate backend and frontend builds to Azure ACR"
git push origin main`,
              },
              {
                heading: "Verify Built Images in ACR",
                note: `<p>Verify in your terminal once the GitHub Action turns green:</p>`,
                lang: "bash",
                code: `az acr repository list --name $ACR_NAME --output table`,
              },
            ],
          },
        ],
      },
      {
        id: "phase5",
        number: "05",
        title: "Container Environment & Link",
        target: "community-voice-env & volumedata",
        desc: "Create Container Apps environment and link Azure File Share as volumedata.",
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
            id: "phase5-a",
            letter: "A",
            shortTitle: "Create Environment & Storage Link",
            tabName: "Env & Storage Link",
            title: "Step 11: Create Container Environment & Link File Share",
            why: `<ol>
  <li><strong><code>env create</code>:</strong> Sets up the Kubernetes micro-VM cluster, manages ingress routing, and allocates internal DNS.</li>
  <li><strong><code>env storage set</code>:</strong> Links the Azure Storage account credentials to the environment under the alias <code>volumedata</code>. Individual containers can now mount this storage share to any local directory path.</li>
</ol>`,
            steps: [
              {
                heading: "Create the Container Apps Environment",
                note: `<p>Create the managed environment in Zurich:</p>`,
                lang: "bash",
                code: `az containerapp env create \\
  --name $ENVIRONMENT_NAME \\
  --resource-group $RESOURCE_GROUP \\
  --location $LOCATION`,
              },
              {
                heading: "Link File Share as 'volumedata'",
                note: `<p>Attach the storage account to the environment with ReadWrite access:</p>`,
                lang: "bash",
                code: `az containerapp env storage set \\
  --name $ENVIRONMENT_NAME \\
  --resource-group $RESOURCE_GROUP \\
  --storage-name "volumedata" \\
  --azure-file-account-name $STORAGE_ACCOUNT \\
  --azure-file-account-key $STORAGE_KEY \\
  --azure-file-share-name $FILE_SHARE_NAME \\
  --access-mode ReadWrite`,
              },
            ],
          },
        ],
      },
      {
        id: "phase6",
        number: "06",
        title: "Deploy Backend Service",
        target: "community-voice-api (Port 8800)",
        desc: "Initial deployment, JSON volume patch script, and v2 storage initialization.",
        theme: {
          text: "text-uj-orange",
          borderLeft: "border-uj-orange",
          activeBorder: "border-uj-orange/60",
          cardBg: "bg-uj-orange/[0.04]",
          badge: "bg-uj-orange/10 text-orange-300 border-uj-orange/30",
          badgeActive: "bg-uj-orange text-white border-orange-400",
          partActive: "bg-uj-orange text-white",
          bullet: "bg-uj-orange",
        },
        parts: [
          {
            id: "phase6-a",
            letter: "A",
            shortTitle: "Initial Backend Deployment",
            tabName: "Initial Deploy",
            title: "Step 12: Initial Backend Container Deployment",
            why: `<ol>
  <li><strong><code>--target-port 8800 --ingress external</code>:</strong> Exposes port 8800 with public HTTPS access.</li>
  <li><strong><code>--min-replicas 1</code>:</strong> Ensures at least one instance runs 24/7, eliminating cold starts when citizens submit reports.</li>
  <li><strong><code>--env-vars</code>:</strong> Pydantic validates settings on startup; missing keys will cause the app to crash.</li>
</ol>`,
            steps: [
              {
                heading: "Retrieve ACR Password & Deploy Backend",
                note: `<p>Launch the initial backend container instance:</p>`,
                lang: "bash",
                code: `export ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

az containerapp create \\
  --name "community-voice-api" \\
  --resource-group $RESOURCE_GROUP \\
  --environment $ENVIRONMENT_NAME \\
  --image "$ACR_NAME.azurecr.io/community-voice-api:latest" \\
  --registry-server "$ACR_NAME.azurecr.io" \\
  --registry-username $ACR_NAME \\
  --registry-password $ACR_PASSWORD \\
  --target-port 8800 \\
  --ingress external \\
  --min-replicas 1 \\
  --max-replicas 1 \\
  --cpu 0.5 \\
  --memory 1.0Gi \\
  --env-vars \\
    GEMINI_API_KEY="your-gemini-key" \\
    GROQ_API_KEY="your-groq-key" \\
    TAVILY_API_KEY="your-tavily-key" \\
    JWT_SECRET="$(openssl rand -hex 32)" \\
    GEMINI_MODEL="gemini-3.1-flash-lite" \\
    GROQ_MODEL="openai/gpt-oss-20b"`,
              },
            ],
          },
          {
            id: "phase6-b",
            letter: "B",
            shortTitle: "Mount Persistent Volume",
            tabName: "Patch Storage",
            title: "Step 13: Mount the Persistent Volume to /app/data via CLI Script",
            why: `<ol>
  <li><code>az containerapp show -o json</code> outputs the exact live JSON schema of the container.</li>
  <li>The script programmatically inserts <code>volumes:</code> and <code>volumeMounts:</code> into the container template.</li>
  <li>YAML 1.2 is a superset of JSON, allowing <code>az containerapp update --yaml</code> to apply <code>ca_patched.json</code> directly without manual editing mistakes.</li>
</ol>`,
            steps: [
              {
                heading: "Create patch_storage.py Script",
                note: `<p>To prevent making mistakes when manually editing YAML files, create <code>patch_storage.py</code>:</p>`,
                lang: "python",
                code: `import json
import os
import subprocess

rg = os.environ.get("RESOURCE_GROUP", "community-voice-rg")
app_name = "community-voice-api"

print(f"1. Fetching live configuration for {app_name} from {rg}...")
cmd = f"az containerapp show --name {app_name} --resource-group {rg} -o json"
raw = subprocess.check_output(cmd, shell=True)
data = json.loads(raw)

print("2. Adding storage volume to template...")
template = data["properties"]["template"]

# define the storage volume linked in step 11
template["volumes"] = [{
    "name": "azure-files-volume",
    "storageName": "volumedata",
    "storageType": "AzureFile"
}]

# mount it inside the container at /app/data
template["containers"][0]["volumeMounts"] = [{
    "mountPath": "/app/data",
    "volumeName": "azure-files-volume"
}]

print("3. Writing validated patch to ca_patched.json...")
with open("ca_patched.json", "w") as f:
    json.dump(data, f, indent=2)

print("SUCCESS: ca_patched.json is ready!")`,
              },
              {
                heading: "Run Script & Apply Storage Patch",
                note: `<p>Execute the script and update the container app:</p>`,
                lang: "bash",
                code: `python patch_storage.py

az containerapp update \\
  --name "community-voice-api" \\
  --resource-group $RESOURCE_GROUP \\
  --yaml ca_patched.json`,
              },
            ],
          },
          {
            id: "phase6-c",
            letter: "C",
            shortTitle: "Force Revision v2 & Health",
            tabName: "Revision v2",
            title: "Step 14: Force Revision v2 to Initialize Storage and Seed Database",
            why: `<p>Adding <code>--revision-suffix "v2"</code> forces Azure to spin up a new replica (<code>community-voice-api--v2</code>), run the startup script (<code>CMD</code>), copy default data, and seed the user accounts into SQLite.</p>`,
            steps: [
              {
                heading: "Deploy Revision v2",
                note: `<p>Force a new revision to trigger initialization:</p>`,
                lang: "bash",
                code: `az containerapp update \\
  --name "community-voice-api" \\
  --resource-group $RESOURCE_GROUP \\
  --revision-suffix "v2"`,
              },
              {
                heading: "Retrieve Backend URL & Test Health",
                note: `<p>Verify backend health (returns <code>{"status":"ok"}</code>):</p>`,
                lang: "bash",
                code: `export BACKEND_URL=$(az containerapp show \\
  --name "community-voice-api" \\
  --resource-group $RESOURCE_GROUP \\
  --query "properties.configuration.ingress.fqdn" -o tsv)

echo "https://$BACKEND_URL/health"
curl https://$BACKEND_URL/health`,
              },
            ],
          },
        ],
      },
      {
        id: "phase7",
        number: "07",
        title: "Deploy Frontend Service",
        target: "community-voice-frontend (Port 3000)",
        desc: "Rebuild image with live backend URL and deploy public frontend ACA.",
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
            shortTitle: "Inject Backend URL in CI/CD",
            tabName: "Build Args",
            title: "Step 15: Rebuild Frontend Image with the Live Backend URL",
            why: `<p>Next.js client-side code (<code>frontend/src/lib/config.ts</code>) reads <code>process.env.NEXT_PUBLIC_API_URL</code>. Providing it as an <code>ARG</code> during Docker build ensures the frontend sends requests to your live Azure backend rather than falling back to <code>localhost:8800</code>.</p>`,
            steps: [
              {
                heading: "Update .github/workflows/deploy-azure.yml",
                note: `<p>In <code>.github/workflows/deploy-azure.yml</code>, update the <code>Build & Push Frontend Container</code> step with your live <code>$BACKEND_URL</code> (no trailing slash):</p>`,
                lang: "yaml",
                code: `      # build and push frontend image
      - name: Build & Push Frontend Container
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: ./frontend/Dockerfile
          push: true
          build-args: |
            NEXT_PUBLIC_API_URL=https://community-voice-api.switzerlandnorth.azurecontainerapps.io
          tags: \${{ env.ACR_LOGIN_SERVER }}/community-voice-frontend:latest`,
              },
              {
                heading: "Push Workflow to Trigger Image Rebuild",
                note: `<p>Commit and push:</p>`,
                lang: "bash",
                code: `git commit -am "ci: inject live Azure backend URL into Next.js compilation"
git push origin main`,
              },
            ],
          },
          {
            id: "phase7-b",
            letter: "B",
            shortTitle: "Deploy Frontend Container",
            tabName: "Deploy Frontend",
            title: "Step 16 & 17: Deploy Frontend Container App & Sign In",
            why: `<p>Exposes the Next.js frontend on port 3000 with public HTTPS access, pointing all browser traffic to the pre-compiled production bundle.</p>`,
            steps: [
              {
                heading: "Deploy Frontend Container App",
                note: `<p>Once the GitHub Action completes, deploy the frontend service:</p>`,
                lang: "bash",
                code: `az containerapp create \\
  --name "community-voice-frontend" \\
  --resource-group $RESOURCE_GROUP \\
  --environment $ENVIRONMENT_NAME \\
  --image "$ACR_NAME.azurecr.io/community-voice-frontend:latest" \\
  --registry-server "$ACR_NAME.azurecr.io" \\
  --registry-username $ACR_NAME \\
  --registry-password $ACR_PASSWORD \\
  --target-port 3000 \\
  --ingress external \\
  --min-replicas 1 \\
  --max-replicas 1 \\
  --cpu 0.5 \\
  --memory 1.0Gi \\
  --env-vars \\
    NODE_ENV="production" \\
    PORT="3000"`,
              },
              {
                heading: "Retrieve Frontend URL",
                note: `<p>Export and print your live web application URL:</p>`,
                lang: "bash",
                code: `export FRONTEND_URL=$(az containerapp show \\
  --name "community-voice-frontend" \\
  --resource-group $RESOURCE_GROUP \\
  --query "properties.configuration.ingress.fqdn" -o tsv)

echo "Frontend Live Web URL: https://$FRONTEND_URL"`,
              },
            ],
          },
        ],
      },
      {
        id: "phase8",
        number: "08",
        title: "Verification & Maintenance",
        target: "Credentials & CLI Operations",
        desc: "Default login accounts, live logs, revision inspection, and storage quotas.",
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
            id: "phase8-a",
            letter: "A",
            shortTitle: "Default Credentials",
            tabName: "Login Accounts",
            title: "Default Login Accounts (Seeded)",
            why: `<p>The startup script seeds default accounts into <code>/app/data/app.db</code> on first boot, backed by the persistent Azure File Share.</p>`,
            steps: [
              {
                heading: "Pre-Configured System Accounts",
                note: `<p>Use these credentials to test citizen and administrator capabilities:</p>
<ul>
  <li><strong>Admin:</strong> <code>admin@communityvoice.test</code> / <code>AdminPass123</code><br>
    Access: Review Queue (<code>/review</code>), Dashboard (<code>/dashboard</code>), Draft approvals
  </li>
  <li><strong>Citizen 1:</strong> <code>citizen1@communityvoice.test</code> / <code>Citizen1Pass123</code><br>
    Access: Submit reports (<code>/submit</code>) with live SSE progress, view history (<code>/my-reports</code>)
  </li>
  <li><strong>Citizen 2:</strong> <code>citizen2@communityvoice.test</code> / <code>Citizen2Pass123</code><br>
    Access: Isolated report history & citizen capabilities
  </li>
</ul>`,
                lang: "text",
                code: `Admin: admin@communityvoice.test / AdminPass123
Citizen 1: citizen1@communityvoice.test / Citizen1Pass123
Citizen 2: citizen2@communityvoice.test / Citizen2Pass123`,
              },
            ],
          },
          {
            id: "phase8-b",
            letter: "B",
            shortTitle: "Maintenance Commands",
            tabName: "CLI Commands",
            title: "Essential Azure Maintenance Commands",
            why: `<p>Monitor container health, inspect live agent traces, follow Server-Sent Events, and audit storage usage on Azure Files.</p>`,
            steps: [
              {
                heading: "Live Backend Container Logs",
                note: `<p>Stream live logs and trace agent execution steps:</p>`,
                lang: "bash",
                code: `az containerapp logs show --name "community-voice-api" --resource-group $RESOURCE_GROUP --follow`,
              },
              {
                heading: "Live Frontend Container Logs",
                note: `<p>Stream live Next.js access and server logs:</p>`,
                lang: "bash",
                code: `az containerapp logs show --name "community-voice-frontend" --resource-group $RESOURCE_GROUP --follow`,
              },
              {
                heading: "Inspect Azure File Share Usage",
                note: `<p>Check quota, file share properties, and storage utilization:</p>`,
                lang: "bash",
                code: `az storage share-rm show --name "appdata" --storage-account $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP`,
              },
              {
                heading: "List Container Revisions",
                note: `<p>View deployed container revisions and rollout history:</p>`,
                lang: "bash",
                code: `az containerapp revision list --name "community-voice-api" --resource-group $RESOURCE_GROUP --output table`,
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
        color: { value: ["#ffffff", "#0078d4", "#F26522"] },
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