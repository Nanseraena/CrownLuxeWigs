/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#FCF6F6",
          100: "#F8ECEC",
          200: "#F0D4D6",
          300: "#E8B4B8",
          400: "#DE9096",
          500: "#D46D75",
          600: "#BF4F58",
          700: "#A23C44",
          800: "#863037",
          900: "#6F2A2F",
          dark: "#1A1A1A",
          gold: "#D4AF37",
          champagne: "#F7F1E5",
          cream: "#FAF8F5",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        serif: ["var(--font-serif)", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};
