import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#0a4d3c",
          light: "#1a7f5e",
          dark: "#063a2d",
        },
        accent: {
          DEFAULT: "#ffd700",
          light: "#ffe44d",
        },
        success: "#28a745",
        danger: "#dc3545",
        warning: "#ffc107",
      },
      fontFamily: {
        inter: ["Inter", "sans-serif"],
        urdu: ["Noto Nastaliq Urdu", "serif"],
      },
    },
  },
  plugins: [],
};

export default config;
