window.bacissPortal = function () {
  return {
    copiedTarget: null,

    links: {
      lectureTeams:
        "https://teams.microsoft.com/meet/3295303883813545?p=gzYg7Vf1SKbhbixU8a",
      googleDrive:
        "https://drive.google.com/drive/folders/1JDUid4YL6CfK6ROc02QZ4kAvLc_xqK8E?usp=sharing",
      supportTeams:
        "https://teams.microsoft.com/meet/346606700875325?p=ikeObmhgt4kutLVyMP",
      emailSupport: "blockchain@uj.ac.za",
    },

    wifi: {
      ssid: "UJ_BACISS_GUEST",
      password: "UJBlockchain2026!",
    },

    init() {
      this.initMap();
      this.generateQRCodes();
    },

    generateQRCodes() {
      this.$nextTick(() => {
        if (typeof QRious === "undefined") {
          console.warn("QRious library not loaded yet.");
          return;
        }

        const renderQR = (elementId, value, size = 160) => {
          const el = document.getElementById(elementId);
          if (el) {
            new QRious({
              element: el,
              value: value,
              size: size,
              background: "#ffffff",
              foreground: "#0b1120",
              level: "M",
            });
          }
        };

        renderQR("qr-lecture-canvas", this.links.lectureTeams, 160);
        renderQR("qr-drive-canvas", this.links.googleDrive, 160);
        renderQR("qr-support-canvas", this.links.supportTeams, 160);
        renderQR("qr-email-canvas", "mailto:" + this.links.emailSupport, 160);

        // wi-fi string format for auto-connection
        const wifiString = `WIFI:T:WPA;S:${this.wifi.ssid};P:${this.wifi.password};;`;
        renderQR("qr-wifi-canvas", wifiString, 210);
      });
    },

    initMap() {
      const tryInit = () => {
        const mapContainer = document.getElementById("venue-map");
        if (!mapContainer) return;

        if (!window.L) {
          setTimeout(tryInit, 100);
          return;
        }

        if (mapContainer._leaflet_id) return;

        const lat = -26.18247;
        const lng = 28.00016;

        const map = L.map("venue-map", {
          center: [lat, lng],
          zoom: 16,
          scrollWheelZoom: false,
        });

        //  openstreetmap tile endpoint
        const tileLayer = L.tileLayer(
          "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
          {
            attribution:
              '&copy; <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a>',
            className: "dark-map-tiles",
            maxZoom: 19,
          },
        );

        let hasError = false;

        tileLayer.on("tileerror", function () {
          if (hasError) return;
          hasError = true;

          // embedded vector campus view
          mapContainer.innerHTML = `
            <div style="position: relative; width: 100%; height: 100%; background: #070d18; border-radius: 1.25rem; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; padding: 24px;">
              <svg style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0.25;" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#f26522" stroke-width="0.7"/>
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />
                <!-- Stylized Auckland Park campus arterial lines -->
                <path d="M -50 120 Q 200 180 550 100" stroke="#38bdf8" stroke-width="3" fill="none" opacity="0.6"/>
                <path d="M 120 -50 L 180 450" stroke="#f26522" stroke-width="4" fill="none" opacity="0.6"/>
                <path d="M 280 -50 L 320 450" stroke="#94a3b8" stroke-width="2" fill="none" opacity="0.4"/>
              </svg>

              <div style="position: relative; z-index: 2; display: flex; justify-content: space-between; align-items: center;">
                <div style="background: rgba(11, 17, 32, 0.85); backdrop-filter: blur(8px); padding: 6px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); font-size: 11px; font-weight: bold; color: #f26522; font-family: monospace;">
                  <i class="fas fa-university" style="margin-right: 6px;"></i> UJ Kingsway Campus (APK)
                </div>
                <div style="background: rgba(11, 17, 32, 0.85); backdrop-filter: blur(8px); padding: 6px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: #94a3b8; font-family: monospace;">
                  -26.18247, 28.00016
                </div>
              </div>

              <div style="position: relative; z-index: 2; align-self: center; text-align: center; margin: auto;">
                <div style="position: relative; display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; margin-bottom: 12px;">
                  <div style="position: absolute; width: 64px; height: 64px; background: rgba(242, 101, 34, 0.25); border-radius: 50%; animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;"></div>
                  <div style="position: relative; width: 44px; height: 44px; background: #f26522; border: 3px solid #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; box-shadow: 0 0 25px rgba(242,101,34,0.9);">
                    <i class="fas fa-location-dot"></i>
                  </div>
                </div>
                <div style="background: rgba(6, 9, 19, 0.95); border: 1px solid rgba(242, 101, 34, 0.4); padding: 12px 20px; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); max-width: 320px;">
                  <strong style="color: #ffffff; font-size: 13px; display: block;">Lab 219, DEEES Building</strong>
                  <span style="color: #f26522; font-size: 11px; font-weight: 600; display: block; margin-top: 2px;">Faculty of Engineering (FEBE)</span>
                  <span style="color: #94a3b8; font-size: 11px; display: block; margin-top: 4px;">Auckland Park, Johannesburg</span>
                </div>
              </div>

              <div style="position: relative; z-index: 2; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; background: rgba(11, 17, 32, 0.85); backdrop-filter: blur(8px); padding: 10px 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <span style="font-size: 11px; color: #cbd5e1;"><i class="fas fa-signs-post" style="color: #f26522; margin-right: 6px;"></i> Entry via Kingsway Gate or University Rd</span>
                <a href="https://maps.google.com/?q=-26.18247,28.00016" target="_blank" style="font-size: 11px; font-weight: bold; color: #ffffff; background: #f26522; padding: 6px 12px; border-radius: 8px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
                  Open Live GPS <i class="fas fa-arrow-up-right-from-square" style="font-size: 10px;"></i>
                </a>
              </div>
            </div>
          `;
        });

        tileLayer.addTo(map);

        // custom pulsing uj orange marker icon for leaflet
        const customIcon = L.divIcon({
          className: "custom-venue-pin",
          html: `
            <div style="position: relative; display: flex; align-items: center; justify-content: center; width: 36px; height: 36px;">
              <div style="position: absolute; width: 32px; height: 32px; background: rgba(242, 101, 34, 0.4); border-radius: 50%; animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;"></div>
              <div style="position: relative; width: 22px; height: 22px; background: #F26522; border: 3px solid #ffffff; border-radius: 50%; box-shadow: 0 0 15px rgba(242, 101, 34, 0.8);"></div>
            </div>
          `,
          iconSize: [36, 36],
          iconAnchor: [18, 18],
        });

        const marker = L.marker([lat, lng], { icon: customIcon }).addTo(map);

        const popupContent = `
          <div style="font-family: inherit; color: #0b1120; padding: 4px; min-width: 170px;">
            <strong style="color: #F26522; font-size: 13px;">BACISS 2026 Venue</strong><br/>
            <span style="font-size: 12px; font-weight: bold; color: #0f172a;">Lab 219, DEEES Building</span><br/>
            <span style="font-size: 11px; color: #475569;">Auckland Park Kingsway Campus, UJ</span>
          </div>
        `;

        marker.bindPopup(popupContent).openPopup();

        setTimeout(() => {
          map.invalidateSize();
        }, 250);
      };

      this.$nextTick(() => {
        tryInit();
      });
    },

    // clipboard copy with fallback
    async copyText(text, targetId) {
      let success = false;

      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(text);
          success = true;
        } catch (err) {
          console.warn("navigator.clipboard error, trying fallback...", err);
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
          console.error("All copy mechanisms failed:", err);
        }
      }

      if (success) {
        this.copiedTarget = targetId;
        setTimeout(() => {
          if (this.copiedTarget === targetId) {
            this.copiedTarget = null;
          }
        }, 2200);
      }
    },
  };
};

if (window.Alpine) {
  window.Alpine.data("bacissPortal", window.bacissPortal);
} else {
  document.addEventListener("alpine:init", () => {
    window.Alpine.data("bacissPortal", window.bacissPortal);
  });
}
