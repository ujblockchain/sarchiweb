AOS.init({ duration: 800, once: true, offset: 50 });

document.addEventListener("DOMContentLoaded", () => {
  const map = L.map("map", {
    zoomControl: false,
    scrollWheelZoom: false,
  }).setView([-26.1825, 27.9976], 15);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap",
  }).addTo(map);
  L.marker([-26.1825, 27.9976])
    .addTo(map)
    .bindPopup("UJ Blockchain Research Chair");
});

// particles
(async () => {
  await window.tsParticles.load("particles-container", {
    background: { color: { value: "transparent" } },
    fpsLimit: 60,
    particles: {
      color: { value: ["#ffffff", "#F26522"] },
      links: {
        color: "#ffffff",
        distance: 150,
        enable: true,
        opacity: 0.1,
        width: 1,
      },
      move: { enable: true, speed: 0.6 },
      number: { density: { enable: true, area: 800 }, value: 40 },
      opacity: { value: 0.3 },
      shape: { type: "circle" },
      size: { value: { min: 1, max: 2 } },
    },
  });
})();

// typewriter component
function typewriter() {
  return {
    words: ["Blockchain", "AI", "IoT", "GovTech", "AgriTech", "EdTech", "Web3"],
    currentWordIndex: 0,
    displayedText: "",
    isDeleting: false,
    typingSpeed: 100,
    deletingSpeed: 50,
    delayBetweenWords: 2000,

    init() {
      this.type();
    },

    type() {
      const currentWord = this.words[this.currentWordIndex];

      if (this.isDeleting) {
        this.displayedText = currentWord.substring(
          0,
          this.displayedText.length - 1,
        );
      } else {
        this.displayedText = currentWord.substring(
          0,
          this.displayedText.length + 1,
        );
      }

      let typeSpeed = this.typingSpeed;

      if (!this.isDeleting && this.displayedText === currentWord) {
        typeSpeed = this.delayBetweenWords;
        this.isDeleting = true;
      } else if (this.isDeleting && this.displayedText === "") {
        this.isDeleting = false;
        this.currentWordIndex = (this.currentWordIndex + 1) % this.words.length;
        typeSpeed = 500;
      } else if (this.isDeleting) {
        typeSpeed = this.deletingSpeed;
      }

      setTimeout(() => {
        this.type();
      }, typeSpeed);
    },
  };
}

// alpine data
function appData() {
  return {
    mobileMenuOpen: false,
    scrolled: false,
    isModalOpen: false,
    isGalleryOpen: false,
    activeGalleryIndex: 0,

    selectedCategory: "All",
    categories: [
      "All",
      "Blockchain",
      "AI",
      "IoT",
      "GovTech",
      "AgriTech",
      "EdTech",
    ],

    selectedActivityCategory: "All",
    activityCategories: [
      "All",
      "Blockchain",
      "Demo Day",
      "BACISS",
      "Training",
      "Mainstreaming Blockchain",
    ],

    selectedGalleryCategory: "All",
    galleryCategories: [
      "All",
      "BACISS",
      "Blockchain",
      "Awards",
      "Media Day",
      "Masterclass",
    ],

    navItems: [
      { name: "Home", href: "#home" },
      { name: "About", href: "#about" },
      { name: "Innovations", href: "#innovations" },
      { name: "Activities", href: "#activities" },
      { name: "Gallery", href: "#gallery" },
      { name: "Team", href: "#team" },
      { name: "Events", href: "#events" },
      { name: "Research", href: "#publications" },
    ],
    stats: [
      { value: "850+", label: "Code Deployments" },
      { value: "15+", label: "Apps" },
      { value: "25+", label: "Papers" },
      { value: "12+", label: "Trainings" },
    ],
    leadership: [
      {
        name: "Prof. Nnamdi Nwulu",
        role: "Director",
        image: "/static/img/prof_nnamdi_nwulu.jpeg",
        linkedin: "https://www.linkedin.com/in/nnamdi-nwulu-292666111/",
        scholar: "https://scholar.google.com/citations?user=CzQ1lyYAAAAJ&hl=en",
        research: "https://www.researchgate.net/profile/Nnamdi-Nwulu",
      },
      {
        name: "Dr. Luca Mazzola",
        role: "Co-Director",
        image: "/static/img/Luca.jpeg",
        linkedin: "https://ch.linkedin.com/in/mazzolaluca",
        scholar: "https://scholar.google.com/citations?user=ZMNUo_IAAAAJ&hl=it",
        research: "https://www.researchgate.net/profile/Luca-Mazzola-3",
      },
    ],
    teamMembers: [
      {
        name: "Dimakatso Tshabalala",
        role: "Administrative Assistant",
        image: "/static/img/dima.jpg",
        linkedin: "https://www.linkedin.com/in/dimakatso-tshabalala-175262b2/",
        github: "#",
        scholar: "#",
      },
      {
        name: "Akinyomi Oluwarotimi",
        role: "Lead Developer",
        image: "/static/img/oluwarotimi.jpg",
        linkedin: "https://www.linkedin.com/in/oluwarotimiakinyomi/",
        github: "https://github.com/edmundrotimi",
        scholar: "#",
      },
      {
        name: "Ajibola Oyedeji",
        role: "AI & Blockchain Developer",
        image: "/static/img/ayodeji.jfif",
        linkedin: "https://www.linkedin.com/in/ajibola-oyedeji-128ab5190/",
        github: "https://github.com/JblIdeal",
        scholar: "https://scholar.google.com/citations?user=KJg18j0AAAAJ&hl=en",
      },
       {
        name: "Oluwadamilola Esan",
        role: "Blockchain Researcher",
        image: "/static/img/esan.png",
        linkedin: "https://www.linkedin.com/in/oluwadamilola-esan-534118202/",
        github: "#",
        scholar: "#",
      },
      {
        name: "Timileyin Abiodun",
        role: "AI & Blockchain Developer",
        image: "/static/img/timi.png",
        linkedin: "https://www.linkedin.com/in/timileyin/",
        github: "https://github.com/timileyin19",
        scholar: "https://scholar.google.com/citations?user=ZlkAtpwAAAAJ&hl=en",
      },
      {
        name: "Nazire Mathe",
        role: "Fullstack Developer",
        image: "/static/img/nazire.jpg",
        linkedin: "https://www.linkedin.com/in/nazire-mathe-98674022b?trk=contact-info",
        github: "#",
        scholar: "#",
      },
        {
        name: "Masibonge Shabalala",
        role: "Fullstack Developer",
        image: "/static/img/shabalala.png",
        linkedin: "https://www.linkedin.com/in/masibonge-shabalala-344464284/",
        github: "https://github.com/Masibonge05",
        scholar: "#",
      },
        {
        name: "Fulufhelo Nageli",
        role: "Frontend Developer",
        image: "/static/img/fulu.jpg",
        linkedin: "https://www.linkedin.com/in/fulufhelo-nageli-ba0856292/",
        github: "#",
        scholar: "#",
      },
    ],
    activities: [
      {
        id: 1,
        category: "BACISS",
        date: "Nov 2025",
        title: "Blockchain, AI, & Cloud Innovation Startup School (BACISS)",
        desc: "From Sport Science to Smart Contracts | Testimonial.",
        image: "/static/img/baciss.jpg",
        videoUrl: "https://youtube.com/embed/g7yDXpxSED8?si=38RAIubpUmliWheA",
      },
      {
        id: 2,
        category: "Demo Day",
        date: "Aug 2024",
        title: "Demo Day 2024",
        desc: "Short recap video on how UJ Blockchain's Demo Day went.",
        image: "/static/img/demoday.jpg",
        videoUrl:
          "https://www.youtube.com/embed/xI3swHZV9jI?si=NwT8rBBaLao7jOyp",
      },
      {
        id: 3,
        category: "Blockchain",
        date: "Jul 2024",
        title: "Food Trolley Launch Day",
        desc: "Successfully launched the Food Trolley across all UJ campuses.",
        image: "/static/img/foodtrolley_.jpg",
        videoUrl:
          "https://www.youtube.com/embed/IRMAeDvybqw?si=slXrn0eAgs8bX-5n",
      },
      {
        id: 4,
        category: "Blockchain",
        date: "Sep 2024",
        title: "Leveling Up Your Technical Skills As A Blockchain Developer",
        desc: "Highlights and Key Takeaways of the UJ Blockchain Demo Day",
        image: "/static/img/levelup.jpg",
        videoUrl:
          "https://www.youtube.com/embed/EsnPPVYtZP4?si=uADy6rS6WaMLFkKF",
      },
      {
        id: 5,
        category: "Training",
        date: "Sep 2023",
        title: "Time Series Analysis",
        desc: "Time Series Analysis for predicting future occurrences.",
        image: "/static/img/timeseries.jpg",
        videoUrl:
          "https://www.youtube.com/embed/XYhwzB6fUX4?si=G3ruDKP21DkZsvZ1",
      },
      {
        id: 6,
        category: "Mainstreaming Blockchain",
        date: "Apr 2023",
        title: "Mainstreaming Blockchain (MB)",
        desc: "Event Recap - Mainstreaming Blockchain MB A Thought Leadership Media Event.",
        image: "/static/img/mb.jpg",
        videoUrl:
          "https://www.youtube.com/embed/27oJIRaRwlM?si=sQfsMCdR5RSVVKWn",
      },
    ],

    upcomingEvents: [
      {
        day: "12",
        month: "Dec",
        title: "Understanding Artificial Intelligence for Water and Environmental ...",
        type: "ECOWAS Regional Advisory Council on IWRM",
      },
      {
        day: "13",
        month: "NOV",
        title: "Africa Stablecoin Summit 2025",
        type: "UJ Blockchain Innovation Demo",
      },
      {
        day: "05",
        month: "Nov",
        title: "Mpilisweni Secondary School Training",
        type: "Community Engagement",
      },
    ],
    projects: [
      {
        id: 1,
        title: "Workflow Designer",
        category: "Blockchain",
        shortDesc: "No-code builder.",
        description: "Drag-and-drop interface for building DApps.",
        image: "/static/img/designer.jpg",
        videoUrl:
          "https://www.youtube.com/embed/4rutazuehKI?si=BkUsN9wHSvHbzONB",
      },
      {
        id: 2,
        title: "CertyFile",
        category: "AI",
        shortDesc: "Digital Credentials.",
        description: "Tamper-proof document verification on chain.",
        image: "/static/img/certyfile.jpg",
        videoUrl:
          "https://www.youtube.com/embed/gy0THfHHsH8?si=4bVMVS0TAEORCQHs",
      },
      {
        id: 3,
        title: "Tranzfile",
        category: "Blockchain",
        shortDesc: "Secure Transfer.",
        description: "Encrypted file sharing with immutable logs.",
        image: "/static/img/tranzfile.jpg",
        videoUrl:
          "https://www.youtube.com/embed/FyZlstKIyyk?si=vGSpnClnFMa8N55k",
      },
      {
        id: 4,
        title: "TenderBlock",
        category: "GovTech",
        shortDesc: "Fair Procurement.",
        description: "AI & Blockchain for transparent tenders.",
        image: "/static/img/tenderblock.jpg",
        videoUrl:
          "https://www.youtube.com/embed/JWprDEXcKsM?si=Yc_N6e9rsZUhSLM2",
      },
      {
        id: 5,
        title: "Food Trolley",
        category: "Blockchain",
        shortDesc: "Donation Tracking.",
        description: "Traceable food aid distribution.",
        image: "/static/img/foodtrolley.jpg",
        videoUrl:
          "https://www.youtube.com/embed/L_hPs9qhNEU?si=a87A_r7bj96xi4N9",
      },
      {
        id: 6,
        title: "FloraShield",
        category: "AgriTech",
        shortDesc: "AI Plant Doctor.",
        description: "Detects diseases via image analysis.",
        image: "/static/img/florashield.jpg",
        videoUrl:
          "https://www.youtube.com/embed/GhlxIKJcX5Y?si=sXUOJA2dUCUWtop",
      },
      {
        id: 7,
        title: "Edu Quiz",
        category: "EdTech",
        shortDesc: "Gamified Learning.",
        description: "Earn tokens while learning.",
        image: "/static/img/eduquiz.jpg",
        videoUrl:
          "https://www.youtube.com/embed/Kf4BFDYy2kM?si=WsaiKmg8HrwmYZVy",
      },
      {
        id: 8,
        title: "CrackScan",
        category: "IoT",
        shortDesc: "Drone Inspection.",
        description: "Automated infrastructure maintenance.",
        image: "/static/img/crackscan.jpg",
        videoUrl:
          "https://www.youtube.com/embed/JtRFPl4Nhls?si=7gJaaVPl3U17q4WR",
      },
      {
        id: 9,
        title: "Workflow Builder",
        category: "Blockchain",
        shortDesc: "Dual-canvas no-code DApp builder.",
        description:
          "A visual development platform combining UI Design and Logic canvases.",
        image: "/static/img/workflow.jpg",
        videoUrl:
          "https://www.youtube.com/embed/ljUW6qg4CsY?si=X_Zv5ZzHnRMuRsxm",
      },
      {
        id: 10,
        title: "AfriLance",
        category: "GovTech",
        shortDesc: "Web3 Freelance Marketplace.",
        description: "A decentralized marketplace for African talent.",
        image: "/static/img/afrilance.jpg",
        videoUrl:
          "https://www.youtube.com/embed/tFwA1KXWkHg?si=Z1akgmQAs0kofrmf",
      },
    ],
    publications: [
      {
        year: "2025",
        journal: "International Journal of Sustainable Energy",
        title:
          "Evaluating the use of blockchain technology and identifying ...",
        authors:
          "Love Opeyemi David, Nnamdi Ikechi Nwulu, Clinton Ohis Aigbavboa, Adeyemi Adepoju, Omoseni Oyindamola Adepoju",
        link: "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=CzQ1lyYAAAAJ&sortby=pubdate&citation_for_view=CzQ1lyYAAAAJ:7H_MAutzIkAC",
      },
      {
        year: "2025",
        journal: "Frontiers in Energy Research",
        title:
          "Leveraging blockchain technology for cost efficiency of renewable energy",
        authors: "Nnamdi Nwulu, Love David, Tayo Uthman Badrudeen",
        link: "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=CzQ1lyYAAAAJ&sortby=pubdate&citation_for_view=CzQ1lyYAAAAJ:6bLC7aUMtPcC",
      },
      {
        year: "2025",
        journal: "Energy Nexus",
        title:
          "Enhancing transparency and efficiency in green energy management through blockchain ...",
        authors: "Oliver O Apeh, Nnamdi I Nwulu",
        link: "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=CzQ1lyYAAAAJ&sortby=pubdate&citation_for_view=CzQ1lyYAAAAJ:L1USKYWJimsC",
      },
    ],

    galleryImages: [
      {
        url: "/static/img/naziri_demo.png",
        title: "Africa Stablecoin Submit 2025 Afrilance demo",
        category: "Blockchain",
      },
      {
        url: "/static/img/masi_demo.png",
        title: "Africa Stablecoin Submit 2025 Webflow demo",
        category: "Blockchain",
      },
      {
        url: "/static/img/nobuhle_mbuyisa_gold_medal.png",
        title:
          "Nobuhle Mbuyisa gold medal in blockchain technology BRICS Future SkillsTech Challenge in Kazan, Russia",
        category: "Awards",
      },
      {
        url: "/static/img/miriam_sithole_award.png",
        title:
          "Miriam Sithole IEEE blockchain technical community region 8 student excellence award in Romania",
        category: "Awards",
      },
      {
        url: "/static/img/miriam_sithole_award_2.png",
        title:
          "Miriam Sithole first place for best final year project at EEE project demo day.",
        category: "Awards",
      },
      {
        url: "/static/img/prof_nnamdi_nwulu_remark.png",
        title:
          "Prof. Nnamdi Nwulu remark on The Algorithm, the Ledger and the Technologist Reimagining",
        category: "Media Day",
      },
      {
        url: "/static/img/baciss_2025.png",
        title: "BACISS 2025",
        category: "BACISS",
      },
      {
        url: "/static/img/masterclass_2025.png",
        title: "Masterclass 2025",
        category: "Masterclass",
      },
    ],

    activeProject: {},

    get filteredProjects() {
      return this.selectedCategory === "All"
        ? this.projects
        : this.projects.filter((p) => p.category === this.selectedCategory);
    },

    get filteredActivities() {
      return this.selectedActivityCategory === "All"
        ? this.activities
        : this.activities.filter(
            (a) => a.category === this.selectedActivityCategory,
          );
    },

    get filteredGallery() {
      return this.selectedGalleryCategory === "All"
        ? this.galleryImages
        : this.galleryImages.filter(
            (g) => g.category === this.selectedGalleryCategory,
          );
    },

    get relatedList() {
      if (this.activeProject && this.activeProject.date) {
        return this.activities;
      }
      return this.projects;
    },

    openModal(item) {
      this.activeProject = item;
      this.isModalOpen = true;
      document.body.style.overflow = "hidden";
    },
    closeModal() {
      this.isModalOpen = false;
      document.body.style.overflow = "auto";
    },

    // Gallery Functions
    openGallery(index) {
      this.activeGalleryIndex = index;
      this.isGalleryOpen = true;
      document.body.style.overflow = "hidden";
    },
    closeGallery() {
      this.isGalleryOpen = false;
      document.body.style.overflow = "auto";
    },
    nextGalleryImage() {
      this.activeGalleryIndex =
        (this.activeGalleryIndex + 1) % this.filteredGallery.length;
    },
    prevGalleryImage() {
      this.activeGalleryIndex =
        (this.activeGalleryIndex - 1 + this.filteredGallery.length) %
        this.filteredGallery.length;
    },
  };
}
