tailwind.config = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', "sans-serif"],
      },
      colors: {
        uj: {
          orange: "#F26522",
          dark: "#0B1120",
          surface: "#151E2E",
          accent: "#1E293B",
          text: "#94A3B8",
        },
      },
      animation: {
        blob: "blob 10s infinite",
        float: "float 6s ease-in-out infinite",
        cursor: "cursor .75s step-end infinite",
      },
      keyframes: {
        blob: {
          "0%": { transform: "translate(0px, 0px) scale(1)" },
          "33%": { transform: "translate(30px, -50px) scale(1.1)" },
          "66%": { transform: "translate(-20px, 20px) scale(0.9)" },
          "100%": { transform: "translate(0px, 0px) scale(1)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        cursor: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0" },
        },
      },
      screens: {
        xs: "370px",
        xxs: "300px",
      },
    },
  },
};
